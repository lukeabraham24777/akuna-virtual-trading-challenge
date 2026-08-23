# CLAUDE.md — Akuna Virtual Trading Challenge (2026)

Working notes for AI assistants (and humans) operating on this repo. Read this first;
it maps every file and distills everything we know about the competition.

## Repo map — where to look for what

| Path | What it is / when to read it |
|---|---|
| `Round1/instructions.md` | Official task statement: fill in `MarketMaker` in `trader.py`. Defines the three underlyings (FED rate, AJR, THR), binary options, RFQ vs FOK pipelines. |
| `Round1/transcript.md` | Transcript of the intro video + user notes. Key line: competitors with own ideas beyond AI-prompting are expected to win — favor competition-specific, unorthodox tactics. |
| `Round1/trader.py` | The original HackerRank scaffold: all environment dataclasses (`BinaryOption`, `MarketParameters`, `Quote`, `FokOrder`, `MarketHistory`, `Position`, `Underlying`) plus the six stubbed `MarketMaker` methods. **Changes to non-MarketMaker classes are ignored by the autograder.** |
| `Round1/discord-insights/general-page-{1,2}.json` | Raw Discrub Discord exports (~1.5MB each) of the competitor server. Don't read raw — use the extracted file below. |
| `Round1/discord-insights/messages_extracted.txt` | All 1,541 substantive messages in chronological readable form (regenerate via the snippet in "Maintenance"). This is the intel goldmine — scoring rules, per-test-case hints, opponent bot names, constraints. |
| `Round1/output1.py` … `output5.py` | **The deliverables.** Five complete, self-contained `trader.py` replacements, best-first. All share one validated engine; they differ in the policy-constant block at the top of `MarketMaker`. See "The five bots" below. |
| `Round1/make_variants.py` | Generates `output2..5` from `output1` by overriding policy constants. Edit `output1.py` + this file, rerun it — never hand-edit `output2..5`. |
| `Round1/sim_harness.py` | Local environment simulator + validation suite (not part of any submission). See "Testing" below. |

## Competition mechanics (assembled from instructions + Discord intel)

- HackerRank, 20 test cases, file must be **< 64KB**, **no `print` statements**
  (they break the custom checker: "Custom checker Failed: Success" also appears on
  time/memory-limit violations — keep `warm_up` fast). Submission deadline was Aug 23-24.
- **TC1 = "THEO" test**: calls `price_option_from_parameters` with the *true*
  `MarketParameters` and compares against exact theos (pass/fail on max error).
  A competitor leaked a full TC1 output — true params and six option theos — which we use
  as ground truth in `sim_harness.py` (`TC1_PARAMS` / `TC1_CASES`). Our engine reproduces
  all six to 4 decimal places.
- **TC2–4**: easy pass/fail sanity runs (score 1.0 each, negligible PnL).
- **TC5–20 (16 scored)**: live market-making sessions vs Akuna bots. Score per test:
  `0.4 + 0.6*(N - rank)/(N - 1)` ranked by **PnL**; **bankruptcy or a raised exception = 0**
  (confirmed pattern: last of 3 → 0.4, 2nd of 3 → 0.7, 1st → 1.0).
  So: never go bankrupt, never throw, and out-earn the best Akuna bot in each session.
- Known/likely Akuna bot archetypes (from Discord + a community arena): **Fixed Width**
  (quotes true fair ±0.025 — wins all flow if you quote wider), **Stalemate Quoter**
  (boundary quotes 0.01/0.99, skims only huge-edge FOKs; TC5–7 winners made only ~$13–23),
  **Lattice** (coarse price grid). ~6 archetypes are mixed per test ("127 combinations").
- Community experience: TC5–7 (and 8, 10, 13, 14, 18) are the hard ones. One competitor got
  TC5 from 0.4 → 1.0 by **lowering his FOK edge requirement from 2× to 1.5× theo** —
  in sparse/toxic sessions you must still capture the few good trades.
- Typical honest scores: 15–18/20; 19+ is likely overfit. Round 2 = top performers' bots
  face each other on out-of-sample cases (no code changes allowed) → generalization matters.
- `warm_up` history: daily **values** (not returns), ~20 days typical. `on_trade`
  quantity is **signed** (positive = we bought). Quotes: whole pennies, `0 ≤ bid < offer ≤ 1`.

## The market model (exact, from `trader.py` mechanics)

- FED rate: grid random walk, step 0.25, `P(up) = clamp(pu + s*(target - r))`,
  `P(down) = clamp(pd - s*(target - r), 0, 1-P(up))`, floored at 0. Defaults
  `target=2.0`, `step=0.25`.
- Company log-return per day: `drift + rate_beta*Δr + sector_beta*sector_shock + idio`,
  where the sector shock is **shared** between AJR and THR.
- Key structural facts our engine exploits:
  1. A company's T-day log return depends on the rate path **only through the total change**
     `R_T − R_0` (the per-step contributions telescope) → exact pricing = Markov-chain DP
     over rate levels × Gaussian CDF mixture. No Monte Carlo needed.
  2. For strike-0 spreads (`w_a*A + w_b*B ≥ 0`, opposite signs) the event is a **log-ratio**
     event; with equal sector betas the sector shock cancels → very low variance → these can
     be priced (and quoted) much tighter than single names.
  3. Only residual *variance* and *covariance* are identifiable (and needed) from history —
     the sector/idio split matters only for exotic strikes (quadrature fallback handles those).
