# PE Agent OS

Agent operating system for small private equity firms. Replaces G&A functions
at portfolio companies with AI agents, and automates investment workflows at
the fund level.

---

## Quick Start

### 1. Clone and set up

```bash
git clone https://github.com/your-org/pe-agent-os
cd pe-agent-os
python3 setup.py
```

### 2. Start Claude Code

```bash
claude
```

Claude Code reads `CLAUDE.md` on startup and knows the full project context.

### 3. Run your first skill

Paste a CIM, deal summary, or financials into the chat, then:

```
/ic-memo
```

or

```
/kpi-review
```

---

## Slash Commands

| Command | What it does |
|---------|-------------|
| `/ic-memo` | Draft an IC memo from deal materials |
| `/kpi-review` | Run finance G&A for a portco close or KPI review |
| `/run-evals` | Run the eval suite for a skill, report pass/fail |
| `/improve-skill` | Analyze failure logs, propose a skill improvement |
| `/new-skill` | Scaffold a new skill following the standard |

---

## Skills

### Investment Side
| Skill | Status | Version |
|-------|--------|---------|
| `ic-memo` | ✅ Live | 2.0.0 |
| `due-diligence` | 🔲 Planned | — |
| `board-pack` | 🔲 Planned | — |
| `portfolio-monitoring` | 🔲 Planned | — |
| `deal-sourcing` | 🔲 Planned | — |
| `exit-readiness` | 🔲 Planned | — |

### Operating Side
| Skill | Status | Version |
|-------|--------|---------|
| `finance-gna` | ✅ Live | 2.0.0 |
| `hr` | 🔲 Planned | — |
| `legal` | 🔲 Planned | — |
| `sales-ops` | 🔲 Planned | — |
| `marketing-ops` | 🔲 Planned | — |
| `it-ops` | 🔲 Planned | — |

---

## The Improvement Loop

Skills get better every time you use them:

```
Use skill on real work
       ↓
Output needs a fix? Log it:
  → [skill]/references/failure-log.md
       ↓
Monthly: /improve-skill
       ↓
Review proposed diff → approve
       ↓
Version bumped → git commit
       ↓
Skill is smarter next run
```

---

## Adding a Portfolio Company

```bash
cp templates/portco-config-template.md portcos/[company-slug]/config.md
# Fill in ERP system, covenants, KPI definitions, key contacts
```

Then run `/kpi-review` — Claude loads the config automatically.

---

## File Structure

```
pe-agent-os/
├── CLAUDE.md                    # Read by Claude Code on startup
├── SKILL-STANDARD.md            # Standard for all skill files
├── setup.py                     # One-time setup script
│
├── .claude/commands/            # Slash commands
├── .claude-plugin/plugin.json   # Plugin manifest
│
├── investment-side/             # Fund-level agents
├── operating-side/              # Portfolio company G&A agents
├── meta/                        # Skills that improve skills
├── personas/                    # Agent identities
├── templates/                   # Output templates + portco config
├── portcos/                     # Per-portco configuration
└── memory/                      # Persistent artifacts and patterns
```

---

## Reference Repos

| Repo | What we borrowed |
|------|-----------------|
| `anthropics/financial-services-plugins` | Plugin manifest structure, MCP connectors |
| `alirezarezvani/claude-skills` | SKILL.md format, Python tool conventions |
| `virattt/ai-hedge-fund` | Persona-as-agent pattern |
| `hvkshetry/StewardOS` | Portfolio OS architecture |
| `karpathy/autoresearch` | Self-improving loop pattern |
| `osherai/bullhorn-mcp-python` | Bullhorn MCP connector (HR agent) |
