"""Generate output2..output5 from output1 by overriding the policy block.

All five bots share the same validated pricing engine and code path; they differ
only in the calibration constants below. Run:  python3 make_variants.py
"""

VARIANTS = {
    # output4 -- aggressive flow capture: tighter, bigger, faster to take FOKs.
    # Bet: most sessions are dominated by uninformed flow and rank rewards volume.
    "output4.py": {
        "NAME": '"Lodestar-A"',
        "BASE_HALF": 0.008, "UNC_HALF": 0.60, "HALF_MAX": 0.12,
        "SIZE_BASE": 21.0, "SIZE_MAX": 60.0,
        "FOK_FLOOR": 0.009, "FOK_UNC": 0.55,
        "TIGHT_MIN": 0.45, "FOKM_MIN": 0.5,
        "DILUTE_EDGE": 0.003, "LOTTERY_PRICE": 0.06,
        "POS_CAP": 42.0, "EXP_CAP": 19.0, "GROSS_CAP": 110.0,
        "N_PRIOR": 20.0,
        "TAIL_SELL_MULT": 1.35,
        "DEF1_ADV": 0.040, "DEF2_ADV": 0.090, "DEF1_BEN": 0.075, "DEF2_BEN": 0.150,
        "RFQ_LOCK_TH": 0.024, "TOX_OVR": 0.025,
        "UNCS_MIN": 0.55, "SIZEM_MAX": 2.0, "HARVEST_CAP": 1.25,
    },
    # output3 -- robust/defensive: uncertainty-heavy spreads, strict FOK bar,
    # small book, hair-trigger defenses. Optimized for toxic/unknown regimes.
    "output3.py": {
        "NAME": '"Lodestar-R"',
        "BASE_HALF": 0.014, "UNC_HALF": 1.15, "HALF_MAX": 0.20, "HALF_MIN": 0.02,
        "SIZE_BASE": 12.0, "SIZE_MAX": 30.0,
        "FOK_FLOOR": 0.018, "FOK_UNC": 0.90, "TAIL_SELL_MULT": 1.60,
        "TIGHT_MIN": 0.70, "FOKM_MIN": 0.75,
        "DILUTE_EDGE": 0.02,
        "POS_CAP": 26.0, "EXP_CAP": 11.0, "GROSS_CAP": 55.0,
        "N_PRIOR": 32.0,
        "DEF1_ADV": 0.025, "DEF2_ADV": 0.055, "DEF1_BEN": 0.050, "DEF2_BEN": 0.100,
        "RFQ_LOCK_TH": 0.014, "RFQ_LOCK_DAY": 3, "TOX_OVR": 0.015, "TOX_OVR_DAY": 6,
        "TOX_OVR2": 0.010, "TOX_OVR2_DAY": 5,
        "RISK_MARGIN": 0.09, "UNCS_MIN": 0.40, "SIZEM_MAX": 1.4,
        "HARVEST_CAP": 1.45, "WIN_HI": 0.60,
    },
    # output2 -- simple static maker: same exact pricing engine, but all the
    # adaptive machinery pinned to neutral. Fixed uncertainty-scaled width,
    # fixed sizes, plain FOK edge rule, one drawdown breaker. Fewest moving parts.
    "output2.py": {
        "NAME": '"Meridian"',
        "BASE_HALF": 0.012, "UNC_HALF": 0.60, "HALF_MIN": 0.02, "HALF_MAX": 0.12,
        "SIZE_BASE": 18.0, "SIZE_MAX": 40.0,
        "FOK_FLOOR": 0.020, "FOK_UNC": 0.70,
        "TIGHT_MIN": 1.0, "TIGHT_MAX": 1.0,        # spread controller disabled
        "FOKM_MIN": 1.0, "FOKM_MAX": 1.0,          # FOK controller disabled
        "SIZEM_MIN": 1.0, "SIZEM_MAX": 1.0,        # size controller disabled
        "UNCS_MIN": 1.0, "UNCS_MAX": 1.0,          # session-quality sizing disabled
        "CP_LOCK_TH": 9.0, "CP_WIDEN_TH": 9.0, "CP_TIGHT": 1.0,  # no counterparty logic
        "NUDGE": 0.0, "FADE_G": 0.0,               # no micro-price adjustments
        "DILUTE_EDGE": 9.0,                        # no dilution accepts
        "STEP_DD": 9.0,                            # no step-markout reaction
        "WIN_LO": -1.0, "WIN_HI": 2.0,             # no win-rate response
        "DEF1_ADV": 0.10, "DEF2_ADV": 0.13, "DEF1_BEN": 0.10, "DEF2_BEN": 0.13,
        "TOX_OVR_DAY": 9999, "TOX_OVR2_DAY": 9999, "RFQ_LOCK_DAY": 9999,
        "RSCALE_K": 0.0,
        "POS_CAP": 38.0, "EXP_CAP": 16.0, "GROSS_CAP": 100.0,
    },
    # output5 -- ultra-safe floor-maximizer: wide quotes, tiny book, high FOK
    # bar, earliest defenses. Goal: never below 0.4, top rank when others bleed.
    "output5.py": {
        "NAME": '"Bastion"',
        "BASE_HALF": 0.030, "UNC_HALF": 1.30, "HALF_MIN": 0.03, "HALF_MAX": 0.25,
        "SIZE_BASE": 7.0, "SIZE_MAX": 16.0,
        "FOK_FLOOR": 0.035, "FOK_UNC": 1.10, "TAIL_SELL_MULT": 1.70,
        "TIGHT_MIN": 1.0, "TIGHT_MAX": 3.0,        # may widen, never tighten
        "FOKM_MIN": 1.0, "FOKM_MAX": 3.0,
        "WIN_LO": -1.0, "WIN_HI": 2.0,
        "DILUTE_EDGE": 9.0,
        "LOTTERY_PRICE": 0.04, "LOTTERY_EDGE": 0.012,
        "POS_CAP": 14.0, "EXP_CAP": 7.0, "GROSS_CAP": 30.0,
        "N_PRIOR": 35.0,
        "DEF1_ADV": 0.020, "DEF2_ADV": 0.045, "DEF1_BEN": 0.040, "DEF2_BEN": 0.080,
        "RFQ_LOCK_TH": 0.012, "RFQ_LOCK_DAY": 3, "TOX_OVR": 0.012, "TOX_OVR_DAY": 5,
        "TOX_OVR2": 0.008, "TOX_OVR2_DAY": 4,
        "RISK_MARGIN": 0.12, "UNCS_MIN": 0.35, "SIZEM_MAX": 1.1,
    },
}


def main():
    import re
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


if __name__ == "__main__":
    main()
