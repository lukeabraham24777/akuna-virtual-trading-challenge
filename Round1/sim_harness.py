"""Local simulator harness for the Akuna virtual trading challenge (Round 1).

Not part of any submission. Usage:
    python3 sim_harness.py theo output1            # validate pricing engine vs TC1 ground truth + MC
    python3 sim_harness.py run output1 [seeds]     # run scenario battery for one bot
    python3 sim_harness.py h2h output1 output2 ... # all bots in the same sessions
    python3 sim_harness.py speed output1           # timing check

Environment mechanics reverse-engineered from trader.py + instructions + Discord intel:
  - score per session = 0.4 + 0.6*(N-rank)/(N-1) by PnL, bankrupt -> 0
  - RFQ routed to best price, remainder walks the book; FOK split among accepters
  - competitor archetypes: fixed width (true fair +/- 0.025), stalemate quoter,
    lattice, wide, noisy; customers: noise / biased / informed / lookahead
"""
import importlib
import math
import random
import sys
import time

ENV = importlib.import_module("output1")  # shared dataclasses (identical in every output file)

FED, AJR, THR = 1, 2, 3


# ---------------------------------------------------------------------------
# true-parameter reference pricing (validated Monte Carlo)
# ---------------------------------------------------------------------------
def mc_price(mp, values, option, n_paths=200000, seed=7):
    rng = random.Random(seed)
    hits = 0
    t = option.steps_until_expiry
    if t == 0:
        return option.expiry_valuation(values)
    for _ in range(n_paths):
        vals = dict(values)
        for _s in range(t):
            r = vals[FED]
            tilt = mp.rate_reversion_strength * (mp.rate_target - r)
            up = min(max(mp.rate_up_probability + tilt, 0.0), 1.0)
            dn = min(max(mp.rate_down_probability - tilt, 0.0), 1.0 - up)
            d = rng.random()
            nr = r
            if d < up:
                nr = max(round(r + mp.rate_step, 2), 0.0)
            elif d < up + dn:
                nr = max(round(r - mp.rate_step, 2), 0.0)
            dr = round(nr - r, 2)
            sec = rng.gauss(0.0, mp.sector_std_dev)
            vals[FED] = nr
            vals[AJR] = round(vals[AJR] * math.exp(mp.ajarai_drift + mp.ajarai_rate_beta * dr +
                                                   mp.ajarai_sector_beta * sec + rng.gauss(0, mp.ajarai_idio_std_dev)), 2)
            vals[THR] = round(vals[THR] * math.exp(mp.theriodic_drift + mp.theriodic_rate_beta * dr +
                                                   mp.theriodic_sector_beta * sec + rng.gauss(0, mp.theriodic_idio_std_dev)), 2)
        if option.observable_value(vals) >= option.strike:
            hits += 1
    return hits / n_paths


TC1_PARAMS = dict(
    ajarai_drift=0.001, ajarai_idio_std_dev=0.01, ajarai_rate_beta=-0.02, ajarai_sector_beta=1.0,
    rate_down_probability=0.2, rate_reversion_strength=0.1, rate_up_probability=0.25,
    sector_std_dev=0.02, theriodic_drift=0.0015, theriodic_idio_std_dev=0.012,
    theriodic_rate_beta=-0.015, theriodic_sector_beta=1.0, rate_step=0.25, rate_target=2.0,
)
TC1_STATE = {FED: 3.0, AJR: 500.0, THR: 600.0}
TC1_CASES = [  # (legs, T, strike, expected from the leaked TC1 output)
    (((FED, 1.0),), 1, 3.00, 0.7000),
    (((FED, 1.0),), 5, 3.50, 0.0471),
    (((AJR, 1.0),), 1, 500.00, 0.5309),
    (((THR, 1.0),), 10, 650.00, 0.2068),
    (((THR, 1.0), (AJR, -1.0)), 1, 0.00, 1.0000),
    (((THR, 1.0), (AJR, -1.0)), 10, 0.00, 0.9999),
]


def make_option(oid, legs, t, strike):
    return ENV.BinaryOption(
        legs=tuple(ENV.OptionLeg(underlying_id=u, weight=w) for u, w in legs),
        option_id=oid, steps_until_expiry=t, strike=strike)


