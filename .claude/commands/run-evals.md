# /run-evals

Run the eval suite for a skill and report pass/fail results.

## What to do

1. Ask which skill to evaluate if not specified
2. Read the target skill's SKILL.md — extract all eval test cases from the Evals section
3. For each eval test case:
   a. Present the input scenario to yourself
   b. Execute the skill workflow against that input (simulate it fully)
   c. Score the output against `expected` items — each must appear
   d. Check `must_not` items — none must appear
   e. Verify `flags_expected` matches what you raised
   f. Verify `hitl_expected` matches whether you triggered HITL
   g. Record PASS or FAIL with specific reason
4. Produce a summary table:
   ```
   Eval ID | Name | Result | Failures
   --------|------|--------|----------
   eval-01 | Clean deal | PASS | —
   eval-02 | Red flag | FAIL | expected "customer concentration" not found
   ```
5. Append results to `references/eval-results.jsonl`
6. If any eval fails, recommend running `/improve-skill`

## Usage

```
/run-evals
```

Then specify the skill name.