- Estimation (in `warm_up`, updated online every step as new days arrive):
  rate params via grid MLE with priors; company drift/beta by ridge regression on rate
  changes with **heavy drift shrinkage** (drift estimated from ~20 points is pure noise —
  the biggest error source for long-dated options); variances/covariance from residuals.
  Per-option **uncertainty** is derived (estimation-error propagation) and drives spreads.

## Strategy architecture (shared by all five bots)

Single code path, behavior set by the policy-constant block at the top of `MarketMaker`:

- **Pricing**: exact DP/closed-form engine above; `price_option_from_parameters` uses given
  params (TC1-exact), `price_option` uses shrunk estimates.
- **Quoting**: micro-price = theo + flow-fade + FOK-price nudge + inventory & bucket skew;
  half-spread = `tight * cp_mult * (BASE_HALF + UNC_HALF * unc)`; sizes scale with cash,
  inventory side, per-underlying net exposure (asymmetric: only the risk-increasing side is
  choked), gross book, and session estimate quality. Riskless boundary quotes
  (bid 0.00 / offer 1.00) when locked down — free options if hit.
- **FOK policy**: accept when edge ≥ adaptive threshold (uncertainty- and
  counterparty-scaled); relaxed for position-reducing trades and cheap "lottery" buys
  (bounded loss); tail shorts need a price multiple of theo; hard risk checks assume full fill.
- **Adaptivity** (the load-bearing part; markouts = post-trade theo moves):
  - per-counterparty markout EWMAs → per-cp spread widening / hard lockout / tightening
    for proven-benign flow (quote() receives `counterparty_id` — price discrimination is legal);
  - RFQ vs FOK **channel-split** markout controllers (widen/lockdown quoting while still
    harvesting FOKs — this is how you beat the Stalemate Quoter at its own game);
  - win-rate controller (tighten when losing RFQs profitably, **harvest-widen** when
    winning nearly all);
  - mark-to-model drawdown circuit breaker, stricter when flow is provably adverse;
    full sit-out override for hopeless toxic sessions (rank preservation).
- **Bankruptcy shield**: cash-reserve accounting (shorts fully reserved at $1), margin
  buffer, position/exposure/gross caps. Zero bankruptcies in 100+ simulated sessions.
- All public methods are wrapped in try/except with safe fallbacks (an exception = score 0).
- Private RNG only (`random.Random`) — never touch the global `random` module state, which
  the grader's simulation uses.

## The five bots (descending confidence)

| File | Name | Profile |
|---|---|---|
| `output1.py` | **Lodestar** | Balanced adaptive flagship. Full machinery, moderate base aggression. Best head-to-head, swept the stalemate-sparse scenarios (the TC5–7 analog), top-2 everywhere else. |
| `output2.py` | **Meridian** | Same engine, adaptive machinery pinned neutral: static uncertainty-scaled width, fixed sizes, plain FOK rule, single breaker. Fewest moving parts; best solo-battery score. If the grader environment differs from our assumptions, this is the hardest to break. |
| `output3.py` | **Lodestar-R** | Robust/defensive calibration: uncertainty-heavy spreads, strict FOK bar, small book, hair-trigger defenses, extra shrinkage. Built for toxic/unknown regimes and R2 out-of-sample. |
| `output4.py` | **Lodestar-A** | Aggressive flow-capture: tighter, bigger, lower FOK bar (the Discord "1.5×" lesson), dilution accepts. Upside bet that real test flow is richer/dumber than our harness. Weakest when many sharp MMs compete. |
| `output5.py` | **Bastion** | Ultra-safe floor-maximizer: wide quotes, tiny book, high FOK bar, earliest lockdowns. Goal: never below 0.4, occasionally 1.0 when everyone else bleeds. |

Empirics (local harness, 8 scenarios × seeds; score = rank formula above):
solo batteries ≈ 0.65–0.75 avg vs oracle-informed bot mixtures; head-to-head with all five
plus bots: output1 ≈ output2 > output3 > output4 ≈ output5. Zero bankruptcies, zero
exceptions, ~0.2s compute per 40-day session, theo RMSE vs truth ≈ 0.036.

## Testing (`sim_harness.py`)

```
python3 sim_harness.py theo output1     # TC1 exact-value check + Monte Carlo cross-check
python3 sim_harness.py run output1 1 2 3    # scenario battery (8 scenarios x seeds)
python3 sim_harness.py h2h output1 ... output5   # all bots in the same sessions
python3 sim_harness.py diag output1 toxic 2      # per-fill PnL attribution for one session
python3 sim_harness.py speed output1    # timing check
```

Scenarios replicate the intel: fixed-width-true / stalemate / lattice / wide / noisy
opponents; noise / biased / informed / lookahead customers; RFQ best-price routing with
book-walking; FOK splitting among accepters; bankruptcy → dead; final PnL marked at true theo.
The `diag` mode splits instant edge (vs true theo) from inventory losses — that distinction
drove the biggest design win (inventory variance, not adverse selection, was the main bleed).

## Maintenance

- To change strategy: edit `output1.py` (and/or the override dicts in `make_variants.py`),
  run `python3 make_variants.py`, then `theo` + `run` + `h2h` before committing.
- Keep each output file under 64KB and free of `print`/new imports/global-RNG usage.
- Regenerate `messages_extracted.txt` if the raw JSONs change:
  load both JSONs, dedupe by message `id`, sort by `timestamp`, emit
  `[ts] author (replying to ...): content` lines, skip empty system messages.
- The `MarketMaker` class must stay drop-in compatible with the scaffold: same six public
  methods, no reliance on modifications to the other classes.
