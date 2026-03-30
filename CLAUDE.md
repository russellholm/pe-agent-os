# PE Agent OS

## Project Overview

This repo is a **agent operating system for small private equity firms** — a library of skills, plugins, personas, and commands that replace G&A functions across portfolio companies with AI agents, and automate investment workflows at the fund level.

**Two-sided mission:**
1. **Investment side** — Agents that make the deal team faster: sourcing, diligence, IC memos, portfolio monitoring, board packs, exit prep
2. **Operating side** — Agents that replace or augment G&A at portfolio companies: Finance, HR, Legal, Sales Ops, Marketing Ops, IT

**North star:** A new portfolio company should be fully configured with the agent OS in under 2 weeks, with every G&A function covered by an agent within 90 days of acquisition.

---

## Repo Structure

```
pe-agent-os/
├── CLAUDE.md                        # This file — read first
├── README.md                        # Public-facing overview
├── SKILL-STANDARD.md                # How to write a SKILL.md
├── PORTCO-ONBOARDING.md             # How to configure agents for a new portco
│
├── .claude-plugin/
│   └── plugin.json                  # Master plugin manifest
│
├── core/                            # Shared foundation — install first
│   ├── SKILL.md
│   └── .mcp.json                    # MCP connectors (Chronograph, PitchBook, etc.)
│
├── investment-side/                 # Fund-level agents
│   ├── deal-sourcing/
│   ├── due-diligence/
│   ├── ic-memo/
│   ├── portfolio-monitoring/
│   ├── board-pack/
│   └── exit-readiness/
│
├── operating-side/                  # Portfolio company G&A agents
│   ├── finance/                     # Monthly close, reporting, forecasting, covenants
│   ├── hr/                          # Recruiting, onboarding, comp, compliance
│   ├── legal/                       # Contract review, entity mgmt, compliance
│   ├── sales-ops/                   # CRM hygiene, pipeline review, forecasting
│   ├── marketing-ops/               # Demand gen, content, brand
│   └── it-ops/                      # Vendor mgmt, access, security
│
├── personas/                        # Agent identities with curated skill loadouts
│   ├── operating-partner.md
│   ├── portco-cfo.md
│   ├── portco-coo.md
│   ├── deal-analyst.md
│   └── TEMPLATE.md
│
├── commands/                        # Explicit slash commands
│   ├── board-pack.md
│   ├── ic-memo.md
│   ├── 100-day-plan.md
│   ├── kpi-review.md
│   ├── diligence-checklist.md
│   └── exit-narrative.md
│
└── templates/                       # Reusable output templates
    ├── ic-memo-template.md
    ├── board-pack-template.md
    ├── 100-day-plan-template.md
    └── monthly-finance-report-template.md
```

---

## Skill File Standard

Every skill follows this structure. Never deviate.

```
skill-name/
├── SKILL.md          # Required — trigger conditions, workflow, decision frameworks
├── README.md         # Optional — usage examples, installation
├── scripts/          # Optional — stdlib-only Python tools (zero pip installs)
└── references/       # Optional — templates, checklists, domain knowledge
```

### SKILL.md Format

```markdown
---
name: skill-name
description: "One sentence. Include trigger keywords. When to use, when NOT to use."
version: 1.0.0
domain: investment-side | operating-side
function: finance | hr | legal | deal-sourcing | etc.
portco-configurable: true | false
---

# Skill Name

## Purpose
What this skill does and why it exists.

## Triggers
Bullet list of exact phrases or situations that activate this skill.

## Workflow
Step-by-step. Include decision points. Be specific about inputs and outputs.

## Decision Framework
When to escalate to a human. What requires judgment vs. what can be automated.

## Output Format
What the deliverable looks like. Link to template if applicable.

## Portco Configuration
Variables to customize per portfolio company (if portco-configurable: true).
```

---

## Persona Standard

Personas are agent identities that combine multiple skills with a communication style and set of priorities.

```markdown
---
name: persona-name
role: Operating Partner | Portco CFO | Deal Analyst | etc.
skills: [skill-1, skill-2, skill-3]
triggers: ["situations that activate this persona"]
---

# Persona Name

## Identity
Who this agent is, what they care about, how they think.

## Priorities (in order)
1. First priority
2. Second priority
3. Third priority

## Communication Style
How this agent writes and speaks. Tone, format preferences, level of detail.

## Skill Loadout
Which skills this persona draws on and when.

## Escalation Rules
What this persona always refers to a human. Non-negotiables.
```

---

## MCP Connectors

