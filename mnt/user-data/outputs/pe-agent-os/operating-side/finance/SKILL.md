---
name: finance-gna
description: "Automates finance G&A functions for portfolio companies: monthly close support, variance commentary, cash flow forecasting, covenant monitoring, and board reporting. Use when: 'monthly close', 'variance analysis', 'cash flow', 'covenant', 'board reporting', 'finance package', 'CFO report'. Do NOT use for: investment-side IC memos, fund-level reporting, or LP communications."
version: 2.0.0
domain: operating-side
function: finance
portco-configurable: true
author: PE Agent OS
changelog:
  - 1.0.0: Initial version — 5 modules, portco config, decision framework
  - 2.0.0: Added evals (4 test cases), observability log, HITL design (3 triggers),
            memory spec, action layer stubs (Google Sheets, Email, Chronograph, NetSuite)
---

# Finance G&A Agent

## Purpose
Replaces or augments the controller/CFO function at portfolio companies for routine finance G&A work. Handles the monthly reporting cycle, cash flow monitoring, covenant tracking, and board finance package — freeing management to focus on the business rather than the finance function.

## Triggers
- "Monthly close" / "close the books" / "close package"
- "Variance analysis" / "explain the variance" / "budget vs. actual"
- "Cash flow" / "13-week cash flow" / "liquidity"
- "Covenant" / "compliance certificate" / "leverage ratio"
- "Board package" / "board reporting" / "finance section"
- `/kpi-review` command invoked
- End of month (can be triggered on schedule)

## Portco Configuration

```yaml
PORTCO_NAME: "[Company Name]"
REPORTING_CADENCE: monthly          # monthly | quarterly
ERP_SYSTEM: NetSuite                # NetSuite | QuickBooks | Sage | SAP | other
FISCAL_YEAR_END: December           # Month name
BOARD_MEETING_DAY: 15               # Day of month after close
CLOSE_TARGET_DAYS: 10               # Business days after month end

# KPI Definitions
KPI_REVENUE: "Net revenue excluding contra"
KPI_EBITDA: "Operating income + D&A + stock comp"
KPI_NRR: "Net revenue retention (SaaS portcos only)"

# Covenant Thresholds (from credit agreement)
COVENANT_MAX_LEVERAGE: 4.5          # Total debt / LTM EBITDA
COVENANT_MIN_COVERAGE: 1.25         # EBITDA / cash interest
COVENANT_TESTING_FREQUENCY: quarterly

# Reporting Format
CURRENCY: USD
ROUNDING: thousands                 # thousands | millions
COMPARISON_PERIOD: prior_year       # prior_year | budget | both
```

## Workflow

### Module 1 — Monthly Close Support

**Step 1: Pre-close checklist**
Generate a close checklist for the portco controller:
- [ ] Bank reconciliations complete
- [ ] AR aging reviewed, bad debt reserve updated
- [ ] AP accruals posted (recurring vendors, utilities, rent)
- [ ] Payroll entries posted and reconciled
- [ ] Prepaid and deferred revenue schedules updated
- [ ] Fixed asset additions/disposals recorded
- [ ] Intercompany eliminations (if applicable)
- [ ] Month-end journal entries reviewed by CFO

**Step 2: Variance commentary**
When provided with actuals vs. budget or prior year:
- Calculate dollar and percent variances for each P&L line
- Identify variances > $10K or > 5% (flag for explanation)
- Draft one-sentence commentary for each flagged variance
- Aggregate into executive summary: "Revenue beat by $X driven by Y; EBITDA missed by $Z due to W"

**Step 3: Close package assembly**
Compile:
1. P&L (actuals vs. budget vs. prior year, with variance columns)
2. Balance sheet (current month vs. prior month)
3. Cash flow statement (YTD)
4. KPI dashboard (see Module 3)
5. Variance commentary narrative
6. Open items for next month

### Module 2 — 13-Week Cash Flow

When requested or when cash balance triggers threshold:

**Step 1: Build/update cash flow model**
Weeks 1-13 rolling forecast:
- Collections: AR aging × historical DSO, plus known large receipts
- Disbursements: payroll (bi-weekly), rent, debt service, vendor payments
- Net cash position by week

**Step 2: Flag liquidity risks**
- 🔴 Projected cash < $[PORTCO_MIN_CASH] in any week → Immediate escalation
- 🟡 Projected cash < $[PORTCO_MIN_CASH × 1.5] in any week → Flag to PE operating partner
- 🟢 Comfortable coverage throughout → No action needed