def make_underlyings(vals):
    names = {FED: "FED", AJR: "AJR", THR: "THR"}
    return [ENV.Underlying(name=names[k], underlying_id=k, value=v) for k, v in vals.items()]


def theo_check(module_name):
    mod = importlib.import_module(module_name)
    mp = ENV.MarketParameters(**TC1_PARAMS)
    mm = mod.MarketMaker(make_underlyings(TC1_STATE), [], 1000.0)
    max_err = 0.0
    print(f"== THEO check for {module_name} ==")
    for i, (legs, t, k, exp) in enumerate(TC1_CASES):
        opt = make_option(i + 1, legs, t, k)
        got = mm.price_option_from_parameters(mp, opt)
        err = abs(got - exp)
        max_err = max(max_err, err)
        print(f"  case {i+1}: got={got:.4f} expected={exp:.4f} err={err:.4f}")
    print(f"  TC1 max_err={max_err:.4f}  ({'PASS' if max_err < 0.001 else 'FAIL'})")

    # random-option cross-check vs high-path Monte Carlo
    rng = random.Random(11)
    worst = 0.0
    for j in range(14):
        kind = rng.choice(["fed", "co", "co", "sp"])
        t = rng.randint(1, 12)
        if kind == "fed":
            k = round(rng.randint(4, 20) * 0.25, 2)
            legs, strike = ((FED, 1.0),), k
        elif kind == "co":
            uid = rng.choice([AJR, THR])
            v0 = TC1_STATE[uid]
            z = rng.uniform(-1.8, 1.8)
            strike = round(v0 * math.exp(z * 0.025 * math.sqrt(t)), 2)
            legs = ((uid, 1.0),)
        else:
            legs = ((THR, 1.0), (AJR, -1.0)) if rng.random() < 0.5 else ((AJR, 1.0), (THR, -1.0))
            strike = 0.0
        opt = make_option(100 + j, legs, t, strike)
        got = mm.price_option_from_parameters(mp, opt)
        ref = mc_price(mp, TC1_STATE, opt, n_paths=120000, seed=j)
        err = abs(got - ref)
        worst = max(worst, err)
        flag = " <-- LARGE" if err > 0.006 else ""
        print(f"  rand {kind} T={t:2d} K={strike:8.2f}: engine={got:.4f} mc={ref:.4f} err={err:.4f}{flag}")
    print(f"  random max_err={worst:.4f} (MC noise ~0.003)")


# ---------------------------------------------------------------------------
# session simulation
# ---------------------------------------------------------------------------
class Adapter:
    """Grader-side tracking wrapper around any MarketMaker-like object."""

    def __init__(self, mm, label, cash):
        self.mm = mm
        self.label = label
        self.cash = cash
        self.cash0 = cash
        self.pos = {}
        self.alive = True
        self.n_trades = 0
        self.errors = 0
        self.time_spent = 0.0

    def _call(self, fn, *args, default=None):
        t0 = time.perf_counter()
        try:
            out = fn(*args)
        except Exception:
            self.errors += 1
            out = default
        self.time_spent += time.perf_counter() - t0
        return out

    def get_quote(self, opt, cp):
        q = self._call(self.mm.quote, opt, cp)
        if q is None:
            return None
        try:
            bp, op = float(q.bid_price), float(q.offer_price)
            bq, oq = int(q.bid_quantity), int(q.offer_quantity)
            if not (0.0 <= bp < op <= 1.0) or bq <= 0 or oq <= 0:
                self.errors += 1
                return None
            if abs(round(bp * 100) - bp * 100) > 1e-6 or abs(round(op * 100) - op * 100) > 1e-6:
                self.errors += 1
                return None
            return (bp, bq, op, oq)
        except Exception:
            self.errors += 1
            return None

    def ask_fok(self, opt, fok):
        return bool(self._call(self.mm.respond_to_fok, opt, fok, default=False))

    def fill(self, opt, price, signed_qty, cp, true_p=None, tag=""):
        self.cash -= price * signed_qty
        self.pos[opt.option_id] = self.pos.get(opt.option_id, 0) + signed_qty
        self.n_trades += 1
        if true_p is not None:
            log = getattr(self, "fills_log", None)
            if log is None:
                self.fills_log = log = []
            log.append((tag, opt, price, signed_qty, cp, true_p))
        self._call(self.mm.on_trade, opt, price, signed_qty, cp)
        if self.cash < 0:
            self.alive = False

    def settle(self, oid, payout):
        q = self.pos.pop(oid, 0)
        if q:
            self.cash += q * payout
        if self.cash < 0:
            self.alive = False

    def pnl(self, mark):
        v = self.cash - self.cash0
        for oid, q in self.pos.items():
            v += q * mark.get(oid, 0.0)
        return v


