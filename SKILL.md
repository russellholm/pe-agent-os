---
name: ic-memo
description: "Drafts investment committee memos from CIMs, deal summaries, financial models, or management presentations. Use when: 'ic memo', 'investment committee', 'deal memo', 'write up the deal', 'draft the memo', user uploads a CIM or deal file. Do NOT use for: board packs, LP updates, portfolio monitoring, or exit materials."
version: 2.0.0
domain: investment-side
function: ic-memo
portco-configurable: false
author: PE Agent OS
changelog:
  - 1.0.0: Initial version — workflow, decision framework, output format
  - 2.0.0: Added evals (4 test cases), observability log, HITL design (2 triggers),
            memory spec, action layer stubs
---

# IC Memo

## Purpose
Drafts a standard 2-page investment committee memo from deal materials. Extracts thesis, risks, and returns from raw inputs (CIM, financials, management deck) and formats them into a memo ready for IC review — flagging any gaps that would block approval.

## Triggers
- User says "write the IC memo", "draft the memo", "IC write-up"
- User uploads or references a CIM, deal summary, or management presentation
- User provides company financials and asks for a deal analysis
- `/ic-memo` command invoked

## Inputs

**Required (memo cannot proceed without these):**
- Company name and brief description
- LTM financials (revenue, EBITDA minimum)
- Deal structure (enterprise value or equity check)

**Optional (improve output quality):**
- Full CIM or information memorandum
- Historical financials (3 years preferred)
- Management presentation
- Comparable transactions or public comps
- Customer concentration data
- Debt structure / cap table

**MCP Sources:**
- PitchBook: sector comps, transaction multiples, comparable deals
- S&P Global / FactSet: public company benchmarks, leverage data

## Workflow

### Step 1 — Company Overview
Extract or ask for:
- Business description (1-2 sentences: what they do, who they sell to, how they make money)
- Founded, HQ, employee count
- Ownership history (founder-owned, sponsor-backed, corporate carve-out)
- Why it's for sale

### Step 2 — Investment Thesis
Identify the top 3-5 reasons the firm should own this business:
- Recurring revenue / defensible customer relationships
- Margin expansion opportunity
- Operational improvement levers (G&A rationalization, pricing, procurement)
- Platform/add-on potential
- Industry tailwinds

If thesis pillars are not obvious from materials, explicitly note: "Thesis requires validation in diligence."

### Step 3 — Financial Analysis
Calculate from provided financials:
- LTM Revenue, EBITDA, EBITDA margin
- 3-year revenue CAGR (if historical data available)
- Entry multiple: EV/LTM EBITDA, EV/LTM Revenue
- Return sensitivity (see model below)

**Return Sensitivity Model:**
| Scenario | Assumption | Return |
|----------|-----------|--------|
| Base | Exit at entry multiple, 3% EBITDA CAGR | Calculate MOIC + IRR |
| Upside | 1-turn multiple expansion, 8% EBITDA CAGR | Calculate MOIC + IRR |
| Downside | 1-turn compression, -10% EBITDA haircut | Calculate MOIC + IRR |

**Threshold Flags:**
- 🔴 LTM EBITDA < $3M → Flag: below typical small PE minimum size
- 🔴 Entry EV/EBITDA > 10x → Flag: rich valuation, requires strong thesis
- 🟡 Revenue CAGR < 5% → Flag: low growth, value creation depends on margin improvement
- 🟡 EBITDA margin < 15% → Flag: below sector average, margin expansion required
- 🟢 Revenue CAGR > 10% + EBITDA margin > 20% → Strong fundamental profile

### Step 4 — Risk Assessment
Identify top 3 risks with mitigants:

For each risk:
- **Risk:** Specific, concrete description
- **Severity:** High / Medium / Low
- **Mitigant:** What protects the firm if this risk materializes
- **Diligence question:** What needs to be confirmed to de-risk this

Common risks to check for:
- Customer concentration (top customer > 20% of revenue = 🔴)
- Key person dependency
- Technology/product obsolescence
- Competitive dynamics
- Regulatory exposure
- Integration risk (if platform deal)

### Step 5 — Value Creation Plan
List the 3-5 EBITDA levers the firm would pull:
- G&A rationalization (agent OS deployment)
- Pricing optimization
- Sales force effectiveness
- Procurement / vendor consolidation
- Add-on acquisitions

Estimate EBITDA impact where possible (even rough: "50-100bps margin improvement from G&A rationalization").

### Step 6 — Structure & Terms
Summarize:
- Enterprise value / equity check
- Debt structure (leverage, pricing, lender)
- Management rollover (%)
- Key deal terms or conditions

If not provided, note as "TBD — requires term sheet."

