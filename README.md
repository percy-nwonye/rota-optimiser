# Rota Optimiser (MVP)

This is a backend project exploring how rota decisions in care homes can be made more transparent, fair, and explainable using code.

I currently work in the care sector and built this after seeing how rota planning often involves a mix of software, spreadsheets, experience, and last-minute judgement, especially when staff wellbeing, fairness, and operational pressure collide.

This project is **not a replacement for existing rota systems**.  
It focuses on the **decision logic behind the rota**, rather than the surrounding HR or payroll workflow.

---

## Why This Exists

Many care homes already use established rota and workforce management systems. These tools are strong at things like compliance, payroll integration, staff communication, and day-to-day operations.

However, even with these systems in place, managers often still find themselves asking questions like:
- Why is this shift unfilled?
- Why does the same person keep getting nights or weekends?
- Who is actually the fairest next option?
- What rule am I breaking if I override this decision?

In practice, these questions are often answered informally — using experience, spreadsheets, or memory.

This project exists to explore whether rota decisions can be:
- More **explainable**
- More **consistent**
- Easier to **justify and review**
- Adjustable without hiding the trade-offs

The aim is not automation for its own sake, but **decision support**.

---

## What This Project Focuses On

Instead of building a full rota platform, this MVP focuses on:

- The logic used to select staff for shifts
- Making constraints visible rather than implicit
- Showing *why* a decision was made or blocked
- Supporting human judgement rather than replacing it

Think of it as a **rota decision engine**, not a complete scheduling system.

---

## What the Script Does

At a high level, the engine:

1. Reads shift requirements and staff roles  
2. Scores eligible staff based on fairness factors  
3. Applies configurable constraints (e.g. consecutive nights)  
4. Assigns the most suitable available candidate  
5. Flags unfilled shifts with clear reasons  
6. Suggests alternative cover options and explains what blocks them  
7. Exports results for review  

---

## Key Features

- Automatic rota generation (backend logic)
- Fairness tracking for:
  - Total hours
  - Night shifts
  - Weekend shifts
- Configurable rules via `config.json`
- Enforcement of:
  - Maximum consecutive night shifts
  - Maximum consecutive long days
  - One shift per person per day
- Optional override warnings (configurable)
- Detection of unfilled shifts with explanations
- Cover suggestions ranked by fairness impact
- CSV and Excel exports for review

---

## Configuration

Most behaviour is controlled through `config.json`, allowing rules to be changed without modifying code.

Example (simplified):

```json
{
  "constraints": {
    "one_shift_per_day": true,
    "max_consecutive_nights": 2,
    "max_consecutive_long_days": 3
  },
  "overrides": {
    "warnings_enabled": true
  }
}
```

---

## Outputs

When run, the script generates:

- `rota_assignments.csv` – generated rota
- `rota_fairness.csv` – fairness breakdown per staff member
- `rota_unfilled.csv` – unfilled shifts with explanations
- `rota.xlsx` – combined Excel export (if enabled)

Generated files are excluded from version control.




## How to Run

### Requirements
- Python 3.10+
- `openpyxl` (for Excel export)

Install dependency:
```bash
pip install openpyxl
```
Run the script:
```bash
python rota_mvp.py
```


## Current Status

This is an early-stage backend prototype.

It does not yet include:
- A user interface
- Live data imports
- Payroll or HR integrations

The focus at this stage is the decision logic, not polish.

---

## Licence

MIT License
