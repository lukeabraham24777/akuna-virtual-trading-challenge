# Akuna Virtual Trading Challenge — Market-Making Bots

A `MarketMaker` for Akuna Capital's 2026 Virtual Quant Trading Challenge: a HackerRank
exercise where you quote and trade binary options on three simulated underlyings against
scripted competitor bots, scored on PnL and survival across 20 hidden test sessions.

**Submission: `Round1/output5.py`** — final real hidden-test score **17.1/20**, PnL
≈ **+$203.60**, **0 bankruptcies**. See [Results](#results) below for how it got there.

## The challenge, briefly

You fill in a `MarketMaker` class (`Round1/trader.py` has the scaffold) that trades
binary options — event contracts paying 1.0 or 0.0 at expiry — on:

- **FED**: the fed funds rate
- **AJR**: AjarAI, a fictional AI research lab
- **THR**: Theriodic, a competing fictional AI research lab

Orders arrive two ways: **RFQ** (you quote a two-sided market, the exchange routes the
order to the best price) and **FOK** (fill-or-kill — you see the full order and decide
yes/no). Six exchange-facing hooks drive the bot each session: `warm_up`, `quote`,
`respond_to_fok`, `on_trade`, `on_step_advance`, plus `price_option_from_parameters` for
the pure-pricing test.

**Scoring**, reverse-engineered and verified to the penny against real grader logs:

- **Test 1 (THEO)**: pass/fail on pricing accuracy against known true parameters.
- **Tests 2–4 (VERBOSE)**: full credit for not erroring or going bankrupt; their logs
  are also the best intel available — they show real counterparty behavior and fills.
- **Tests 5–20 (SCORED)**: `0.4 + 0.6·(N−rank)/(N−1)` by end-of-session PnL among
  N competitors; **zero credit for bankruptcy or a code error**, regardless of PnL.
- **Bankruptcy** is a cash-reserve rule, not a PnL rule: every trade immediately debits
  its *maximum possible loss* (`price·qty` to buy, `(1−price)·qty` to sell) from a
  reserve balance that's separate from your own bookkeeping. That debit is only repaid
  by expiry payouts, not by closing the position early. Solvency is checked at the end
  of each day; go negative and the session ends immediately at zero credit. This makes
  bankruptcy fundamentally a *liquidity* problem — avoidable by budgeting against the
  reserve, not just by having a good pricing model.
- Per Akuna's own intro video, this is a **two-stage competition**: "the top competitors
  will then face off directly to determine the winners." No specific cutoff score was
  ever published — despite constant speculation in the competition's Discord, nobody,
  including the organizers of the (unofficial, fan-run) live-testing arena, actually
  knows the bar.

## Approach

Both strategies here share one exact pricing engine and differ only in how aggressively
they adapt in-session:

- **The FED rate** follows a grid random walk with a reversion tilt — small enough state
  space to solve exactly with a Markov-chain DP instead of approximating it.
- **Company returns** (AJR, THR) are `drift + β·Δrate + sector_shock + idiosyncratic`;
  because a T-day return only depends on the rate path through its net displacement, the
  T-day distribution collapses to a DP-weighted mixture of Gaussian CDFs — closed form,
  no Monte Carlo needed.
- **Spread options** (AJR vs. THR) are a log-ratio event where the shared sector shock
  cancels out, so they price tighter than either leg alone.
- Market parameters are estimated online from the warm-up history and each session's
  fills (grid-MLE on rates, ridge-shrunk drift/beta), with per-option uncertainty feeding
  directly into how wide each quote needs to be.
- On top of the pricing engine sits a **capital model**: an exact in-bot replica of the
  grader's reserve balance, so every quote size and FOK accept is budgeted in real
  max-loss currency rather than contract count. A side that can't afford one contract
  quotes the risk-free boundary price (0.00/1.00) instead of going silent — this is what
  makes bankruptcy structurally avoidable rather than something to detect after the fact.

**Lodestar** (`output1.py`) is the adaptive variant: per-counterparty markout tracking
and exposure ladders, volatility-scaled circuit breakers, and whale-FOK capture logic
that lets deeply-mispriced bounded-loss trades bypass normal position caps.
**Meridian** (`output2.py`) runs the identical engine and capital model with all of that
adaptive machinery pinned neutral — same brain, no reflexes.

## Results

Five iterations were built and measured against real hidden-test output, not just local
simulation. Two independent lessons drove the final call:

1. The original (v1) risk model refunded closed positions the way you'd naively expect;
   the real grader doesn't. Under the corrected accounting, v1-Lodestar's 17.1 survived
   on favorable session draws — replayed on fresh sessions it goes bankrupt **5 times out
   of 16**.
2. Layering the adaptive stack on top of the corrected capital model *hurt*: v3-Lodestar
   scored 15.4 against v3-Meridian's 16.8 running the exact same engine — the adaptivity
   had been tuned against patterns that didn't generalize.

The shipped bot (**v5**) is v1-Lodestar's original, highest-scoring trading logic with a
pure veto layer bolted on: a grader-exact replica of the reserve balance that blocks any
FOK accept or quote size the reserve can't actually afford. Nothing else changes.

| Version | Score /20 | PnL | Bankruptcy-proof? |
|---|---|---|---|
| **v5 — Lodestar + solvency governor (submitted)** | **17.1** | **+$203.60** | **yes** |
| v1 — Lodestar (original) | 17.1 | +$204.15 | no — 5/16 on fresh sessions |
| v3 — Meridian | 16.8 | +$150.23 | yes |
| v2 — Meridian / v2 — Lodestar | 16.4 / 16.2 | +$114 / +$185 | yes |
| v1 — Meridian (original) | 16.0 | +$174 | no |
| v4 — Meridian / v3–v4 — Lodestar | 15.8 / 15.4 | — | yes |

v5 reproduces v1's score on **every single one of the 20 real tests**, with PnL within
55 cents (three penny-level clips from the governor capping a couple of oversized fills)
— for zero bankruptcy exposure on the fresh sessions Round 2 would actually run. Full
per-test breakdowns are in [`Round1/outputs_v2/RESULTS_MATRIX.md`](Round1/outputs_v2/RESULTS_MATRIX.md).

**Further validation:** the same relative ranking — Meridian's static, capital-model-only
approach outperforming heavier adaptivity, and the governed bot trading a bit of peak
score for zero downside — reproduced independently in a fan-run community live-testing
arena (`arena_client.py`, not Akuna infrastructure), where Meridian-v3 topped the
cumulative standings across dozens of live matches against other competitors' bots.

## Repo map

| Path | What's there |
|---|---|
| `CLAUDE.md` | Detailed working notes: mechanics, full version history, testing commands |
| `Round1/instructions.md` | Official task statement, including the bankruptcy rule |
| `Round1/transcript.md` | Intro-video transcript |
| `Round1/trader.py` | The unmodified HackerRank scaffold (data classes + stubbed `MarketMaker`) |
| `Round1/output1.py` | **Lodestar** — adaptive strategy, current dev master |
| `Round1/output2.py` | **Meridian** — static strategy, generated from `output1.py` |
| `Round1/output5.py` | **The submitted bot** — v1-Lodestar + solvency governor |
| `Round1/make_variants.py` | Regenerates `output2.py` from `output1.py`'s policy overrides |
| `Round1/sim_harness.py` | Local simulator with grader-exact accounting + a validation suite |
| `Round1/outputs/output{1..5}/` | Archived first-generation strategies + their real hidden-test logs |
| `Round1/outputs_v2/` | Later-version mirrors, real-test result records, `RESULTS_MATRIX.md` |
| `Round1/discord-insights/` | Scraped competition Discord — scoring rules, opponent behavior, fills |

> **Naming note:** `outputs/output1` … `outputs/output5` are five *different early
> strategies* (Lodestar, Meridian, and three others), not five versions of one bot.
> Separately, "v1" … "v5" throughout this README and `CLAUDE.md` track the *iteration
> history* of the two strategies that survived — Lodestar and Meridian. `output5.py` at
> the repo root is v5 of Lodestar, not a sixth original strategy.

## Running it locally

```bash
cd Round1
python3 sim_harness.py theo output1          # pricing-engine check against known-true params
python3 sim_harness.py run output1 1 2 3     # scenario battery, grader-exact accounting
python3 sim_harness.py h2h output1 output2   # head-to-head, same sessions
python3 sim_harness.py diag output1 tc8_fw 1 # per-fill PnL attribution for one session
python3 sim_harness.py speed output1         # timing check
```

The harness's own bots and customer flow are richer than the real hidden tests (it's
built for safety proofs and A/B comparisons, not for predicting an exact score), but its
capital-reserve accounting is verified to the penny against real grader logs — the
`max_hard_err` it reports should always read `0.000`.

## Constraints this code respects

HackerRank enforces: file size under 64KB, no `print` statements, no new imports beyond
the standard library, time and memory limits, and no reliance on the global `random`
module (each bot keeps its own private RNG instance). All six exchange-facing methods
are wrapped in `try`/`except` so a single bad step can't crash the whole session.
