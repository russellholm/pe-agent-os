#!/usr/bin/env python3
"""
setup.py — PE Agent OS one-time setup
Run once after cloning the repo.
stdlib only, no pip installs required.

Usage:
    python3 setup.py
"""

import os
import sys
import pathlib
import json
import datetime

REPO_ROOT = pathlib.Path(__file__).parent


def create_dir(path: pathlib.Path, label: str):
    path.mkdir(parents=True, exist_ok=True)
    print(f"  ✓ {label}")


def create_file_if_missing(path: pathlib.Path, content: str, label: str):
    if path.exists():
        print(f"  · {label} (already exists, skipped)")
    else:
        path.write_text(content)
        print(f"  ✓ {label}")


def verify_structure():
    required = [
        "CLAUDE.md",
        "SKILL-STANDARD.md",
        ".claude-plugin/plugin.json",
        ".claude/commands/ic-memo.md",
        ".claude/commands/kpi-review.md",
        ".claude/commands/improve-skill.md",
        ".claude/commands/run-evals.md",
        ".claude/commands/new-skill.md",
        "investment-side/ic-memo/SKILL.md",
        "investment-side/ic-memo/scripts/run_evals.py",
        "investment-side/ic-memo/references/failure-log.md",
        "investment-side/ic-memo/references/eval-results.jsonl",
        "operating-side/finance/SKILL.md",
        "operating-side/finance/scripts/run_evals.py",
        "operating-side/finance/references/failure-log.md",
        "operating-side/finance/references/eval-results.jsonl",
        "meta/skill-improver/SKILL.md",
    ]
    
    missing = []
    for f in required:
        p = REPO_ROOT / f
        if not p.exists():
            missing.append(f)
    
    return missing


def create_portco_template():
    template = """# Portco Configuration Template
# Copy this to portcos/[company-slug]/config.md and fill in values

PORTCO_NAME: "[Company Name]"
PORTCO_SLUG: "[company-slug]"         # kebab-case, used in artifact keys
INDUSTRY: "[industry]"                 # e.g. B2B SaaS, Healthcare Services

# Systems
ERP_SYSTEM: NetSuite                   # NetSuite | QuickBooks | Sage | SAP | other
HRIS_SYSTEM: Rippling                  # Rippling | ADP | Gusto | Bullhorn | other
CRM_SYSTEM: Salesforce                 # Salesforce | HubSpot | Bullhorn | other

# Reporting
REPORTING_CADENCE: monthly             # monthly | quarterly
FISCAL_YEAR_END: December              # Month name
BOARD_MEETING_DAY: 15                  # Day of month after close
CLOSE_TARGET_DAYS: 10                  # Business days after month end
CURRENCY: USD
ROUNDING: thousands                    # thousands | millions

# KPI Definitions
KPI_REVENUE: "Net revenue excluding contra-revenue"
KPI_EBITDA: "Operating income + D&A + stock-based comp + one-time items"
KPI_NRR: "Net revenue retention (SaaS portcos only — delete if not applicable)"

# Covenant Thresholds (from credit agreement — update at each amendment)
COVENANT_MAX_LEVERAGE: 4.5             # Total debt / LTM EBITDA
COVENANT_MIN_COVERAGE: 1.25            # LTM EBITDA / LTM cash interest
COVENANT_TESTING_FREQUENCY: quarterly  # quarterly | semi-annual | annual
COVENANT_NEXT_TEST_DATE: YYYY-MM-DD

# Cash Management
PORTCO_MIN_CASH: 500000                # Minimum cash balance before escalation ($)
REVOLVER_AVAILABILITY: 0               # Available revolver capacity ($, 0 if none)

# Key Contacts
CFO_NAME: ""
CFO_EMAIL: ""
CONTROLLER_NAME: ""
CONTROLLER_EMAIL: ""
PE_DEAL_LEAD: ""
PE_OPERATING_PARTNER: ""

# Acquisition Context
ACQUISITION_DATE: YYYY-MM-DD
ENTRY_EV: 0                            # Entry enterprise value ($M)
ENTRY_EBITDA: 0                        # LTM EBITDA at acquisition ($M)
ENTRY_MULTIPLE: 0.0                    # EV / EBITDA at entry
HOLD_PERIOD_TARGET: 5                  # Years
"""
    return template


