# Failure Log — ic-memo

Every time the ic-memo skill produces output you have to manually
correct, log it here before fixing it. Three entries with the same
root cause triggers a skill update via /improve-skill.

## Root Cause Categories
- `missing-workflow-step` — skill didn't execute a step it should have
- `wrong-threshold` — flag triggered at wrong level or missed entirely
- `bad-trigger` — skill fired when it shouldn't or didn't fire when it should
- `wrong-escalation` — escalated something routine or missed a real flag
- `incomplete-output` — output missing a required section
- `wrong-calculation` — math error in return sensitivity or entry multiple
- `hallucinated-data` — agent invented numbers not in the source
- `other` — describe below

## Entry Format

```
---
date: YYYY-MM-DD
scenario: [deal name or description — no confidential names]
eval_id: [eval-01 through eval-04 if matches a test case, else "real"]
what_failed: [one sentence]
root_cause: [category from above]
section_responsible: [which SKILL.md section — Workflow Step N, Decision Framework, etc.]
fix_applied: [yes — bumped to vX.X | no — needs more data]
---
```

## Log

<!-- First entry goes here -->
