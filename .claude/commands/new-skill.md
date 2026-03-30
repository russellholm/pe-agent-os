# /new-skill

Scaffold and draft a new skill following the PE Agent OS standard.

## What to do

1. Read `SKILL-STANDARD.md` fully before writing a single line
2. Ask for:
   - Skill name (kebab-case)
   - Domain: investment-side or operating-side
   - Function: what it does in one phrase
   - portco-configurable: true or false
3. Create the folder structure:
   ```
   [domain]/[skill-name]/
   ├── SKILL.md
   ├── scripts/          (empty, ready for tools)
   └── references/
       └── failure-log.md
   ```
4. Draft the SKILL.md with all 13 required sections
5. For Evals: write 3 test cases minimum (happy path, red flag, missing data)
6. For HITL: write at least 1 trigger with full option menu and resume paths
7. For Action Layer: stub at minimum 1 action even if status: planned
8. Rate the skill against the quality levels before delivering
9. Register the skill in `.claude-plugin/plugin.json`

## Usage

```
/new-skill
```

Then describe what the skill should do and Claude will build it.
