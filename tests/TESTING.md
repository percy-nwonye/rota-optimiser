# Testing

This project is still an early-stage backend prototype, so testing is kept simple on purpose.

## Scenario checks (no pytest)

I validate core scheduling rules using small repeatable “scenarios”:

- one shift per person per day
- non-overridable restrictions (e.g. cannot do nights)
- maximum consecutive night limits

Run:

```bash
python tests/run_scenarios.py
