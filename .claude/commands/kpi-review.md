# /kpi-review

Run the Finance G&A skill for a portfolio company monthly close or KPI review.

## What to do

1. Read `operating-side/finance/SKILL.md` fully before starting
2. Ask which module to run if not specified:
   - Module 1: Monthly close support
   - Module 2: 13-week cash flow
   - Module 3: KPI dashboard
   - Module 4: Covenant monitoring
   - Module 5: Board finance package
3. Load portco config variables from `portcos/[portco-slug]/config.md` if it exists
4. Emit the observability log block first (include module name)
5. Execute the module workflow exactly as specified
6. Apply all threshold flags — escalation tiers must be respected
7. If any HITL trigger fires, stop and present the options with timeouts

## Usage

```
/kpi-review
```

Then specify: portco name, which module, and paste the source data
(P&L actuals, AR aging, debt schedule, or whatever the module needs).