**Step 3: Options if liquidity risk**
Draft memo with:
- Specific week(s) of stress
- Dollar shortfall amount
- Options: revolver draw, collection acceleration, payable extension
- Recommendation with rationale

### Module 3 — KPI Dashboard

Generate standard portco KPI dashboard monthly:

| KPI | Current Month | Budget | Prior Year | YTD | YTD Budget |
|-----|--------------|--------|-----------|-----|-----------|
| Revenue | | | | | |
| Gross Profit | | | | | |
| Gross Margin % | | | | | |
| EBITDA | | | | | |
| EBITDA Margin % | | | | | |
| Cash Balance | | | | | |
| ARR (if SaaS) | | | | | |
| NRR (if SaaS) | | | | | |

**Trend flags:**
- Revenue: 3-month trend arrow (↑ ↓ →)
- EBITDA margin: compare to underwriting assumptions
- Cash: vs. prior month and vs. covenant minimum

### Module 4 — Covenant Monitoring

Run quarterly (or monthly if requested):

**Step 1: Calculate ratios**
- Leverage ratio: Total debt ÷ LTM EBITDA
- Interest coverage: LTM EBITDA ÷ LTM cash interest expense
- Any other covenants in credit agreement

**Step 2: Headroom analysis**
For each covenant:
- Current ratio
- Covenant threshold
- Headroom ($, bps)
- Projected ratio at next test date

**Step 3: Compliance certificate draft**
If within 30 days of test date, draft compliance certificate:
- Calculation schedule
- Officer certification language
- Flag any covenants with < 20% headroom for PE firm review

**Escalation:**
- 🔴 Any covenant within 10% of threshold → Immediate PE operating partner notification
- 🔴 Projected breach at next test date → Alert deal team, begin waiver process

### Module 5 — Board Finance Package

Assemble the finance section of the board package:

1. **Executive summary** (1 page): Month/quarter in review, key wins, key misses, outlook
2. **P&L summary** with variance commentary
3. **KPI dashboard** (Module 3 output)
4. **Cash flow** and liquidity update
5. **Covenant compliance** summary
6. **Rolling 12-month outlook**: Revenue and EBITDA bridge to year-end
7. **Key risks and mitigants** (top 3)
8. **Asks of the board** (if any)

Format per `templates/monthly-finance-report-template.md`.

## Decision Framework

**Handle autonomously:**
- Routine monthly close checklist generation
- Variance commentary for variances < $50K
- KPI dashboard population
- Covenant calculation (non-breach situations)

**Flag to portco CFO/controller:**
- Unusual journal entries or balance sheet movements
- Variances > $50K requiring business context
- Customer payment anomalies in AR

**Escalate to PE operating partner:**
- Covenant headroom < 20%
- Cash projected below minimum in 13-week model
- EBITDA trending > 15% below budget for 2+ consecutive months
- Any off-cycle cash need > $500K

**Escalate to PE deal team:**
- Potential covenant breach
- Material adverse change in business performance
- CFO/controller departure

## Output Formats

- **Monthly close package**: Word/markdown document per template
- **13-week cash flow**: Excel/CSV with weekly cash positions
- **KPI dashboard**: Table (markdown or Excel)
- **Covenant compliance**: Calculation schedule + certificate draft
- **Board finance section**: Follows `templates/board-pack-template.md`

## Quality Checklist
Before delivering any finance output:
- [ ] All numbers tie to source data (no manual overrides without notation)
- [ ] Variances explained, not just calculated
- [ ] Any 🔴 flags surfaced before output delivered
- [ ] Covenant ratios verified against credit agreement definition
- [ ] Output reviewed against prior month for anomalies

## Related Skills
- `board-pack` — finance section feeds into full board package
- `portfolio-monitoring` — KPI dashboard feeds fund-level monitoring
- `exit-readiness` — clean financials are table stakes for exit

## Known Limitations
- Cannot access ERP systems directly without MCP connector configured
- Cannot make accounting policy judgments (revenue recognition, capitalization) — always flag these for CFO review
- Cash flow forecast accuracy depends on quality of AR aging and payment terms provided
- Does not replace audit or tax preparation

---

## Evals