### Step 7 — Gap Flags
Before finalizing, explicitly list any missing information that would block IC approval:
- Missing diligence items
- Unverified financial data
- Open structuring questions
- Management team gaps

## Decision Framework

**Proceed to full memo:** All required inputs available, no 🔴 flags, or 🔴 flags have documented mitigants.

**Request more information:** Missing financials, customer data, or deal structure. Tell user exactly what's needed.

**Flag for human review:**
- Entry multiple > 10x EV/EBITDA
- Customer concentration > 30% in top customer
- Declining revenue (negative CAGR)
- EBITDA < $2M
- Any regulatory or litigation exposure mentioned in materials

**Do not draft memo if:**
- No financial data provided (offer to draft a preliminary one-pager instead)
- Obvious conflicts of interest or ethical concerns in deal materials

## Output Format

**2-page IC memo in firm format:**

```
INVESTMENT COMMITTEE MEMO
[Company Name] | [Date] | CONFIDENTIAL

EXECUTIVE SUMMARY
[3 sentences: company, opportunity, recommendation]

COMPANY OVERVIEW
[Business description, ownership, why selling]

INVESTMENT THESIS
[3-5 bullet points with sub-bullets]

FINANCIAL SUMMARY
[Table: Revenue, EBITDA, Margin — LTM + 2 historicals]
[Return sensitivity table]

RISK FACTORS
[3 risks, each with severity + mitigant + diligence question]

VALUE CREATION PLAN
[3-5 EBITDA levers with estimated impact]

DEAL STRUCTURE
[EV, equity check, leverage, management rollover]

OPEN ITEMS / DILIGENCE PRIORITIES
[Numbered list of what needs to be confirmed before IC]

RECOMMENDATION: [PROCEED TO DILIGENCE | PASS | ADDITIONAL INFO REQUIRED]
```

See `templates/ic-memo-template.md` for the full formatted version.

## Quality Checklist
Before delivering:
- [ ] All three required inputs present
- [ ] Return sensitivity calculated (not estimated verbally)
- [ ] Top 3 risks each have a named mitigant
- [ ] All 🔴 flags surfaced explicitly
- [ ] Open items section populated
- [ ] Recommendation stated explicitly

## Related Skills
- `due-diligence` — follows IC memo approval
- `board-pack` — uses IC memo thesis as source material
- `exit-readiness` — builds on original investment thesis

## Known Limitations
- Cannot calculate IRR without knowing hold period assumption (default: 5 years)
- Cannot verify customer concentration without customer-level revenue data
- Management quality assessment requires reference calls — always flag as open item

---

## Evals

```yaml
evals:
  - id: eval-01
    name: "Clean deal — full data available"
    input: >
      B2B SaaS company, $8M LTM revenue, $2.5M LTM EBITDA (31% margin),
      15% revenue CAGR, $30M enterprise value, top customer = 12% of revenue,
      founder-owned, full CIM provided, 3 years of audited financials.
    expected:
      - "Investment thesis with 3+ pillars identified"
      - "Entry multiple calculated: 12.0x EV/EBITDA"
      - "Return sensitivity table with base/upside/downside MOIC and IRR"
      - "Risk section with 3 named risks each having a mitigant"
      - "RECOMMENDATION: PROCEED TO DILIGENCE"
    must_not:
      - "RECOMMENDATION: PASS"
      - "Missing financial data"
    flags_expected: green
    hitl_expected: false

  - id: eval-02
    name: "Red flag deal — customer concentration breach"
    input: >
      Industrial services company, $12M LTM revenue, $1.8M LTM EBITDA (15% margin),
      $22M enterprise value, top customer = 38% of revenue, 2 years financials,
      no CIM — deal summary only.
    expected:
      - "Red flag: customer concentration 38% exceeds 30% threshold"
      - "Red flag: EBITDA $1.8M below $2M minimum"
      - "RECOMMENDATION: ADDITIONAL INFO REQUIRED or PASS"
      - "Open items section lists customer contract details"
    must_not:
      - "RECOMMENDATION: PROCEED TO DILIGENCE without flagging concentration"
    flags_expected: red
    hitl_expected: true

  - id: eval-03
    name: "Missing data — no financials provided"
    input: >
      User says: 'write up Acme Corp, they do HVAC services,
      owner wants $15M, seems like a good deal.'
    expected:
      - "Request for LTM revenue and EBITDA before proceeding"
      - "List of exactly what financial data is needed"
      - "Offer to draft preliminary one-pager with available info"
    must_not:
      - "A completed IC memo with invented numbers"
      - "Return sensitivity calculations"
    flags_expected: none
    hitl_expected: false

  - id: eval-04
    name: "Rich valuation — thesis stress test"
    input: >
      Healthcare IT company, $5M LTM EBITDA, $60M enterprise value (12x),
      20% revenue CAGR, 85% gross margin, SaaS model, no customer concentration,
      full CIM provided.
    expected:
      - "Red flag: entry multiple 12.0x exceeds 10x threshold"
      - "Strong thesis supporting the premium valuation"
      - "Downside scenario showing return degradation at multiple compression"
      - "RECOMMENDATION stated explicitly"
    must_not:
      - "No mention of valuation risk"
    flags_expected: red
    hitl_expected: true
```

