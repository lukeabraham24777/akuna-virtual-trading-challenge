# V4 change report — Lodestar-Prime / Meridian-Prime

Two strategy changes to `output1.py` (everything else frozen); `output2.py` and the
`outputs_v2/` mirrors regenerated via `make_variants.py`. No result `.md` files touched.

## 1. What changed (exact diff summary)

### Change 1 — capital-aware base width (`_quote_inner`)

New class attributes:

```python
CAP_WIDTH_REF = 42.0   # capital-aware width: widen when starting cash is below this
CAP_WIDTH_MAX = 1.6
```

`CAP_WIDTH_MAX` was specified as 2.2 in the task brief; it was tuned to **1.6** by the
brief's own iteration rule after the width-sanity check showed $10 halves of
0.100–0.155 at 2.2 (above the 0.05–0.12 target across 6 history seeds). Lowering the
cap (rather than `CAP_WIDTH_REF`) pulls only sub-$16.4 bankrolls back while leaving the
$20 multiplier (1.449, below the cap) and $40 (1.025) untouched.

In `_quote_inner`, the half-spread base expression became:

```python
cw = max(1.0, min(self.CAP_WIDTH_MAX, math.sqrt(self.CAP_WIDTH_REF / self._cash0)))
half = cw * self._tight * cp_mult * (self.BASE_HALF + self.UNC_HALF * unc)
```

applied before the `_def_mode == 1` widening, the capital-utilization widening, and the
`HALF_MIN`/`HALF_MAX` clamp, as specified. Multipliers: 1.60x at $10, 1.449x at $20,
1.025x at $40, 1.0x at >= $42 (scaffold's $1000 unchanged).

### Change 2 — session stop-loss (floor lock)

- `__init__`: `self._floor_lock = False`.
- `_step_advance_inner`, in the drawdown-breaker section after `mp_now` (mark-to-model
  PnL) and the toxic-session override:

```python
if self._floor_lock:
    if mp_now > -0.04 * self._cash0:
        self._floor_lock = False
elif mp_now < -0.08 * self._cash0:
    self._floor_lock = True
```

- `_quote_inner`: the skim-quote branch is now
  `if self._def_mode >= 2 or self._rfq_lock or self._floor_lock:` (0.01/0.99 skims).
- `_fok_inner`: local `dmode = 2 if self._floor_lock else self._def_mode`; the three
  uses of `self._def_mode` inside `_fok_inner` (`>= 2` gate, `== 1` requirement
  multiplier, `== 1 or locked` budget halving) all use `dmode`. A locked session
  therefore accepts only riskless (sell >= 0.995 / buy <= 0.005), fat-edge-cheap
  (edge >= 0.12, unit_cost <= 0.30, cost <= 30% of headroom), and position-reducing
  FOKs.

Both changes propagate into `output2.py` (Meridian-Prime) unchanged — `make_variants.py`
overrides do not touch `CAP_WIDTH_*` or the floor-lock logic.

## 2. Validation results (all on the final committed bytes)

### a) THEO check

`python3 sim_harness.py theo output1` and `... output2`: all six TC1 cases
err = 0.0000, **TC1 max_err = 0.0000 (PASS)** for both. Random cross-check
max_err = 0.0035 (MC noise ~0.003), same as v3.

### b) Scenario batteries (grader-true accounting)

- `run output1 1 2 3` (8 scenarios x 3 seeds = 24 sessions):
  **avg_score = 0.488, avg_pnl = +14.1, bankruptcies = 0/24, errors = 0,
  avg_secs = 0.27, theo_rmse = 0.0327, max_hard_err = 0.000**
- `run output2 1 2` (16 sessions):
  **avg_score = 0.494, avg_pnl = +10.3, bankruptcies = 0/16, errors = 0,
  avg_secs = 0.26, theo_rmse = 0.0333, max_hard_err = 0.000**

v3 baseline (git HEAD `output1.py`, same harness/seeds, run in a scratchpad copy):
avg_score = 0.475, avg_pnl = +15.6, 0/24 bankruptcies. So v4 gains a little score
in-harness (0.475 -> 0.488) and gives up ~10% of in-harness PnL — expected, since the
harness's RFQ flow is much richer than the real tests' (CLAUDE.md: use the harness for
safety proofs and A/B, not absolute score prediction; the real-test evidence is that
tight quotes starve at $10–20).

### c) Head-to-head

`h2h output1 output2` (both bots in the same 24 sessions):
**output1 avg_score = 0.569, avg_pnl = +9.9; output2 avg_score = 0.496,
avg_pnl = +5.9; both bankruptcies = 0/24, errors = 0, max_hard_err = 0.000.**

### d) Width sanity (throwaway script, not in repo)

Warmed on a 30-day synthetic history (FED grid walk ~2.0, AJR ~500, THR ~600, 2% daily
log-noise, 2dp rounding), quoting 2–6 day company options, half = (offer - bid)/2.
Representative table (seed 7; spots FED 3.75, AJR 456.01, THR 718.46):

| option           | theo  | v4 @ $10 | v4 @ $40 | v3 @ $10 | v3 @ $40 |
|------------------|-------|----------|----------|----------|----------|
| AJR 3d K~spot    | 0.481 | 0.090    | 0.060    | 0.060    | 0.060    |
| AJR 3d K=+2.5%   | 0.243 | 0.095    | 0.065    | 0.065    | 0.065    |
| AJR 6d K=-3%     | 0.702 | 0.120    | 0.080    | 0.080    | 0.080    |
| THR 2d K~spot    | 0.556 | 0.085    | 0.055    | 0.055    | 0.055    |
| THR 4d K=+3%     | 0.263 | 0.105    | 0.070    | 0.070    | 0.070    |
| THR 6d K~spot    | 0.585 | 0.125    | 0.085    | 0.075    | 0.075    |
| AJR 5d K=-1%     | 0.567 | 0.115    | 0.075    | 0.075    | 0.075    |

Across 6 history seeds x 7 options:
- **$10: 0.080–0.125, mean 0.105** (target ~0.05–0.12; only the widest 6d option
  rounds up to 0.125, i.e. exactly the Fixed-Width-0.25 half)
- $20: 0.070–0.115, mean 0.095
- **$40: 0.050–0.085, mean 0.069, 57% of quotes <= 0.07** — within one penny of v3 on
  every option (the penny comes from floor/ceil price rounding of the 1.025x factor)

With the brief's initial `CAP_WIDTH_MAX = 2.2`, $10 halves were 0.100–0.155 (mean
~0.13) on every seed — hence the tune to 1.6 and full re-validation.

