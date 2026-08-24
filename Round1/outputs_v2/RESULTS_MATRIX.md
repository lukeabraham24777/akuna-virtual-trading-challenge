# Full version × strategy matrix — real hidden-test results

All 20-test totals from actual HackerRank runs (sessions are near-deterministic, so
per-test comparisons across versions are meaningful). Zero bankruptcies in every
v2/v3/v4 run; v1-Lodestar-A (the old aggressive variant) was the only bankruptcy case.

| Version | Lodestar (adaptive, output1) | Meridian (static, output2) |
|---|---|---|
| v1 (original caps, old reserve model) | **17.1** (+$204) | 16.0 (+$174) |
| v2 (capital model, whale capture) | 16.2 (+$185) | 16.4 (+$114) |
| v3 (+ counterparty FOK ladder) | 15.4 (+$148) | **16.8** (+$150) |
| v4 (+ capital-aware width, stop-loss) | 15.4 (+$138) | 15.8 (+$142) |

## Per-test scores (scored tests e–t)

| Test | v1-L | v3-L | v4-L | v2-M | v3-M | v4-M |
|---|---|---|---|---|---|---|
| e | 0.4 | 0.4 | 0.4 | 0.4 | 0.4 | 0.4 |
| f | 0.4 | 0.4 | 0.4 | 0.4 | 0.4 | 0.4 |
| g | 1.0 | 1.0 | 0.4 | 0.4 | 1.0 | 1.0 |
| h | 0.7 | 0.7 | 0.7 | 0.7 | 0.7 | 0.4 |
| i | 0.7 | 1.0 | 1.0 | 0.7 | 1.0 | 1.0 |
| j | 0.7 | 0.7 | 0.7 | 0.7 | 0.7 | 0.7 |
| k | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| l | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| m | 0.4 | 0.4 | 0.4 | 0.4 | 0.6 | 0.4 |
| n | 1.0 | 0.4 | 0.4 | 0.7 | 1.0 | 0.7 |
| o | 1.0 | 0.4 | 1.0 | 1.0 | 1.0 | 1.0 |
| p | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| q | 1.0 | 0.6 | 0.6 | 1.0 | 0.6 | 0.6 |
| r | 0.8 | 0.6 | 0.6 | 0.6 | 0.6 | 0.6 |
| s | 1.0 | 0.8 | 0.8 | 0.6 | 0.8 | 0.6 |
| t | 1.0 | 1.0 | 1.0 | 0.8 | 1.0 | 1.0 |
| **Σ** | **13.1** | 11.4 | 11.4 | 12.0 | **12.8** | 11.8 |

## What the matrix proves

1. **v1-Lodestar (17.1) stays champion.** Its edge is concentrated in the late $40
   tests q/r/s (+$16.5/+$4.6/+$23.0 where every capital-model bot goes flat/negative)
   — the old tight-caps posture is accidentally optimal against the hard late flow.
2. **v3-Meridian (16.8) is the best of the new family**: the capital model + whale
   capture + counterparty ladder with NO adaptive machinery. It flips i and m and
   wins n/o/t, but can't match v1-L's late-test earnings.
3. **The adaptive stack now hurts** (v3-L 15.4 vs v3-M 16.8): the markout throttles /
   locks that helped v1's tiny-cap world suppress earnings in n/o/q under the
   capital model. Opposite of v1, where Lodestar beat Meridian by +1.1.
4. **v4's capital-aware width overshoots**: it flipped g back to a loss (quoting
   outside Fixed Width 0.25 at $10) and cost v4-M h/m/s vs v3-M. The stop-loss
   didn't add score anywhere it was needed (the q/r gaps are under-earning, not
   over-losing).
5. e/f/h/j remain owned by Stalemate ($36–38 whale food) and Fixed Width 0.1
   ($27–39) across all six variants — structurally out of reach at $10–20 capital.

## Submission decision (Round 1 deadline 2026-08-24 12:00 UTC)

- **Primary: v1-Lodestar** (`outputs/output1/output1.py`) — highest tested score
  (17.1), and it survived all 16 real sessions including the 70/100-day ones. Known
  residual risk: under fresh out-of-sample sessions (Round 2), its outdated reserve
  model carries genuine bankruptcy exposure (5/24 in grader-true harness replays).
- **Runner-up: v3-Meridian** (`akuna_v3_meridian_output2.py` / commit e7d5431's
  output2.py) — 16.8, bankruptcy-impossible by construction; the pick if Round-2
  robustness is weighted over 0.3 of Round-1 score.
