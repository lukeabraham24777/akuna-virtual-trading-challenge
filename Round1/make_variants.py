"""Generate output2 (Meridian-Prime) from output1 (Lodestar-Prime).

Both share the identical pricing engine and the grader-exact capital model
(max-loss reserve accounting, budget-based sizing, whale-FOK capture).
Meridian-Prime pins the adaptive machinery to neutral: static
uncertainty-scaled width, no counterparty logic, no markout controllers --
the fewest-moving-parts backup. Run:  python3 make_variants.py

The v1 five-bot family (tested on the hidden cases, scores 14.8-17.1/20)
is archived untouched under outputs/output{1..5}/.
"""
import re
import os
import shutil

VARIANTS = {
    "output2.py": {
        "NAME": '"Meridian"',
        "BASE_HALF": 0.015, "UNC_HALF": 0.60, "HALF_MIN": 0.02,
        "FOK_FLOOR": 0.018,
        "TIGHT_MIN": 1.0, "TIGHT_MAX": 1.0,        # spread controller disabled
        "FOKM_MIN": 1.0, "FOKM_MAX": 1.0,          # FOK controller disabled
        "SIZEM_MIN": 1.0, "SIZEM_MAX": 1.0,        # size controller disabled
        "UNCS_MIN": 1.0, "UNCS_MAX": 1.0,          # session-quality sizing disabled
        "CP_LOCK_TH": 9.0, "CP_WIDEN_TH": 9.0, "CP_TIGHT": 1.0,  # no counterparty logic
        "NUDGE": 0.0, "FADE_G": 0.0,               # no micro-price adjustments
        "DILUTE_EDGE": 9.0,                        # no dilution accepts
        "STEP_DD": 9.0,                            # no step-markout reaction
        "WIN_LO": -1.0, "WIN_HI": 2.0,             # no win-rate response
        "TOX_OVR_DAY": 9999, "TOX_OVR2_DAY": 9999, "RFQ_LOCK_DAY": 9999,
        "RSCALE_K": 0.0,
    },
}


def main():
    src = open("output1.py").read()
    for fname, overrides in VARIANTS.items():
        out = src
        for key, val in overrides.items():
            pat = re.compile(rf"^(    {key} = )([^#\n]+?)( *#.*)?$", re.M)
            m = pat.search(out)
            assert m, f"{fname}: attribute {key} not found"
            rep = f"{m.group(1)}{val}" + (m.group(3) or "")
            out = pat.sub(lambda _m: rep, out, count=1)
        open(fname, "w").write(out)
        print(f"wrote {fname} ({len(out)} bytes)")
    # mirror the deliverables into the v2 results-folder structure
    for n in (1, 2):
        d = os.path.join("outputs_v2", f"output{n}")
        os.makedirs(d, exist_ok=True)
        shutil.copyfile(f"output{n}.py", os.path.join(d, f"output{n}.py"))
        print(f"copied output{n}.py -> {d}/")


if __name__ == "__main__":
    main()