```yaml
evals:
  - id: eval-01
    name: "Clean monthly close — full data, no issues"
    input: >
      Portco: $2.5M revenue month (vs $2.4M budget, +4.2%), $380K EBITDA
      (vs $350K budget, +8.6%), all accruals posted, bank recs complete,
      leverage ratio 3.2x (covenant max 4.5x), cash $1.8M.
    expected:
      - "P&L variance commentary: revenue beat driven by [explanation]"
      - "KPI dashboard populated with all standard metrics"
      - "Covenant headroom calculated: 1.3x below max"
      - "output_confidence: high"
    must_not:
      - "Any red flags raised"
      - "HITL triggered"
    flags_expected: green
    hitl_expected: false

  - id: eval-02
    name: "Covenant near-breach — escalation required"
    input: >
      Portco Q3 close: LTM EBITDA $3.1M (down from $3.8M prior year),
      total debt $14.2M, leverage ratio 4.58x, covenant max 4.5x,
      next test date in 45 days.
    expected:
      - "Red flag: leverage ratio 4.58x exceeds covenant max 4.5x"
      - "Projected ratio at next test date calculated"
      - "HITL triggered with notification to PE operating partner"
      - "Options presented: waiver request, debt paydown, EBITDA acceleration"
    must_not:
      - "Covenant compliance certificate drafted as if passing"
      - "Issue downplayed or buried in output"
    flags_expected: red
    hitl_expected: true

  - id: eval-03
    name: "Cash stress — 13-week model shows liquidity gap"
    input: >
      Portco current cash $420K, payroll due in 10 days ($280K),
      largest customer payment ($350K) 30 days overdue,
      revolver availability $500K, monthly fixed costs $180K.
    expected:
      - "13-week cash flow showing week-by-week positions"
      - "Red flag: projected cash below minimum in week 2"
      - "Options: revolver draw, collection acceleration, payable extension"
      - "HITL triggered with specific dollar amounts and timing"
    must_not:
      - "Cash stress not flagged"
      - "Generic advice without specific numbers"
    flags_expected: red
    hitl_expected: true

  - id: eval-04
    name: "Large unexplained variance — CFO flag"
    input: >
      Monthly close: SG&A $180K actual vs $95K budget (+89%).
      No explanation provided in source data.
    expected:
      - "Yellow flag: SG&A variance $85K over budget requires explanation"
      - "HITL triggered: request explanation from portco CFO/controller"
      - "Variance noted in close package as pending explanation"
    must_not:
      - "Variance commentary fabricated or assumed"
      - "Variance passed through without flag"
    flags_expected: yellow
    hitl_expected: true
```

---

## Observability

Emit this log block at the start of every run, before any output:

```
[SKILL RUN LOG]
skill: finance-gna
version: 2.0.0
timestamp: [ISO-8601]
portco: [PORTCO_NAME]
module: monthly-close | cash-flow | kpi-dashboard | covenants | board-package
steps_completed: [list of completed steps]
steps_skipped: [list with reason]
flags_raised:
  - [red/yellow/green]: [description and dollar amount if applicable]
hitl_triggered: true/false — [reason, recipient if true]
memory_read:
  - [prior month artifact key if referenced]
  - [portco config variables loaded]
memory_written:
  - [artifact keys produced this run]
estimated_tokens: ~[N]
elapsed_seconds: [N]
output_confidence: high | medium | low
```

**Confidence rules for finance:**
- **high** — source data provided, all steps completed, no flags
- **medium** — some data inferred from prior period, yellow flags present
- **low** — material data gaps, red flags present, or covenant at risk — always triggers HITL

---

## Human-in-the-Loop (HITL) Design

### Trigger 1 — Covenant Near-Breach

```
HITL Trigger: Leverage ratio within 10% of covenant max OR projected
              breach at next test date

Agent produces:
  - Current ratio vs covenant max (specific numbers)
  - Projected ratio at next test date (with assumptions shown)
  - Headroom in dollar terms (how much EBITDA improvement needed to clear)
  - Option A: "Request a waiver — I'll draft the waiver request letter"
  - Option B: "Accelerate debt paydown — I'll model the required payment"
  - Option C: "Pursue EBITDA improvement — I'll identify the fastest levers"
  - Option D: "Escalate to deal team now — this needs legal/lender engagement"
  Recommended: Option D if breach projected within 45 days

Human responds with: option selection + any additional context
Agent resumes:
  - Option A: drafts waiver request with supporting schedules
  - Option B: models paydown scenarios with cash impact
  - Option C: pulls value creation plan levers, estimates timeline
  - Option D: prepares lender communication package, notifies deal team
Timeout: 4 hours — auto-escalates to PE deal team with full context
```

