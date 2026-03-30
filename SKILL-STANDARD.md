# Skill Authoring Standard

Read this before writing any SKILL.md. Every skill in this repo must follow this standard.

---

## What Makes a Good Skill

A skill is not a prompt. A skill encodes **repeatable professional judgment** — the kind an experienced operating partner or CFO would apply consistently. It should tell the agent not just what to do, but how to think about the problem, what to watch for, and when to escalate.

**Bad skill:** "Help the user write an IC memo."
**Good skill:** "When presented with a CIM or deal summary, extract the 5 key investment thesis pillars, identify the top 3 risks with mitigants, calculate entry multiple and return sensitivity at base/downside, and draft a 2-page IC memo in the firm's standard format — flagging any missing data that would block IC approval."

---

## Required Frontmatter

```yaml
---
name: skill-name                          # kebab-case, matches folder name
description: "Trigger description."       # See description rules below
version: 1.0.0                            # Semver
domain: investment-side                   # investment-side | operating-side
function: ic-memo                         # Specific function within domain
portco-configurable: true                 # true if variables change per portco
author: PE Agent OS
---
```

### Description Rules (Critical)

The description is what determines when this skill fires. Write it so Claude Code knows:
- **What it does** (verb + noun)
- **When to use it** (trigger keywords)
- **When NOT to use it** (anti-triggers)

Template: `"[What it does]. Use when: [triggers]. Do NOT use for: [anti-triggers]."`

Example:
```
"Drafts investment committee memos from CIMs, deal summaries, or financial models.
Use when: 'ic memo', 'investment committee', 'deal memo', 'write up the deal'.
Do NOT use for: board packs, LP updates, or portfolio monitoring."
```

---

## Required Sections

### 1. Purpose
2-3 sentences. What this skill does, why it exists, and what problem it solves for the PE firm.

### 2. Triggers
Bullet list. Exact phrases or situations that should activate this skill.
Include both explicit triggers ("user says X") and contextual triggers ("user uploads a CIM").

### 3. Inputs
What the skill needs to run well:
- Required inputs (skill cannot proceed without these)
- Optional inputs (improve output quality)
- Where to find them (data room, Chronograph, MCP connector)

### 4. Workflow
Numbered steps. Be specific. Include:
- What to extract/analyze/calculate at each step
- Decision points (if X then Y, else Z)
- What to do when data is missing or ambiguous

### 5. Decision Framework
The judgment layer. Answer:
- What requires human review before proceeding?
- What thresholds trigger a red flag vs. yellow flag vs. green?
- What would make an experienced operating partner stop and escalate?

### 6. Output Format
Exactly what the deliverable looks like:
- Document type (memo, spreadsheet, dashboard, email)
- Length/structure
- Link to template in `templates/` if applicable
- Formatting conventions (firm brand standards where relevant)

### 7. Portco Configuration (if portco-configurable: true)
List every variable that changes per portfolio company:
```
PORTCO_NAME: Company name
REPORTING_CADENCE: monthly | quarterly
COVENANT_THRESHOLDS: {leverage: x.xx, coverage: x.xx}
ERP_SYSTEM: NetSuite | QuickBooks | SAP | other
KPI_DEFINITIONS: {revenue: ..., ebitda: ..., nrr: ...}
```

### 8. Quality Checklist
Before delivering output, verify:
- [ ] Specific items to check for this skill type
- [ ] Data sources cited
- [ ] Human review triggered if applicable

### 9. Evals
A set of test cases the agent runs against before any skill update ships. Format:

```yaml
evals:
  - id: eval-01
    name: "Descriptive name"
    input: "Brief description of the input scenario"
    expected:
      - "Specific thing that must appear in output"
      - "Another specific verifiable claim"
    must_not:
      - "Thing that must NOT appear"
    flags_expected: red | yellow | green | none
    hitl_expected: true | false
```

Minimum 3 test cases per skill:
- **Happy path** — clean input, full data, expected output
- **Red flag case** — input that should trigger escalation
- **Missing data case** — required input absent, skill requests it gracefully

### 10. Observability
Every skill run must emit a structured log block before delivering output:

```
[SKILL RUN LOG]
skill: skill-name
version: x.x.x
timestamp: ISO-8601
portco: PORTCO_NAME (if configured)
steps_completed: [list of step names]
steps_skipped: [list with reason]
flags_raised: [red/yellow/green with description]
hitl_triggered: true/false — reason if true
memory_read: [list of artifacts/patterns referenced]
memory_written: [list of artifacts produced]
estimated_tokens: ~N
elapsed_seconds: N
output_confidence: high | medium | low
```

