"""
Quick scenario checks for rota_mvp.py (no pytest required).

Run from project root:
    python tests/run_scenarios.py
"""

import sys
import os
from datetime import datetime, timedelta

# 👇 THIS IS THE IMPORTANT FIX
# Add project root to Python path so rota_mvp.py can be imported
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from rota_mvp import (
    load_config,
    ShiftTemplate,
    Staff,
    Requirement,
    RotaGenerator,
    DATE_FMT,
)


def scenario_one_shift_per_day():
    """
    Same staff should not be allocated 2 shifts on the same date
    when one_shift_per_day=True.
    """
    cfg = load_config("config.json")
    cfg["constraints"]["one_shift_per_day"] = True
    cfg["overrides"]["interactive_overrides"] = False

    long_day = ShiftTemplate("long", "Long Day", "08:00", "20:00", False)
    shifts = {"long": long_day}

    staff = [
        Staff("s1", "Amaka", "HCA", "permanent", 44, True),
    ]

    d = "2025-01-06"
    requirements = [
        Requirement(d, "long", "HCA", 2),  # need 2 people, only 1 exists
    ]

    gen = RotaGenerator(cfg, shifts, staff, requirements)
    gen.generate()

    assert len(gen.assignments) == 1, f"Expected 1 assignment, got {len(gen.assignments)}"
    assert len(gen.unfilled) == 1, f"Expected 1 unfilled slot, got {len(gen.unfilled)}"


def scenario_cannot_do_nights_non_overridable():
    """
    Staff who cannot do nights must never be assigned or suggested
    for night shifts.
    """
    cfg = load_config("config.json")
    cfg["overrides"]["interactive_overrides"] = False

    night = ShiftTemplate("night", "Night", "20:00", "08:00", True)
    shifts = {"night": night}

    staff = [
        Staff("s1", "Fatima", "HCA", "permanent", 33, False),  # cannot do nights
    ]

    d = "2025-01-06"
    requirements = [
        Requirement(d, "night", "HCA", 1),
    ]

    gen = RotaGenerator(cfg, shifts, staff, requirements)
    gen.generate()

    assert len(gen.assignments) == 0, "Expected 0 assignments"
    assert len(gen.unfilled) == 1, "Expected 1 unfilled slot"

    cover = gen.suggest_cover(return_data=True)
    assert cover, "Expected cover data"
    assert cover[0]["options"] == [], "Expected NO cover options (non-overridable)"


def scenario_max_consecutive_nights():
    """
    With max_consecutive_nights=1, same staff should not be assigned
    nights on two consecutive days.
    """
    cfg = load_config("config.json")
    cfg["constraints"]["max_consecutive_nights"] = 1
    cfg["overrides"]["interactive_overrides"] = False

    night = ShiftTemplate("night", "Night", "20:00", "08:00", True)
    shifts = {"night": night}

    staff = [
        Staff("s1", "Uche", "HCA", "permanent", 44, True),
    ]

    start = datetime.strptime("2025-01-06", DATE_FMT)
    requirements = []
    for i in range(2):
        d = (start + timedelta(days=i)).strftime(DATE_FMT)
        requirements.append(Requirement(d, "night", "HCA", 1))

    gen = RotaGenerator(cfg, shifts, staff, requirements)
    gen.generate()

    assert len(gen.assignments) == 1, f"Expected 1 assignment, got {len(gen.assignments)}"
    assert len(gen.unfilled) == 1, f"Expected 1 unfilled slot, got {len(gen.unfilled)}"


def main():
    tests = [
        ("one_shift_per_day", scenario_one_shift_per_day),
        ("cannot_do_nights_non_overridable", scenario_cannot_do_nights_non_overridable),
        ("max_consecutive_nights", scenario_max_consecutive_nights),
    ]

    print("Running scenario checks...\n")
    passed = 0

    for name, fn in tests:
        try:
            fn()
            print(f"✅ PASS: {name}")
            passed += 1
        except AssertionError as e:
            print(f"❌ FAIL: {name} -> {e}")

    print(f"\nDone. {passed}/{len(tests)} passed.")


if __name__ == "__main__":
    main()