### Trigger 2 — Large Unexplained Variance

```
HITL Trigger: Any P&L line variance > $50K with no explanation in source data

Agent produces:
  - Variance amount and percentage vs budget/prior year
  - Which specific line item (not just "SG&A was high")
  - "I need context before I can write commentary on this variance:"
  - Request for explanation (one specific question, not open-ended)

Human responds with: explanation of variance
Agent resumes: writes commentary incorporating explanation, completes close package
Timeout: 48 hours — flags as "explanation pending" in close package,
          delivers package with open item noted
```

### Trigger 3 — Cash Stress

```
HITL Trigger: Projected cash below minimum threshold in any week
              of 13-week model

Agent produces:
  - Week-by-week cash position table (showing stress week clearly)
  - Dollar shortfall amount and timing
  - Option A: "Draw revolver — I'll prepare the draw request"
  - Option B: "Accelerate collections — I'll identify overdue AR to chase"
  - Option C: "Extend payables — I'll identify which vendors to approach"
  - Option D: "Combination — I'll model the optimal mix"
  Recommended: Option D (diversifies the response)

Human responds with: option + approval to proceed
Agent resumes: prepares relevant documents/communications per option chosen
Timeout: 2 hours — cash stress is urgent, auto-escalates to PE operating partner
```

---

## Memory

```yaml
memory:
  reads:
    working:
      - session_portco_context      # Any portco info discussed this session
    artifacts:
      - close-package:[portco]:[prior-month]  # Prior month close for comparison
      - kpi-dashboard:[portco]:ytd            # YTD KPI trend data
      - covenant-calc:[portco]:last           # Last covenant calculation
    patterns:
      - portco:[portco-slug]-seasonality      # Known seasonal patterns
      - portco:[portco-slug]-variance-norms   # Normal variance ranges for this business
    portco_config:
      - PORTCO_NAME
      - REPORTING_CADENCE
      - COVENANT_THRESHOLDS
      - ERP_SYSTEM
      - KPI_DEFINITIONS
      - BOARD_MEETING_DAY
      - CLOSE_TARGET_DAYS

  writes:
    artifacts:
      - key: "close-package:[portco-slug]:[YYYY-MM]"
        content: "Full monthly close package: P&L, BS, CF, KPIs, commentary"
        ttl: permanent
      - key: "covenant-calc:[portco-slug]:[YYYY-MM]"
        content: "Covenant ratios, headroom, next test date"
        ttl: permanent
      - key: "cash-forecast:[portco-slug]:[YYYY-MM-DD]"
        content: "13-week cash flow model with assumptions"
        ttl: 90d
    patterns:
      - key: "portco:[portco-slug]-variance-norms"
        trigger: "3+ consecutive months of same variance pattern observed"
        content: "Normal variance range for this line item at this portco"
```

---

## Action Layer

```yaml
actions:
  - system: Google Sheets
    operation: update
    trigger: "KPI dashboard module completes"
    data: "Monthly KPI values written to portco KPI tracker spreadsheet"
    auth: Google OAuth via MCP
    status: planned
    fallback: "Export KPI table as CSV to /portcos/[slug]/kpis/[month].csv"

  - system: Email
    operation: notify
    trigger: "HITL triggered — covenant near-breach or cash stress"
    data: "Flag summary, portco name, specific numbers, response options,
           deadline for response"
    auth: SMTP via MCP
    status: planned
    fallback: "Print urgent flag to console for manual relay"

  - system: Chronograph
    operation: update
    trigger: "Monthly close package completed"
    data: "Revenue, EBITDA, margin, cash, covenant ratios written to
           portco monitoring record"
    auth: MCP connector (core/.mcp.json)
    status: planned
    fallback: "Export close summary as markdown to /portcos/[slug]/closes/[month].md"

  - system: NetSuite
    operation: create
    trigger: "Pre-close checklist module — accrual entries identified"
    data: "Draft journal entry suggestions for controller review"
    auth: NetSuite OAuth via MCP
    status: planned
    fallback: "Export accrual suggestions as CSV for manual entry"
```