class Bot:
    """Akuna-style competitor with access to true theo."""

    def __init__(self, kind, theo_fn, rng):
        self.kind = kind
        self.theo = theo_fn
        self.rng = rng
        self.pos = {}

    @property
    def name(self):
        return self.kind

    def quote(self, opt, cp):
        p = self.theo(opt)
        k = self.kind
        if k == "stalemate":
            return ENV.Quote(bid_price=0.01, bid_quantity=1, offer_price=0.99, offer_quantity=1)
        if k == "fw_true":
            w = 0.025
        elif k == "fw_wide":
            w = 0.06
        elif k == "lattice":
            p = round(p * 10) / 10.0
            w = 0.05
        else:  # noisy
            p = p + self.rng.gauss(0, 0.04)
            w = 0.03
        bid = max(0.0, math.floor((p - w) * 100) / 100.0)
        off = min(1.0, math.ceil((p + w) * 100) / 100.0)
        if off <= bid:
            off = min(1.0, bid + 0.01)
            if off <= bid:
                bid = off - 0.01
        return ENV.Quote(bid_price=round(bid, 2), bid_quantity=20, offer_price=round(off, 2), offer_quantity=20)

    def respond_to_fok(self, opt, fok):
        p = self.theo(opt)
        edge = (fok.price - p) if fok.order_type == ENV.OrderType.BUY else (p - fok.price)
        th = {"stalemate": 0.12, "fw_true": 0.02, "fw_wide": 0.05, "lattice": 0.04, "noisy": 0.03}[self.kind]
        if abs(self.pos.get(opt.option_id, 0)) > 150:
            return False
        return edge >= th

    def on_trade(self, opt, price, qty, cp):
        self.pos[opt.option_id] = self.pos.get(opt.option_id, 0) + qty

    def on_step_advance(self, us, os_):
        pass

    def warm_up(self, h):
        pass

    def price_option(self, opt):
        return self.theo(opt)


