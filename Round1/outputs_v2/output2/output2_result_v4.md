# v4 Meridian-Prime-2 — real hidden-test results (from HackerRank testcase_message API)

**Total: 16.8/20** (scored e–t: 12.8/16) · **Total PnL ≈ +$150.23** · **0 bankruptcies**
Run collected 2026-08-24 via the submission-detail network response (all 20 outputs in one
`testcase_message` array). Behavioral signatures (whale FOK accepts, $10-capital wide
quotes, test-m positive, test-t loss capped) confirm this is the v4 build (commit aae3517).

| Test | Score | Ranking (PnL) |
|---|---|---|
| a (THEO) | PASS | max_error=0.0000 |
| b | 1.00 | 1. Meridian $0.1 · 2. Stalemate $0.0 (cash 10.1 / start 10) |
| c | 1.00 | 1. Meridian $0.81 · 2. Stalemate $0.0 · 3. FW 0.1 $0.0 (cash 20.81 / 20) |
| d | 1.00 | 1. FW 0.05 $2.9 · 2. Mongoose $0.3 · 3. Meridian $-5.32 (cash 34.68 / 40) |
| e | 0.40 | 1. Stalemate $38.0 · 2. Meridian $1.6 (11.6 / 10) |
| f | 0.40 | 1. FW 0.25 $14.33 · 2. Stalemate $0.0 · 3. Meridian $-2.57 (7.43 / 10) |
| g | **1.00** | 1. **Meridian $16.19** · 2. FW 0.25 $9.37 (26.19 / 10) — capital-aware width win |
| h | 0.70 | 1. FW 0.1 $32.04 · 2. Meridian $1.8 · 3. Stalemate $0.0 (11.8 / 10) |
| i | 1.00 | 1. **Meridian $31.62** · 2. FW 0.1 $8.72 · 3. FW 0.25 $0.0 (41.62 / 10) |
| j | 0.70 | 1. FW 0.1 $36.66 · 2. Meridian $4.32 · 3. Stalemate $4.0 (24.32 / 20) |
| k | 1.00 | 1. **Meridian $39.1** · 2. FW 0.1 $0.18 · 3. FW 0.05 $-32.92 (59.1 / 20) |
| l | 1.00 | 1. **Meridian $11.6** · 2. FW 0.05 $-23.52 (31.6 / 20) |
| m | **0.60** | 1. Lattice $9.6 · 2. FW 0.1 $9.09 · 3. **Meridian $6.94** · 4. SU $2.35 (26.94 / 20) — first positive m ever |
| n | 1.00 | 1. **Meridian $16.65** · 2. Lattice $12.61 · 3. FW 0.05 $-15.79 (36.65 / 20) |
| o | 1.00 | 1. **Meridian $5.71** · 2. SU $1.56 · 3. Lattice $0.72 (25.71 / 20) |
| p | 1.00 | 1. **Meridian $43.82** · 2. Lattice $3.1 · 3. FW 0.05 $-0.94 (83.82 / 40) |
| q | 0.60 | 1. SU $8.99 · 2. Lattice $8.35 · 3. Meridian $7.99 · 4. Mongoose $-11.76 (47.99 / 40) — lost 1st by $1 |
| r | 0.60 | 1. FW 0.05 $29.14 · 2. Lattice $5.09 · 3. Meridian $-6.95 · 4. Mongoose $-27.26 (33.05 / 40) |
| s | 0.80 | 1. SU $15.79 · 2. Meridian $-9.85 · 3. Mongoose $-13.0 · 4. FW 0.05 $-35.21 (30.15 / 40) |
| t | **1.00** | 1. **Meridian $-13.33** · 2. Lattice $-15.6 · 3. Mongoose $-32.69 · 4. FW 0.05 $-122.26 (26.67 / 40) — bloodbath won by losing least |

## Version comparison (real hidden tests)

| Version | Score | PnL | Bankruptcies |
|---|---|---|---|
| v1 Lodestar | **17.1** | ≈ +$204 | 0 |
| **v4 Meridian-Prime-2** | **16.8** | ≈ +$150 | 0 |
| v2 Meridian-Prime | 16.4 | ≈ +$114 | 0 |
| v2 Lodestar-Prime | 16.2 | ≈ +$185 | 0 |
| v1 Meridian | 16.0 | ≈ +$174 | 0 |

## v4 mechanisms visibly working (vs earlier Meridians)

- g: 0.4 → 1.0 — capital-aware width beat Fixed Width 0.25 on $10 ($16.19 vs $9.37).
- m: 0.4 → 0.6 — positive PnL (+$6.94) for the first time in any variant.
- r: 0.4 → 0.6, s: 0.6 → 0.8, t: 0.8 → 1.0 — stop-loss floor caps the late-test bleed
  (t: −$13.33 vs v2's −$23.55, and least-negative wins the session).
- Regression: q 1.0 → 0.6 (three bots within $1 at the top; variance-level loss).
- Verbose d: the 26-lot whale FOK @0.94 and 17-lot @0.78 accepted (both expired ITM
  this session, −$5.32 — bounded, +EV trades with unlucky settlement).

Still open: e/f/h/j remain owned by Stalemate ($38 whale food on $10 capital) and
Fixed Width 0.1 ($32–37). v4 Lodestar (output1) untested on the real cases at time of writing.