def main():
    print("\nPE Agent OS — Setup\n" + "="*40)
    
    # Step 1 — Directory structure
    print("\n1. Creating directory structure...")
    dirs = [
        (REPO_ROOT / ".claude" / "commands", "claude commands"),
        (REPO_ROOT / ".claude-plugin", "plugin manifest"),
        (REPO_ROOT / "core", "core/"),
        (REPO_ROOT / "investment-side" / "ic-memo" / "scripts", "ic-memo/scripts/"),
        (REPO_ROOT / "investment-side" / "ic-memo" / "references", "ic-memo/references/"),
        (REPO_ROOT / "investment-side" / "due-diligence", "due-diligence/ (placeholder)"),
        (REPO_ROOT / "investment-side" / "board-pack", "board-pack/ (placeholder)"),
        (REPO_ROOT / "investment-side" / "portfolio-monitoring", "portfolio-monitoring/ (placeholder)"),
        (REPO_ROOT / "investment-side" / "deal-sourcing", "deal-sourcing/ (placeholder)"),
        (REPO_ROOT / "investment-side" / "exit-readiness", "exit-readiness/ (placeholder)"),
        (REPO_ROOT / "operating-side" / "finance" / "scripts", "finance/scripts/"),
        (REPO_ROOT / "operating-side" / "finance" / "references", "finance/references/"),
        (REPO_ROOT / "operating-side" / "hr", "hr/ (placeholder)"),
        (REPO_ROOT / "operating-side" / "legal", "legal/ (placeholder)"),
        (REPO_ROOT / "operating-side" / "sales-ops", "sales-ops/ (placeholder)"),
        (REPO_ROOT / "operating-side" / "marketing-ops", "marketing-ops/ (placeholder)"),
        (REPO_ROOT / "operating-side" / "it-ops", "it-ops/ (placeholder)"),
        (REPO_ROOT / "meta" / "skill-improver", "meta/skill-improver/"),
        (REPO_ROOT / "personas", "personas/"),
        (REPO_ROOT / "commands", "commands/"),
        (REPO_ROOT / "templates", "templates/"),
        (REPO_ROOT / "portcos", "portcos/ (per-portco configs)"),
        (REPO_ROOT / "memory" / "artifacts", "memory/artifacts/"),
        (REPO_ROOT / "memory" / "patterns", "memory/patterns/"),
    ]
    for path, label in dirs:
        create_dir(path, label)
    
    # Step 2 — Seed files
    print("\n2. Creating seed files...")
    
    seed_files = [
        (
            REPO_ROOT / "investment-side" / "ic-memo" / "references" / "eval-results.jsonl",
            json.dumps({"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()+"Z",
                        "eval_id": "seed", "skill": "ic-memo", "version": "2.0.0",
                        "note": "Initialized by setup.py"}) + "\n",
            "ic-memo eval-results.jsonl"
        ),
        (
            REPO_ROOT / "operating-side" / "finance" / "references" / "eval-results.jsonl",
            json.dumps({"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()+"Z",
                        "eval_id": "seed", "skill": "finance-gna", "version": "2.0.0",
                        "note": "Initialized by setup.py"}) + "\n",
            "finance eval-results.jsonl"
        ),
        (
            REPO_ROOT / "templates" / "portco-config-template.md",
            create_portco_template(),
            "portco-config-template.md"
        ),
        (
            REPO_ROOT / "memory" / "artifacts" / ".gitkeep",
            "",
            "memory/artifacts/.gitkeep"
        ),
        (
            REPO_ROOT / "memory" / "patterns" / ".gitkeep",
            "",
            "memory/patterns/.gitkeep"
        ),
    ]
    
    for path, content, label in seed_files:
        create_file_if_missing(path, content, label)
    
    # Step 3 — Verify
    print("\n3. Verifying structure...")
    missing = verify_structure()
    
    if missing:
        print(f"\n  ⚠️  {len(missing)} required files not found:")
        for f in missing:
            print(f"     - {f}")
        print("\n  These files must exist before using Claude Code.")
        print("  Copy them from your downloads or recreate them.")
    else:
        print("  ✓ All required files present")
    
    # Step 4 — Git check
    print("\n4. Git status...")
    git_dir = REPO_ROOT / ".git"
    if git_dir.exists():
        print("  ✓ Git repo detected")
    else:
        print("  · No git repo — run: git init && git add . && git commit -m 'init: pe-agent-os'")
    
    # Done
    print("\n" + "="*40)
    print("Setup complete.\n")
    print("Next steps:")
    print("  1. cd pe-agent-os && claude")
    print("  2. Try: /ic-memo  (paste a CIM or deal summary)")
    print("  3. Try: /kpi-review  (paste monthly financials)")
    print("  4. After real use: log failures to references/failure-log.md")
    print("  5. Monthly: /improve-skill to evolve the skills\n")


if __name__ == "__main__":
    main()
