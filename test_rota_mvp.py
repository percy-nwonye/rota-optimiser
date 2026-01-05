# test_rota_mvp.py
import unittest
from datetime import datetime, timedelta

import rota_mvp as rm


def make_cfg(
    *,
    one_shift_per_day=True,
    max_consecutive_nights=2,
    max_consecutive_long_days=3,
):
    """
    Minimal config for tests. Keep it small so tests don't depend on exports/UI.
    """
    return {
        "constraints": {
            "one_shift_per_day": one_shift_per_day,
            "max_consecutive_nights": max_consecutive_nights,
            "max_consecutive_long_days": max_consecutive_long_days,
        },
        "overrides": {
            "allow_overrides": True,
            "interactive_overrides": False,  # IMPORTANT: tests should not prompt
            "warnings_enabled": True,
            "require_warning_ack": False,
            "warning_ack_phrase": "I UNDERSTAND",
        },
        "scoring_weights": {"hours": 1.0, "nights": 15.0, "weekends": 10.0},
        "exports": {"export_folder": ".", "export_csv": False, "export_excel": False},
        "cover_suggestions": {"top_n": 3},
        "explainability": {"top_n_per_decision": 5},
        "debug": {"print_no_candidate_ranking": False},
    }


def make_demo_generator(cfg=None):
    if cfg is None:
        cfg = make_cfg()

    long_day = rm.ShiftTemplate("long", "Long Day", "08:00", "20:00", False)
    night = rm.ShiftTemplate("night", "Night", "20:00", "08:00", True)
    shifts = {"long": long_day, "night": night}

    staff = [
        rm.Staff("s1", "Amaka", "HCA", "permanent", 44, True),
        rm.Staff("s2", "James", "HCA", "permanent", 44, True),
        rm.Staff("s3", "Fatima", "HCA", "permanent", 33, False),  # cannot do nights
        rm.Staff("s4", "Daniel", "HCA", "permanent", 44, True),
        rm.Staff("s5", "Grace", "HCA", "bank", 0, False),         # cannot do nights
        rm.Staff("s6", "Uche", "HCA", "bank", 0, True),
        rm.Staff("s7", "Ife", "Senior", "permanent", 33, True),
        rm.Staff("s8", "Tunde", "Senior", "permanent", 44, True),
    ]

    # requirements not needed for most unit tests; keep empty
    requirements = []

    return rm.RotaGenerator(cfg, shifts, staff, requirements)


class TestHardBlocks(unittest.TestCase):
    def test_cannot_assign_same_shift_twice_same_date_non_overridable(self):
        gen = make_demo_generator()
        date = "2025-01-06"
        shift = gen.shift_templates["night"]

        ok1, warnings1 = gen._apply_assignment("s6", "HCA", shift, date)
        self.assertTrue(ok1)
        self.assertEqual(warnings1, [])

        ok2, warnings2 = gen._apply_assignment("s6", "HCA", shift, date)
        self.assertFalse(ok2)
        self.assertTrue(any("Already assigned to this shift (NON-OVERRIDABLE)" in w for w in warnings2))

    def test_cannot_do_nights_is_non_overridable(self):
        gen = make_demo_generator()
        date = "2025-01-06"
        night = gen.shift_templates["night"]

        ok, warnings = gen._apply_assignment("s3", "HCA", night, date)  # Fatima cannot do nights
        self.assertFalse(ok)
        self.assertTrue(any("Cannot do nights (NON-OVERRIDABLE)" in w for w in warnings))


class TestSoftWarningsAndSelection(unittest.TestCase):
    def test_double_shift_is_soft_warning_and_can_be_ignored_if_override_flag_used(self):
        # one_shift_per_day ON, so second shift same day should trigger warning unless ignored
        gen = make_demo_generator(make_cfg(one_shift_per_day=True))

        date = "2025-01-06"
        long_day = gen.shift_templates["long"]
        night = gen.shift_templates["night"]

        ok1, w1 = gen._apply_assignment("s6", "HCA", long_day, date)  # Uche long day
        self.assertTrue(ok1)
        self.assertEqual(w1, [])

        # Without ignoring, _blocked_reasons should show the double shift warning
        reasons = gen._blocked_reasons("s6", "HCA", night, date, ignore_one_shift_per_day=False)
        self.assertTrue(any("Already working that date (double shift)" in r for r in reasons))

        # If we ignore one_shift_per_day (override mode), it should allow assignment
        ok2, w2 = gen._apply_assignment(
            "s6", "HCA", night, date,
            allow_double_shift_override=True,   # <-- key
            allow_consecutive_override=False
        )
        self.assertTrue(ok2)
        # In override mode we expect no double-shift warning because we ignored that rule
        self.assertFalse(any("Already working that date (double shift)" in r for r in w2))

    def test_pick_best_candidate_returns_none_when_only_candidates_have_soft_blocks(self):
        """
        Auto-pick should return None if every candidate has at least one blocked reason.
        Soft blocks count as blocked for auto-pick (override mode handles soft warnings).
        """
        gen = make_demo_generator(make_cfg(max_consecutive_nights=2))

        # Create a situation where all HCA candidates are "blocked" by a soft rule:
        # Put all HCAs as already working on the same date so one_shift_per_day blocks everyone.
        date = "2025-01-08"
        shift = gen.shift_templates["night"]
        role = "HCA"

        # Mark every HCA as already working that date (soft warning)
        for sid, staff in gen.staff.items():
            if staff.role == role:
                gen.staff_working_on_date.setdefault(date, set()).add(sid)

        chosen = gen._pick_best_candidate(role, shift, date)
        self.assertIsNone(chosen, "Auto-pick should return None if everyone has any blocked reasons")


    def test_projected_streak_counts_from_assignments_by_date(self):
        gen = make_demo_generator(make_cfg(max_consecutive_nights=10))
        night = gen.shift_templates["night"]

        # Nights on 6th, 7th, 8th -> projected for 9th should be 4
        for d in ["2025-01-06", "2025-01-07", "2025-01-08"]:
            ok, _ = gen._apply_assignment("s6", "HCA", night, d)
            self.assertTrue(ok)

        self.assertEqual(gen._projected_night_streak("s6", "2025-01-09"), 4)


if __name__ == "__main__":
    unittest.main()
