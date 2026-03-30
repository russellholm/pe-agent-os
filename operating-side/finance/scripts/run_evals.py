#!/usr/bin/env python3
"""
run_evals.py — PE Agent OS skill eval runner
stdlib only, no pip installs required.

Usage:
  echo "agent output here" | python3 scripts/run_evals.py --eval eval-01
  python3 scripts/run_evals.py --list          # show all eval IDs
  python3 scripts/run_evals.py --summary       # show pass/fail history
"""

import json
import sys
import argparse
import pathlib
import datetime
import re

SKILL_DIR = pathlib.Path(__file__).parent.parent
SKILL_FILE = SKILL_DIR / "SKILL.md"
EVAL_LOG = SKILL_DIR / "references" / "eval-results.jsonl"


def parse_evals_from_skill(skill_text: str) -> list[dict]:
    """Extract eval test cases from SKILL.md Evals section."""
    evals = []
    
    # Find the Evals section
    evals_match = re.search(r'## Evals\n+```yaml\n(.*?)```', skill_text, re.DOTALL)
    if not evals_match:
        return evals
    
    yaml_block = evals_match.group(1)
    
    # Parse each eval block (simple parser, no PyYAML needed)
    current = {}
    current_list = None
    current_key = None
    
    for line in yaml_block.split('\n'):
        # New eval entry
        id_match = re.match(r'\s+- id:\s+"?([^"]+)"?', line)
        if id_match:
            if current.get('id'):
                evals.append(current)
            current = {'id': id_match.group(1), 'expected': [], 'must_not': []}
            current_list = None
            continue
        
        # Named fields
        name_match = re.match(r'\s+name:\s+"?([^"]+)"?', line)
        if name_match:
            current['name'] = name_match.group(1)
            current_list = None
            continue
            
        flags_match = re.match(r'\s+flags_expected:\s+(\S+)', line)
        if flags_match:
            current['flags_expected'] = flags_match.group(1)
            current_list = None
            continue
            
        hitl_match = re.match(r'\s+hitl_expected:\s+(\S+)', line)
        if hitl_match:
            current['hitl_expected'] = hitl_match.group(1).lower() == 'true'
            current_list = None
            continue
        
        # List sections
        if re.match(r'\s+expected:', line):
            current_list = 'expected'
            continue
        if re.match(r'\s+must_not:', line):
            current_list = 'must_not'
            continue
            
        # List items
        item_match = re.match(r'\s+- "?([^"]+)"?', line)
        if item_match and current_list in ('expected', 'must_not'):
            current[current_list].append(item_match.group(1).strip())
    
    if current.get('id'):
        evals.append(current)
    
    return evals


def score_output(output: str, eval_case: dict) -> dict:
    """Score agent output against an eval test case."""
    output_lower = output.lower()
    
    expected_hits = []
    expected_misses = []
    for criterion in eval_case.get('expected', []):
        # Check if key phrases from the criterion appear in output
        key_phrases = [w for w in criterion.lower().split() 
                      if len(w) > 4 and w not in ('should', 'would', 'could', 'must')]
        hit = any(phrase in output_lower for phrase in key_phrases)
        if hit:
            expected_hits.append(criterion)
        else:
            expected_misses.append(criterion)
    
    must_not_violations = []
    for criterion in eval_case.get('must_not', []):
        key_phrases = [w for w in criterion.lower().split()
                      if len(w) > 4 and w not in ('should', 'would', 'could', 'must')]
        violation = any(phrase in output_lower for phrase in key_phrases)
        if violation:
            must_not_violations.append(criterion)
    
    passed = len(expected_misses) == 0 and len(must_not_violations) == 0
    
    return {
        'passed': passed,
        'expected_hits': expected_hits,
        'expected_misses': expected_misses,
        'must_not_violations': must_not_violations,
        'score': len(expected_hits) / max(len(eval_case.get('expected', [1])), 1)
    }