---

## Observability

Emit this log block at the start of every run, before any output:

```
[SKILL RUN LOG]
skill: ic-memo
version: 2.0.0
timestamp: [ISO-8601]
steps_completed: [company-overview, thesis, financial-analysis, risk-assessment,
                  value-creation, structure, gap-flags]
steps_skipped: [list any skipped with reason]
flags_raised:
  - [red/yellow/green]: [description]
hitl_triggered: true/false — [reason if true]
memory_read:
  - [artifact keys or patterns referenced]
memory_written:
  - ic-memo:[company-slug]:[date]
estimated_tokens: ~[N]
elapsed_seconds: [N]
output_confidence: high | medium | low
```

**Confidence rules for IC memo:**
- **high** — all required inputs present, no red flags, all 7 steps completed
- **medium** — optional inputs missing (no CIM, no comps), or yellow flags present
- **low** — financials unaudited/inferred, red flags present, or required inputs missing — always triggers HITL

---

## Human-in-the-Loop (HITL) Design

### Trigger 1 — Red Flag Detected

```
HITL Trigger: Any red flag (customer concentration >30%, EBITDA <$2M,
              entry multiple >10x, declining revenue, regulatory exposure)

Agent produces:
  - Completed memo sections up to the flag point
  - Red flag summary box: "STOPPED: [flag description]. This requires
    your judgment before I complete the memo."
  - Option A: "Override — proceed anyway. I'll note the flag but
    complete the memo. (Use if you have context I don't)"
  - Option B: "Add mitigant — tell me why this flag is acceptable
    and I'll incorporate it into the risk section"
  - Option C: "Stop — I'll save as draft and flag for team discussion"
  Recommended: Option B (preserves the reasoning)

Human responds with: free text explanation OR selection of A/B/C
Agent resumes:
  - Option A: completes memo, adds prominent flag disclaimer
  - Option B: incorporates explanation as named mitigant, completes memo
  - Option C: saves draft to memory, notifies deal team
Timeout: 24 hours — auto-saves as draft, notifies deal lead
```

### Trigger 2 — Missing Required Data

```
HITL Trigger: Company name present but LTM financials or deal structure absent

Agent produces:
  - "I need the following to draft the IC memo:"
  - Numbered list of exactly what is missing
  - "I can draft a preliminary one-pager with what's available
    while you gather the rest — want me to do that?"

Human responds with: missing data OR "yes, draft one-pager"
Agent resumes: proceeds with full memo OR drafts one-pager
Timeout: none — waits for response
```

---

## Memory

```yaml
memory:
  reads:
    working:
      - session_deal_context      # Any deal info already discussed this session
    artifacts:
      - ic-memo:[similar-company] # Prior memos on comparable deals
      - diligence:[company-slug]  # Diligence findings if this follows DD
    patterns:
      - sector:[industry]-risks   # Common risks for this industry
      - sector:[industry]-thesis  # Common thesis pillars for this sector
      - valuation:[sector]-comps  # Sector multiple benchmarks
    portco_config: []             # Not applicable — pre-investment skill

  writes:
    artifacts:
      - key: "ic-memo:[company-slug]:[YYYY-MM-DD]"
        content: "Completed IC memo with thesis, financials, risks, recommendation"
        ttl: permanent
      - key: "deal-metadata:[company-slug]"
        content: "Entry multiple, sector, deal size, recommendation outcome"
        ttl: permanent
    patterns:
      - key: "sector:[industry]-risks"
        trigger: "Red flags identified that weren't in existing pattern library"
        content: "New risk type + mitigant observed on this deal"
```

---

## Action Layer

```yaml
actions:
  - system: Chronograph
    operation: create
    trigger: "Recommendation is PROCEED TO DILIGENCE"
    data: "New deal record: company name, sector, EV, entry multiple,
           thesis summary, next steps"
    auth: MCP connector (core/.mcp.json)
    status: planned
    fallback: "Export deal summary as markdown to /deals/[slug]/ic-memo.md"

  - system: Email
    operation: notify
    trigger: "HITL triggered — red flag requires human review"
    data: "Flag description, deal name, options for response,
           link to draft memo"
    auth: SMTP via MCP
    status: planned
    fallback: "Print HITL prompt to console for manual relay"
```