class Session:
    def __init__(self, seed, cfg):
        self.rng = random.Random(seed)
        self.cfg = cfg
        r = self.rng
        self.mp = ENV.MarketParameters(
            ajarai_drift=r.uniform(-0.002, 0.003),
            ajarai_idio_std_dev=r.uniform(0.005, 0.02) * cfg.get("vol", 1.0),
            ajarai_rate_beta=r.uniform(-0.05, 0.0),
            ajarai_sector_beta=r.choice([1.0, 1.0, r.uniform(0.6, 1.4)]),
            rate_down_probability=r.uniform(0.1, 0.3),
            rate_reversion_strength=r.uniform(0.0, 0.25),
            rate_up_probability=r.uniform(0.1, 0.3),
            sector_std_dev=r.uniform(0.006, 0.025) * cfg.get("vol", 1.0),
            theriodic_drift=r.uniform(-0.002, 0.003),
            theriodic_idio_std_dev=r.uniform(0.005, 0.02) * cfg.get("vol", 1.0),
            theriodic_rate_beta=r.uniform(-0.05, 0.0),
            theriodic_sector_beta=1.0,
        )
        self.values = {FED: r.choice([1.0, 1.5, 2.0, 2.5, 3.0, 3.5]),
                       AJR: round(r.uniform(200, 800), 2),
                       THR: round(r.uniform(200, 800), 2)}
        self.next_oid = 1
        self.day = 0
        self.options = []
        self.ref = ENV.MarketMaker(make_underlyings(self.values), [], 1000.0)
        self._theo_memo = {}
        n0 = cfg.get("n_options", 10)
        for _ in range(n0):
            self.options.append(self._spawn_option())

    def true_theo(self, opt):
        key = (self.day, opt.option_id, opt.steps_until_expiry)
        v = self._theo_memo.get(key)
        if v is None:
            self.ref.underlying_state = make_underlyings(self.values)
            v = self.ref.price_option_from_parameters(self.mp, opt)
            self._theo_memo[key] = v
        return v

    def _spawn_option(self):
        r = self.rng
        oid = self.next_oid
        self.next_oid += 1
        kinds = self.cfg.get("option_mix", ["fed", "co", "co", "sp"])
        kind = r.choice(kinds)
        t = r.randint(1, self.cfg.get("max_t", 12))
        if kind == "fed":
            steps = r.randint(-3, 4)
            k = max(0.25, round(self.values[FED] + steps * 0.25, 2))
            return make_option(oid, ((FED, 1.0),), t, k)
        if kind == "co":
            uid = r.choice([AJR, THR])
            z = r.uniform(-1.8, 1.8)
            k = round(self.values[uid] * math.exp(z * 0.03 * math.sqrt(t)), 2)
            return make_option(oid, ((uid, 1.0),), t, k)
        legs = ((THR, 1.0), (AJR, -1.0)) if r.random() < 0.5 else ((AJR, 1.0), (THR, -1.0))
        return make_option(oid, legs, t, 0.0)

    def gen_history(self, n_days):
        # simulate BACKWARD-consistent history ending at current values by
        # simulating forward from a start point and re-anchoring current state
        r = self.rng
        vals = dict(self.values)
        hist = {k: [v] for k, v in vals.items()}
        for _ in range(n_days - 1):
            vals = self._advance_values(vals)
            for k in hist:
                hist[k].append(vals[k])
        self.values = vals  # current = end of history
        return ENV.MarketHistory(values_by_underlying_id={k: tuple(v) for k, v in hist.items()})

    def _advance_values(self, vals):
        r = self.rng
        mp = self.mp
        cur = vals[FED]
        tilt = mp.rate_reversion_strength * (mp.rate_target - cur)
        up = min(max(mp.rate_up_probability + tilt, 0.0), 1.0)
        dn = min(max(mp.rate_down_probability - tilt, 0.0), 1.0 - up)
        d = r.random()
        nr = cur
        if d < up:
            nr = max(round(cur + mp.rate_step, 2), 0.0)
        elif d < up + dn:
            nr = max(round(cur - mp.rate_step, 2), 0.0)
        dr = round(nr - cur, 2)
        sec = r.gauss(0.0, mp.sector_std_dev)
        return {
            FED: nr,
            AJR: round(vals[AJR] * math.exp(mp.ajarai_drift + mp.ajarai_rate_beta * dr +
                                            mp.ajarai_sector_beta * sec + r.gauss(0, mp.ajarai_idio_std_dev)), 2),
            THR: round(vals[THR] * math.exp(mp.theriodic_drift + mp.theriodic_rate_beta * dr +
                                            mp.theriodic_sector_beta * sec + r.gauss(0, mp.theriodic_idio_std_dev)), 2),
        }

    def _poisson(self, lam):
        l = math.exp(-lam)
        k, p = 0, 1.0
        while True:
            p *= self.rng.random()
            if p <= l:
                return k
            k += 1

    def run(self, adapters):
        cfg = self.cfg
        r = self.rng
        hist = self.gen_history(cfg.get("n_hist", 20))
        # spawn options against post-history (current) values so strikes are live
        self.options = [self._spawn_option() for _ in range(cfg.get("n_options", 10))]
        for a in adapters:
            a.mm.underlying_state = make_underlyings(self.values)
            a.mm.active_option_state = list(self.options)
            try:
                a.mm.warm_up(hist)
            except Exception:
                a.errors += 1
        cust_kinds = cfg.get("customers", ["noise"] * 6)
        cust_bias = {}
        n_days = cfg.get("n_days", 40)
        for day in range(n_days):
            self.day = day
            alive = [a for a in adapters if a.alive]
            n_rfq = self._poisson(cfg.get("rfq_rate", 5))
            n_fok = self._poisson(cfg.get("fok_rate", 3))
            events = ["rfq"] * n_rfq + ["fok"] * n_fok
            r.shuffle(events)
            next_vals = self._advance_values(self.values)  # pre-drawn for lookahead customers
            for ev in events:
                if not self.options:
                    break
                opt = r.choice(self.options)
                ci = r.randrange(len(cust_kinds))
                ckind = cust_kinds[ci]
                cp = 101 + ci
                true_p = self.true_theo(opt)
                nxt = replace_steps(opt, max(opt.steps_until_expiry - 1, 0))
                if ckind == "noise":
                    value = true_p + r.gauss(0, 0.07)
                elif ckind == "biased":
                    b = cust_bias.setdefault((ci, opt.option_id), r.gauss(0, 0.05))
                    value = true_p + b + r.gauss(0, 0.03)
                elif ckind == "informed":
                    value = true_p
                else:  # lookahead
                    self.values, sv = next_vals, self.values
                    self.day += 1000000  # separate memo namespace
                    value = self.true_theo(nxt)
                    self.day -= 1000000
                    self.values = sv
                value = min(max(value, 0.0), 1.0)
                qty = r.randint(4, cfg.get("max_qty", 30))
                if ckind == "informed":
                    delta = r.uniform(0.015, 0.06)
                    side = None  # decided by which quote is crossable
                else:
                    delta = 0.0
                    side = r.choice(["buy", "sell"])
                if ev == "rfq":
                    self._do_rfq(alive, opt, cp, side, value, delta, qty, ckind)
                else:
                    self._do_fok(alive, opt, cp, side, value, delta, qty, ckind, r, true_p)
            # advance market
            self.values = next_vals
            new_opts = []
            for o in self.options:
                if o.steps_until_expiry <= 1:
                    payout = make_option(o.option_id, [(l.underlying_id, l.weight) for l in o.legs],
                                         0, o.strike).expiry_valuation(self.values)
                    for a in adapters:
                        a.settle(o.option_id, payout)
                else:
                    new_opts.append(replace_steps(o, o.steps_until_expiry - 1))
            while len(new_opts) < self.cfg.get("n_options", 10) and r.random() < 0.8:
                new_opts.append(self._spawn_option())
            self.options = new_opts
            us = make_underlyings(self.values)
            for a in adapters:
                t0 = time.perf_counter()
                try:
                    a.mm.on_step_advance(us, list(self.options))
                except Exception:
                    a.errors += 1
                a.time_spent += time.perf_counter() - t0
            # theo accuracy probe (module bots only)
            for a in adapters:
                if isinstance(a.mm, Bot) or not self.options:
                    continue
                for o in self.options[:4]:
                    try:
                        e = a.mm.price_option(o) - self.true_theo(o)
                        errs = getattr(a, "theo_errs", None)
                        if errs is None:
                            a.theo_errs = errs = []
                        errs.append(e * e)
                    except Exception:
                        pass
        # mark remaining
        mark = {o.option_id: self.true_theo(o) for o in self.options}
        out = {}
        for a in adapters:
            errs = getattr(a, "theo_errs", [])
            rmse = math.sqrt(sum(errs) / len(errs)) if errs else 0.0
            out[a.label] = dict(pnl=a.pnl(mark), alive=a.alive, trades=a.n_trades,
                                errors=a.errors, secs=a.time_spent, rmse=rmse)
        return out

    def _do_rfq(self, alive, opt, cp, side, value, delta, qty, ckind):
        books = []
        for a in alive:
            q = a.get_quote(opt, cp)
            if q:
                books.append((a, q))
        if not books:
            return
        if side is None:  # informed picks the profitable side
            best_off = min(b[1][2] for b in books)
            best_bid = max(b[1][0] for b in books)
            if value - best_off >= delta:
                side = "buy"
            elif best_bid - value >= delta:
                side = "sell"
            else:
                return
        tol = 0.0 if ckind in ("informed", "lookahead") else 0.10
        tp = self.true_theo(opt)
        remaining = qty
        if side == "buy":
            for a, q in sorted(books, key=lambda x: x[1][2]):
                if remaining <= 0 or q[2] > value + tol:
                    break
                if not a.alive:
                    continue
                take = min(remaining, q[3])
                a.fill(opt, q[2], -take, cp, tp, "rfq-" + ckind)
                remaining -= take
        else:
            for a, q in sorted(books, key=lambda x: -x[1][0]):
                if remaining <= 0 or q[0] < value - tol:
                    break
                if not a.alive:
                    continue
                take = min(remaining, q[1])
                a.fill(opt, q[0], take, cp, tp, "rfq-" + ckind)
                remaining -= take

    def _do_fok(self, alive, opt, cp, side, value, delta, qty, ckind, r, true_p):
        if side is None:
            side = "buy" if value >= true_p else "sell"
        if ckind == "informed":
            # informed demands edge vs true fair: accepting loses ~delta on average
            price = value - delta if side == "buy" else value + delta
        elif ckind == "lookahead":
            # priced fair vs TODAY's theo but toxic vs tomorrow's (their value)
            side = "buy" if value >= true_p else "sell"
            price = true_p + r.gauss(0, 0.015)
        else:
            price = value + r.gauss(0, 0.02)
        price = min(max(round(price, 2), 0.01), 0.99)
        ot = ENV.OrderType.BUY if side == "buy" else ENV.OrderType.SELL
        fok = ENV.FokOrder(counterparty_id=cp, option_id=opt.option_id, order_type=ot, price=price, quantity=qty)
        takers = [a for a in alive if a.ask_fok(opt, fok)]
        if not takers:
            return
        share = qty // len(takers)
        extra = qty - share * len(takers)
        tp = self.true_theo(opt)
        for i, a in enumerate(takers):
            amt = share + (1 if i < extra else 0)
            if amt <= 0 or not a.alive:
                continue
            a.fill(opt, price, -amt if side == "buy" else amt, cp, tp, "fok-" + ckind)


