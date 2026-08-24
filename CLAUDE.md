# CLAUDE.md — Akuna Virtual Trading Challenge (2026)

Working notes for AI assistants (and humans) operating on this repo. Read this first;
it maps every file and distills everything we know about the competition.

## Repo map — where to look for what

| Path | What it is / when to read it |
|---|---|
| `Round1/instructions.md` | Official task statement **including the bankruptcy-accounting note** (max-loss debits per trade; end-of-day solvency). The single most important mechanics paragraph. |
| `Round1/transcript.md` | Intro-video transcript + user notes. Key line: competitors with own ideas beyond AI-prompting are expected to win. |
| `Round1/trader.py` | The original HackerRank scaffold (env dataclasses + six stubbed `MarketMaker` methods). Changes to non-MarketMaker classes are ignored by the autograder. |
| `Round1/discord-insights/messages_extracted.txt` | All 1,541 substantive Discord messages, chronological. Scoring rules, per-test hints, opponent names, constraints. (Raw JSON exports sit next to it.) |
| `Round1/outputs/output{1..5}/` | **v1 archive — do not edit.** The five originally submitted-style bots plus their real hidden-test results (`*_results.md`). Scores: Lodestar 17.1, Meridian 16.0, Lodestar-A 14.9 (2 bankruptcies), Lodestar-R 14.8, Bastion 14.8. |
| `Round1/output1.py` | **Lodestar-Prime** — the v2 flagship deliverable (and the dev master). Full adaptive stack on top of the grader-exact capital model. |
| `Round1/output2.py` | **Meridian-Prime** — v2 static backup: same engine + capital model, adaptive machinery pinned neutral. Generated, never hand-edited. |
| `Round1/outputs_v2/output{1,2}/` | Mirror copies of the two v2 deliverables, in the same folder layout used for test results (drop `*_results.md` files here after running the hidden tests). |
| `Round1/make_variants.py` | Regenerates `output2.py` (+ the `outputs_v2/` mirrors) from `output1.py` policy overrides. Edit `output1.py`, run this, never hand-edit `output2.py`. |
| `Round1/sim_harness.py` | Local simulator with **grader-exact accounting** + validation suite. See "Testing". |

## Competition mechanics (confirmed against real grader output)

- HackerRank, 20 tests, file **< 64KB**, **no `print`** statements, time+memory limits.
- **Test a (TC1) = THEO**: `price_option_from_parameters` vs true params, pass/fail on max
  error. The leaked TC1 output (true params + six exact theos) is baked into
  `sim_harness.py` (`TC1_PARAMS`/`TC1_CASES`); both deliverables reproduce all six to 4dp.
- **Tests b–d (TC2–4) = VERBOSE**: full credit unless you error/bankrupt. Their logs are
  gold: they reveal counterparty ids, option universes, and fills (see the archived
  `*_results.md`).
- **Tests e–t (TC5–20) = SCORED**: `0.4 + 0.6·(N−rank)/(N−1)` by PnL; bankrupt/error = 0.
  Observed: **starting capital $10 (e–i), $20 (j–o), $40 (p–t)**; sessions up to
  **70–100 days**; opponents drawn from Stalemate Quoter, Fixed Width 0.05/0.1/0.25,
  Lattice, Mongoose, Situational Unawareness (2–4 per session).
- **Bankruptcy accounting (verified to the penny against three grader logs):** every trade
  immediately debits its **maximum loss** — buys cost `price·qty`, sells cost
  `(1−price)·qty` — and the debit is **not refunded by closing trades**, only by expiry
  credits (`bought·X + sold·(1−X)` per option, always ≥ 0). Solvency is checked at end of
  day after credits. Consequences: bankruptcy is a *liquidity* event (impossible if you
  budget reserve), churn is expensive, selling high-priced options is nearly free,
  and capital recycles at expiry.

## What the real v1 results taught us (drove the v2 redesign)

1. All five v1 bots scored 0.4 on TC5/6/13; the Stalemate Quoter won TC5 with ~$34 from
   huge-edge "whale" FOKs (e.g. `buy 0.94 for 26` vs theo 0.81) that our contract-count
   position caps (sized for $1000 capital, not $10–40) auto-rejected.