`output_confidence` rules:
- **high** — all required inputs present, no flags, all steps completed
- **medium** — optional inputs missing or yellow flags present
- **low** — required inputs inferred or red flags present — always triggers HITL

### 11. Human-in-the-Loop (HITL) Design
The exact handoff interface — not just "escalate to human" but the complete interaction design:

```
HITL Trigger: [exact condition]

Agent produces:
  - Summary of what was completed before stopping
  - The specific blocker (data gap, flag, threshold breach)
  - 2-3 specific options for the human (not open-ended)
  - Recommended option with rationale

Human responds with:
  - Option A: [what agent does next]
  - Option B: [what agent does next]
  - Option C: [what agent does next]

Agent resumes: [exactly what happens after human input]
Timeout behavior: [what happens if no response in X hours]
```

### 12. Memory
What the skill reads from and writes to memory:

```yaml
memory:
  reads:
    working: []        # Keys from current session
    artifacts: []      # Prior outputs to reference
    patterns: []       # Cross-portco learnings to apply
    portco_config: []  # Config variables to load
  writes:
    artifacts:
      - key: "artifact-key"
        content: "description of what is stored"
        ttl: permanent | 90d | 30d
    patterns:
      - key: "pattern-key"
        trigger: "condition under which this pattern is written"
```

### 13. Action Layer
What external system this skill writes to when fully connected. Plant the flag even if not yet built:

```yaml
actions:
  - system: NetSuite | Bullhorn | Google Sheets | Chronograph | Email
    operation: create | update | notify | export
    trigger: "condition that fires this action"
    data: "what fields/content are written"
    auth: OAuth | API key | service account
    status: planned | in-progress | live
    fallback: "what agent does if action fails"
```

---

## Optional Sections

### Python Tools
If the skill includes scripts in `scripts/`:
- List each script with a one-line description
- Show the CLI call with example arguments
- All scripts must be stdlib-only (no pip installs)

### Related Skills
Skills that chain well with this one (for orchestration).

### Known Limitations
Be honest. What can this skill NOT do reliably?

---

## Two-Layer Rule

Every operating-side skill must have two explicit layers:

**Universal layer** — Best practice for the function (how any competent CFO would approach a monthly close)

**Firm layer** — Firm-specific: your templates, your thresholds, your reporting formats, your escalation paths

Label them clearly in the skill file. The firm layer is what makes this a proprietary asset vs. a generic tool.

---

## Anti-Patterns to Avoid

| Anti-pattern | Why it's bad | Fix |
|---|---|---|
| Vague triggers | Skill fires at wrong times or never fires | Use specific keywords + anti-triggers |
| No decision framework | Agent can't distinguish routine from escalation | Add explicit thresholds and red flags |
| Hardcoded company names | Skill breaks when portco context changes | Use PORTCO_NAME variable |
| Embedded full templates | Templates go stale, can't be versioned | Reference `templates/` folder |
| External Python dependencies | Breaks in restricted environments | Stdlib only |
| Missing output format | Agent produces inconsistent deliverables | Spec exact structure + link template |
| No evals | Can't verify a skill update didn't break anything | Add minimum 3 test cases in Evals section |
| No HITL design | Escalation is vague — human doesn't know what to do | Spec exact options and resume path |
| No observability | Can't debug failures or track cost | Add run log block to every skill |
| No memory spec | Agent re-derives what it already knows | Declare reads and writes explicitly |
| Action layer absent | Skill advises but never acts | Stub action layer even if status: planned |

---

## Skill Quality Levels

Rate your skill before submitting:

**Level 1 — Draft**
Has frontmatter, basic workflow, and triggers. Untested.

**Level 2 — Functional**
Has all 13 required sections. Tested against 2+ real examples. Evals written.

**Level 3 — Production**
All 13 sections complete. Evals passing against 5+ real scenarios. Observability log emitted on every run. HITL design tested with a real user. Memory reads/writes documented. Action layer status confirmed (planned or live). Reviewed by a domain expert.

Target Level 3 for all investment-side skills. Level 2 acceptable for operating-side skills in Phases 2–4.

---

## Example: Good vs. Bad Workflow Step

**Bad:**
> 3. Analyze the financials.

**Good:**
> 3. Financial Analysis
>    - Calculate LTM revenue, EBITDA, and EBITDA margin from the provided financials
>    - Compute entry multiple at deal price (EV/EBITDA, EV/Revenue)
>    - Run return sensitivity: base case (entry multiple reversion to sector median at exit), upside (1-turn expansion), downside (1-turn compression + 10% EBITDA haircut)
>    - Flag if LTM EBITDA < $3M (below typical small PE minimum threshold) or leverage > 5.0x
>    - If financials are unaudited or >6 months old, add a data quality warning to the output