def replace_steps(opt, t):
    return make_option(opt.option_id, [(l.underlying_id, l.weight) for l in opt.legs], t, opt.strike)


SCENARIOS = {
    "easy_noise": dict(bots=["fw_wide", "noisy"], customers=["noise"] * 5 + ["biased"],
                       rfq_rate=6, fok_rate=3, n_days=40),
    "fw_true": dict(bots=["fw_true", "lattice"], customers=["noise"] * 4 + ["biased", "informed"],
                    rfq_rate=6, fok_rate=3, n_days=40),
    "stalemate_sparse": dict(bots=["stalemate", "fw_wide"], customers=["noise", "noise", "informed"],
                             rfq_rate=2, fok_rate=2, n_days=40),
    "toxic": dict(bots=["fw_true", "stalemate"], customers=["informed", "lookahead", "noise", "lookahead"],
                  rfq_rate=4, fok_rate=4, n_days=40),
    "high_vol": dict(bots=["fw_true", "noisy"], customers=["noise"] * 4 + ["lookahead"],
                     vol=2.0, rfq_rate=6, fok_rate=3, n_days=40),
    "rate_heavy": dict(bots=["fw_true", "lattice"], customers=["noise"] * 4 + ["informed"],
                       option_mix=["fed", "fed", "fed", "co"], rfq_rate=5, fok_rate=3, n_days=40),
    "crowded": dict(bots=["fw_true", "fw_wide", "stalemate", "lattice", "noisy"],
                    customers=["noise"] * 3 + ["biased", "informed", "lookahead"],
                    rfq_rate=8, fok_rate=4, n_days=40),
    "long_sparse": dict(bots=["stalemate", "fw_true"], customers=["noise", "informed"],
                        rfq_rate=2, fok_rate=1, n_days=80, n_hist=30),
}