2. v1's internal reserve model refunded closed shorts; the grader doesn't → the aggressive
   variant went bankrupt twice (small negatives, −0.34/−0.85). Under the harness's
   grader-true replay, v1-Lodestar itself goes bankrupt in 5/24 sessions — its real 17.1
   survived on favorable draws.
3. v1's drawdown breaker used fractions of capital ($0.6–$1.3 triggers at $10) → ordinary
   PnL noise forced near-permanent lockdown in the sessions we under-earned (TC5–10).

## The market model & pricing engine (unchanged, exact)

- FED: grid random walk with reversion tilt → exact Markov-chain DP.
- Companies: log-return `drift + β·Δr + sector + idio`; T-day return depends on the rate
  path only through `R_T − R_0` → DP × Gaussian-CDF mixture, closed form.
- Strike-0 spreads: log-ratio event, sector shock cancels → priced very tight.
- Estimation: grid-MLE rates with priors; ridge β; heavy drift shrinkage; residual
  var/cov; online re-estimation every step; per-option uncertainty drives spreads.

## v2 architecture (both deliverables)

Everything from v1 (exact engine, markout/counterparty adaptivity in Lodestar-Prime,
try/except shells, private RNG) plus the capital model:

- `_hard`: exact replica of the grader's reserve balance (per-trade max-loss debits,
  gross-leg expiry credits). Verified `max_hard_err = 0.000` across every harness session.
- All quote sizes and FOK accepts budgeted in max-loss currency; a side that cannot afford
  one contract quotes the free boundary price instead (bankruptcy impossible by
  construction — zero bankruptcies in all v2 harness runs).
- **Whale-FOK capture**: bounded-loss trades (unit max-loss ≤ 0.15) and fat-edge blocks
  (edge ≥ 0.10) bypass contract-count caps; budget fraction grows with edge (up to 0.90),
  bonus for fast-recycling short expiries; even lockdown mode accepts edge ≥ 0.12 at
  unit-cost ≤ 0.30.
- **Vol-scaled circuit breakers**: drawdown limits = max(capital fraction, k·realized
  daily-PnL vol), benign-regime variance can throttle but never force a full sit-out;
  lockdown quotes are stalemate-style 0.01/0.99 skims (reserve-cheap), not just 0.00/1.00.
- **Capital-scarcity widening**: profit per unit of reserve is `edge/(1−price)` for sells,
  so as utilization rises past 35%, quotes widen (up to HALF_MAX 0.34) — wide quotes only
  forfeit flow the budget couldn't service anyway.
- Lodestar-Prime keeps the adaptive stack (per-cp markouts/lockouts, RFQ/FOK channel
  controllers, harvest-widening to 2.6×, flow fades); Meridian-Prime pins all of it
  neutral via `make_variants.py`.

Harness comparison under identical grader-true conditions (8 scenarios × 3 seeds):
v1-Lodestar 0.342 avg score, +3.8 PnL, **5 bankruptcies**; Lodestar-Prime 0.513–0.596,
+17–18 PnL, **0 bankruptcies**; Meridian-Prime ~0.48–0.52, +12–15, 0 bankruptcies.
(Harness scores undershoot real scores: its bots are capital-unconstrained and its flow
is richer than the real tests'; use it for safety proofs and A/B comparisons, not
absolute score prediction.)

## Testing (`sim_harness.py`)

```
python3 sim_harness.py theo output1        # TC1 exact-value check + MC cross-check
python3 sim_harness.py run output1 1 2 3   # scenario battery (grader-true accounting)
python3 sim_harness.py h2h output1 output2 # both in the same sessions
python3 sim_harness.py diag output1 tc8_fw 1   # per-fill attribution for one session
python3 sim_harness.py speed output1
```

Scenarios replicate the observed tests: $10–40 capital, 40–100 days, whale FOK flow,
the real opponent roster, end-of-day solvency with max-loss debits. The summary's
`max_hard_err` asserts the bot's internal `_hard` matches the grader-side balance
exactly — keep it at 0.000.

## Maintenance

- To change strategy: edit `output1.py` (+ overrides in `make_variants.py`), run
  `python3 make_variants.py`, then `theo` + `run` + `h2h` before committing.
  The archived v1 family under `outputs/` stays untouched as the known-17.1 fallback.
- Keep files < 64KB, no `print`, no new imports, no global-RNG usage; all six public
  methods wrapped in try/except.
- The `MarketMaker` class must stay drop-in compatible with the scaffold.
