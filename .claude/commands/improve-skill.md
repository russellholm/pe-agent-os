# /improve-skill

Run the skill improver on a skill that has accumulated failures.

## What to do

1. Read `meta/skill-improver/SKILL.md` fully
2. Ask which skill to improve if not specified
3. Read the target skill's SKILL.md
4. Read the target skill's `references/failure-log.md`
5. Read the target skill's `references/eval-results.jsonl` if it exists
6. Follow the skill-improver workflow exactly:
   - Identify the single most common root cause
   - Find the responsible section
   - Draft a minimal fix (diff format)
   - State which failure this prevents
   - Propose version bump
   - WAIT FOR APPROVAL before writing

## Usage

```
/improve-skill
```

Then specify which skill to improve (e.g., "ic-memo" or "finance-gna").

## Rules

- Never modify eval test cases to make failing evals pass
- One fix per session
- If failure log has fewer than 3 entries, say so and stop
