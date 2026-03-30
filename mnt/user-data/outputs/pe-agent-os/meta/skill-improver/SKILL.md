---
name: skill-improver
description: "Analyzes failure logs and eval results to propose targeted improvements
to SKILL.md files. Use when: 'improve this skill', 'update the skill', 'fix the skill',
'review failures', 'skill is wrong', 'skill missed'. Do NOT use for: building new
skills from scratch, running evals, or general PE analysis."
version: 1.0.0
domain: meta
function: skill-improvement
portco-configurable: false
author: PE Agent OS
---

# Skill Improver

## Purpose
Reads failure logs and eval results for a skill, identifies the single most impactful
improvement, and proposes a minimal targeted edit to SKILL.md. Enforces the rule that
skills improve incrementally — one fix per session, based on real evidence.

## Triggers
- User says "improve this skill" / "update the skill" / "fix the skill"
- `/improve-skill` command invoked
- User pastes a failure they just logged
- After `/run-evals` reports a failure

## Workflow

### Step 1 — Load Evidence
Read in this order:
1. `[skill]/SKILL.md` — current state, current version
2. `[skill]/references/failure-log.md` — real-world failures
3. `[skill]/references/eval-results.jsonl` — last 30 entries

### Step 2 — Check Signal Threshold
Count distinct failure log entries (not counting the template header).
- If fewer than 3 entries: respond "Not enough signal yet — run the skill
  on more real scenarios before improving it" and stop.
- If 3 or more entries: continue.

### Step 3 — Identify Top Failure Pattern
Group failures by `root_cause`. Find the most frequent category.
If tied, prefer in this order:
  1. `wrong-calculation` — most dangerous in PE context
  2. `wrong-escalation` — second most dangerous
  3. `wrong-threshold` — affects quality
  4. `missing-workflow-step` — affects completeness
  5. Others alphabetically

### Step 4 — Find the Responsible Section
Trace the root cause to the exact section of SKILL.md.
Quote the specific lines that are producing the failure.

### Step 5 — Draft the Minimal Fix
Write the smallest possible change that addresses the root cause.
- For threshold fixes: change the number and one sentence of explanation
- For missing steps: add the step in the right place with full specificity
- For escalation fixes: tighten the condition or add the missing tier
- Never rewrite a whole section when a sentence fix will do
- Never add new evals to make failing evals pass — fix the skill instead

### Step 6 — Present the Diff
Show exactly:
```
CURRENT (line N):
[exact current text]

PROPOSED:
[exact replacement text]

Failure this prevents:
[quote the specific failure log entry]

Version bump: X.X.X → X.X.Y (patch) | X.Y.0 (minor) | Y.0.0 (major)
```

### Step 7 — Wait for Approval
Do not write to any file until the user explicitly approves.
If approved: apply the change, bump the version in frontmatter, add changelog entry.
If rejected: ask what direction they'd prefer instead.

## Decision Framework

**Apply the fix:** User says yes, approve, looks good, do it.

**Propose alternative:** User says "not quite" or provides more context.
  → Revise the fix based on their direction, present again.

**Do nothing:** User says no or wants to gather more data first.
  → Acknowledge and suggest running the skill more before next review.

**Stop early:** Fewer than 3 failure log entries.
  → Explicitly tell the user how many entries exist and what the threshold is.

## Rules

1. One fix per session — do not fix multiple things at once
2. Never modify eval test cases to make failing evals pass
3. Never add complexity — prefer removing ambiguity over adding steps
4. Every fix must trace to at least one logged failure
5. Always show the diff before writing — never surprise the user
6. Changelog entry is required — no silent version bumps

## Known Limitations
- Cannot assess whether a fix is PE-domain-correct — always have a domain
  expert review changes to thresholds and escalation rules
- Cannot access real deal data to validate fixes — improvement quality
  depends on how well failures were logged