def score_from_results(res):
    entries = list(res.items())
    n = len(entries)
    alive_sorted = sorted([e for e in entries if e[1]["alive"]], key=lambda e: -e[1]["pnl"])
    scores = {}
    for label, d in entries:
        if not d["alive"] or d["errors"] > 0:
            scores[label] = 0.0
        else:
            rank = next(i for i, e in enumerate(alive_sorted) if e[0] == label) + 1
            scores[label] = 0.4 + 0.6 * (n - rank) / (n - 1) if n > 1 else 1.0
    return scores


def build_session_adapters(session, module_names, bot_kinds, cash=1000.0):
    adapters = []
    for i, mn in enumerate(module_names):
        mod = importlib.import_module(mn)
        mm = mod.MarketMaker(make_underlyings(session.values), list(session.options), cash)
        adapters.append(Adapter(mm, mn, cash))
    for kind in bot_kinds:
        bot = Bot(kind, session.true_theo, random.Random(hash(kind) & 0xFFFF))
        adapters.append(Adapter(bot, kind, cash))
    return adapters


def run_battery(module_names, seeds):
    agg = {mn: dict(score=0.0, pnl=0.0, n=0, bankrupt=0, errors=0, secs=0.0, rmse=0.0) for mn in module_names}
    for scen_name, cfg in SCENARIOS.items():
        for seed in seeds:
            stable = sum(ord(c) * (i + 1) for i, c in enumerate(scen_name))
            session = Session(seed * 1000 + stable % 997, cfg)
            adapters = build_session_adapters(session, module_names, cfg["bots"])
            res = session.run(adapters)
            scores = score_from_results(res)
            line = f"  [{scen_name} seed={seed}] "
            for label, d in res.items():
                line += f"{label}: pnl={d['pnl']:+7.1f} s={scores[label]:.1f}{'!' if not d['alive'] else ''}{'E' if d['errors'] else ''}  "
            print(line)
            for mn in module_names:
                d = res[mn]
                agg[mn]["score"] += scores[mn]
                agg[mn]["pnl"] += d["pnl"]
                agg[mn]["n"] += 1
                agg[mn]["bankrupt"] += 0 if d["alive"] else 1
                agg[mn]["errors"] += d["errors"]
                agg[mn]["secs"] += d["secs"]
                agg[mn]["rmse"] += d["rmse"]
    print("\n== battery summary ==")
    for mn, d in agg.items():
        n = max(d["n"], 1)
        print(f"  {mn}: avg_score={d['score']/n:.3f} avg_pnl={d['pnl']/n:+.1f} "
              f"bankruptcies={d['bankrupt']}/{n} errors={d['errors']} avg_secs={d['secs']/n:.2f} "
              f"theo_rmse={d['rmse']/n:.4f}")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "theo"
    if mode == "theo":
        theo_check(sys.argv[2] if len(sys.argv) > 2 else "output1")
    elif mode == "run":
        mods = [sys.argv[2]]
        seeds = [int(s) for s in sys.argv[3:]] or [1, 2, 3]
        run_battery(mods, seeds)
    elif mode == "h2h":
        mods = sys.argv[2:]
        run_battery(mods, [1, 2, 3])
    elif mode == "diag":
        mn = sys.argv[2]
        scen = sys.argv[3]
        seed = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        cfg = SCENARIOS[scen]
        stable = sum(ord(c) * (i + 1) for i, c in enumerate(scen))
        session = Session(seed * 1000 + stable % 997, cfg)
        adapters = build_session_adapters(session, [mn], cfg["bots"])
        res = session.run(adapters)
        a = adapters[0]
        print(f"{mn} on {scen} seed={seed}: pnl={res[mn]['pnl']:+.1f} trades={res[mn]['trades']} rmse={res[mn]['rmse']:.4f}")
        by_tag = {}
        for tag, opt, price, q, cp, tp in getattr(a, "fills_log", []):
            kind = ("fed" if opt.legs[0].underlying_id == FED and len(opt.legs) == 1
                    else ("sp" if len(opt.legs) == 2 else "co"))
            t_b = "T<=3" if opt.steps_until_expiry <= 3 else "T>3"
            inst = (tp - price) * q  # instant edge in dollars vs true theo
            for k in (tag, "kind:" + kind, "tb:" + t_b, f"cp:{cp}"):
                d = by_tag.setdefault(k, [0.0, 0, 0])
                d[0] += inst
                d[1] += abs(q)
                d[2] += 1
        for k in sorted(by_tag):
            d = by_tag[k]
            print(f"  {k:18s} inst_edge=${d[0]:+8.2f} qty={d[1]:5d} fills={d[2]:4d}")
    elif mode == "speed":
        mn = sys.argv[2] if len(sys.argv) > 2 else "output1"
        t0 = time.time()
        session = Session(42, SCENARIOS["crowded"])
        adapters = build_session_adapters(session, [mn], SCENARIOS["crowded"]["bots"])
        res = session.run(adapters)
        print(f"total wall {time.time()-t0:.2f}s; bot compute {res[mn]['secs']:.2f}s "
              f"trades={res[mn]['trades']} errors={res[mn]['errors']}")


if __name__ == "__main__":
    main()