### e) Edge suite (throwaway script, not in repo)

All of the following return valid values (0 <= bid < offer <= 1, whole-penny prices,
quantities >= 1) and raise nothing, on a warmed $10 bot:

| case                                  | theo   | quote                |
|---------------------------------------|--------|----------------------|
| 0-days-to-expiry (AJR K=spot)         | 1.0000 | 0.98 x2 / 1.00 x12   |
| weighted spread THR 1.5 / AJR -1, K=0 | 1.0000 | 0.97 x2 / 1.00 x12   |
| spread THR +1 / AJR -1, K=50          | 1.0000 | 0.96 x2 / 1.00 x12   |
| negative-weight leg AJR -1, K=-450    | 0.3777 | 0.28 x8 / 0.48 x4    |
| mixed FED +1 / AJR +0.01, K=8         | 0.8975 | 0.72 x3 / 1.00 x12   |

- `price_option` before `warm_up`: returns 1.0000 for the weighted spread, in [0, 1].
- BUY FOK at 0.99 x3 on the theo-0.38 option: accepted, then `on_trade(opt, 0.99, +3, cp)`
  leaves position at **-3** (unsigned-quantity auto-flip via `_fok_pend`), and `_hard`
  on the fresh $10 bot decreased by exactly **0.030000 = (1 - 0.99) * 3**.
  (A first attempt tested the FOK on a theo~1.0 option; the bot correctly *rejects*
  selling at 0.99 below fair, so no flip occurs — the flip applies to accepted FOKs.)
- Floor-lock behavioral check: forcing mark PnL to -1.0 on a $10 bot sets
  `_floor_lock = True` on the next step (with `_def_mode` still 0); locked quotes are
  0.01/0.99 skims; a modest-edge non-cheap FOK is rejected while riskless sell @ 1.00
  and fat-edge sell @ 0.90 vs theo 0.38 are still accepted; the lock holds at
  mark -0.7 (inside the -0.8/-0.4 hysteresis band) and releases at -0.2, after which
  quoting resumes two-sided.

### f) File constraints

- `wc -c`: **output1.py 57,680**, **output2.py 57,672** (mirrors identical) — both < 64,000.
- `grep -c "print("`: **0** in both.
- No new imports (`math`/`random` only, unchanged header); all six public methods keep
  their try/except shells; module-level dataclasses untouched; no use of global
  `random` state and no new randomness.
- `make_variants.py` regeneration verified: output2's diff vs its HEAD version contains
  only the v4 lines (a normalized-bytecode comparison also confirmed the final
  comment-only touch-up changed no semantics, and the re-run batteries reproduced the
  recorded numbers exactly).

## 3. Concerns

1. **CAP_WIDTH_MAX deviates from the brief's 2.2** (tuned to 1.6 under the brief's
   width-target rule). If the reviewer prefers the literal 2.2, note it puts typical
   $10 halves at 0.10–0.155, i.e. *outside* the Fixed-Width-0.25 quotes it is meant to
   undercut. 1.6 leaves the $20 multiplier untouched at sqrt(42/20) = 1.449.
2. **In-harness PnL dips ~10% vs v3** (+15.6 -> +14.1 on `run`, seeds 1-3) while score
   rises 0.475 -> 0.488. The harness's rich flow rewards tight quotes; the real
   hidden-test evidence (fixed-width bots winning $14–42 at $10–20 while we starved)
   is the driver for the change, and the harness cannot show that upside.
3. The floor lock is a deliberate profit-cap-for-loss-cap trade: a session that dips
   below -8% of cash and never recovers past -4% finishes near -8% instead of chasing
   a rebound (this is exactly the TC13 failure mode being targeted). Expiry credits do
   move the mark, so temporary reserve-driven dips can still unlock.
4. Meridian-Prime (output2) inherits both changes including the floor lock; its
   `make_variants.py` override table was not modified. If a fully static backup is
   preferred, the floor lock could be considered adaptive machinery — it is left on
   because it is a safety mechanism, not a flow controller.
5. Width-sanity numbers come from 30-day synthetic warmups; deep into a real session
   the uncertainty term shrinks, so late-session halves will sit toward the low end of
   the quoted ranges.