The following MCP servers are available. Reference them in `.mcp.json` files.

| Provider | Purpose | URL |
|----------|---------|-----|
| PitchBook | Deal sourcing, market data | `https://premium.mcp.pitchbook.com/mcp` |
| Chronograph | Portfolio company monitoring | `https://ai.chronograph.pe/mcp` |
| S&P Global | Financial data, comps | `https://kfinance.kensho.com/integrations/mcp` |
| FactSet | Financial modeling data | `https://mcp.factset.com/mcp` |
| Morningstar | Market benchmarks | `https://mcp.morningstar.com/mcp` |

---

## Build Priorities

### Phase 1 — Investment Side (Current Focus)
- [ ] `core/` — shared financial analysis skill + MCP connectors
- [ ] `investment-side/ic-memo/` — IC memo drafting
- [ ] `investment-side/board-pack/` — board pack generation
- [ ] `investment-side/portfolio-monitoring/` — KPI tracking + red flags
- [ ] `investment-side/due-diligence/` — diligence checklist + red flag scanner
- [ ] `personas/deal-analyst.md`
- [ ] `personas/operating-partner.md`
- [ ] `commands/ic-memo.md`
- [ ] `commands/board-pack.md`

### Phase 2 — Operating Side: Finance G&A
- [ ] `operating-side/finance/` — monthly close, variance commentary, 13-week cash flow, covenant monitoring
- [ ] `personas/portco-cfo.md`
- [ ] `commands/kpi-review.md`
- [ ] `templates/monthly-finance-report-template.md`

### Phase 3 — Operating Side: HR + Legal
- [ ] `operating-side/hr/`
- [ ] `operating-side/legal/`

### Phase 4 — Operating Side: Revenue
- [ ] `operating-side/sales-ops/`
- [ ] `operating-side/marketing-ops/`

### Phase 5 — Portco OS Layer
- [ ] `PORTCO-ONBOARDING.md` — repeatable 2-week configuration playbook
- [ ] `operating-side/it-ops/`
- [ ] Per-portco configuration system

---

## Key Reference Repos

Study these when building new skills or agents:

| Repo | What to Steal |
|------|--------------|
| `anthropics/financial-services-plugins` | Plugin manifest structure, PE skill templates, MCP connector pattern, commands/ vs skills/ separation |
| `alirezarezvani/claude-skills` | SKILL.md format, Python tool conventions, skill authoring standard |
| `virattt/ai-hedge-fund` | Persona-as-agent pattern — each agent encodes a distinct mental model |
| `hvkshetry/StewardOS` | Portfolio OS architecture — persona layer → MCP layer → application stack |
| `msitarzewski/agency-agents` | Multi-tool conversion, agent persona structure |

---

## Coding Conventions

- **No external dependencies in scripts/** — stdlib Python only (os, json, csv, datetime, pathlib)
- **All SKILL.md files must have valid YAML frontmatter** — name, description, version, domain, function
- **Templates live in `templates/`** — skills reference them, never embed full templates inline
- **Commands are explicit** — only things a user invokes with `/command`. Everything else is a skill.
- **Portco config is always a variable** — never hardcode company names, thresholds, or formats into skills

---

## How to Add a New Skill

1. Create folder in the right domain (`investment-side/` or `operating-side/`)
2. Write `SKILL.md` following the standard above
3. Add any Python tools to `scripts/` (stdlib only)
4. Add any reference docs, checklists, or templates to `references/`
5. Register the skill in `.claude-plugin/plugin.json`
6. Update the relevant persona's skill loadout in `personas/`
7. Add a command to `commands/` if user-invocable
8. Mark as complete in the Build Priorities checklist above

---

## How to Configure for a New Portfolio Company

See `PORTCO-ONBOARDING.md` (to be built in Phase 5).

Short version:
1. Copy `templates/portco-config-template.md` → `portcos/[company-name]/config.md`
2. Fill in: industry, systems (ERP, HRIS, CRM), KPI definitions, reporting cadence, covenant thresholds, key contacts
3. Run `scripts/configure_portco.py` to generate portco-specific skill variants
4. Test with `/kpi-review` and `/board-pack` commands

---

## Session Workflow

When starting a Claude Code session in this repo:
1. Read this file (`CLAUDE.md`)
2. Check the Build Priorities checklist — identify what's next
3. Read `SKILL-STANDARD.md` before writing any new skill
4. Read the relevant reference repo patterns before building something new
5. Always run a skill through the SKILL.md format checklist before marking it done