def log_result(eval_id: str, eval_name: str, result: dict, skill_name: str, version: str):
    """Append result to eval-results.jsonl."""
    entry = {
        'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat() + 'Z',
        'skill': skill_name,
        'version': version,
        'eval_id': eval_id,
        'eval_name': eval_name,
        'passed': result['passed'],
        'score': result['score'],
        'expected_misses': result['expected_misses'],
        'must_not_violations': result['must_not_violations'],
    }
    EVAL_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(EVAL_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry


def print_summary():
    """Print pass/fail history from eval-results.jsonl."""
    if not EVAL_LOG.exists():
        print("No eval results yet. Run an eval first.")
        return
    
    results = []
    with open(EVAL_LOG) as f:
        for line in f:
            try:
                results.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    
    # Skip seed entry
    results = [r for r in results if r.get('eval_id') != 'seed']
    
    if not results:
        print("No eval results yet.")
        return
    
    print(f"\n{'='*60}")
    print(f"EVAL HISTORY — {SKILL_DIR.name}")
    print(f"{'='*60}")
    
    # Group by eval_id
    by_eval = {}
    for r in results:
        eid = r['eval_id']
        if eid not in by_eval:
            by_eval[eid] = []
        by_eval[eid].append(r)
    
    for eid, runs in sorted(by_eval.items()):
        latest = runs[-1]
        total = len(runs)
        passed = sum(1 for r in runs if r['passed'])
        status = "✓ PASS" if latest['passed'] else "✗ FAIL"
        print(f"\n{eid} ({latest.get('eval_name', '')})")
        print(f"  Latest: {status} | History: {passed}/{total} passed")
        if not latest['passed']:
            if latest.get('expected_misses'):
                print(f"  Missing: {latest['expected_misses'][0]}")
            if latest.get('must_not_violations'):
                print(f"  Violation: {latest['must_not_violations'][0]}")
    
    # Overall
    total_runs = len(results)
    total_passed = sum(1 for r in results if r['passed'])
    print(f"\n{'='*60}")
    print(f"OVERALL: {total_passed}/{total_runs} passed ({100*total_passed//max(total_runs,1)}%)")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description='PE Agent OS eval runner')
    parser.add_argument('--eval', help='Eval ID to score (pipe agent output to stdin)')
    parser.add_argument('--list', action='store_true', help='List all eval IDs')
    parser.add_argument('--summary', action='store_true', help='Show pass/fail history')
    args = parser.parse_args()
    
    # Read skill file
    if not SKILL_FILE.exists():
        print(f"ERROR: SKILL.md not found at {SKILL_FILE}", file=sys.stderr)
        sys.exit(1)
    
    skill_text = SKILL_FILE.read_text()
    
    # Get skill name and version from frontmatter
    skill_name_match = re.search(r'^name:\s+(\S+)', skill_text, re.MULTILINE)
    version_match = re.search(r'^version:\s+(\S+)', skill_text, re.MULTILINE)
    skill_name = skill_name_match.group(1) if skill_name_match else SKILL_DIR.name
    version = version_match.group(1) if version_match else '0.0.0'
    
    evals = parse_evals_from_skill(skill_text)
    
    if args.summary:
        print_summary()
        return
    
    if args.list:
        print(f"\nEvals in {skill_name} v{version}:")
        for e in evals:
            print(f"  {e['id']}: {e.get('name', '')}")
        return
    
    if args.eval:
        # Find the eval case
        eval_case = next((e for e in evals if e['id'] == args.eval), None)
        if not eval_case:
            print(f"ERROR: eval '{args.eval}' not found. Run --list to see available evals.")
            sys.exit(1)
        
        # Read agent output from stdin
        if sys.stdin.isatty():
            print(f"Paste agent output for eval '{args.eval}', then press Ctrl+D:")
        output = sys.stdin.read()
        
        if not output.strip():
            print("ERROR: No output provided.", file=sys.stderr)
            sys.exit(1)
        
        result = score_output(output, eval_case)
        entry = log_result(args.eval, eval_case.get('name', ''), result, skill_name, version)
        
        # Print result
        status = "✓ PASS" if result['passed'] else "✗ FAIL"
        print(f"\n{status} — {args.eval}: {eval_case.get('name', '')}")
        print(f"Score: {result['score']:.0%}")
        
        if result['expected_misses']:
            print(f"\nMissing expected items:")
            for m in result['expected_misses']:
                print(f"  - {m}")
        
        if result['must_not_violations']:
            print(f"\nMust-not violations:")
            for v in result['must_not_violations']:
                print(f"  - {v}")
        
        if result['passed']:
            print(f"\nResult logged to {EVAL_LOG}")
        else:
            print(f"\nResult logged. Run /improve-skill to address failures.")
        
        return
    
    # No args — print help
    parser.print_help()


if __name__ == '__main__':
    main()
