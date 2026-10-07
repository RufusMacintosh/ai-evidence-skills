"""Reproduce synthetic CLI examples and tests without a model or network."""
import json
from pathlib import Path
import platform
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs' / 'results'


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    cases = [
        ('evidence-valid', 'skills/review-with-evidence/scripts/verify_evidence.py',
         'examples/evidence-synthetic.json', 0),
        ('evidence-fabricated', 'skills/review-with-evidence/scripts/verify_evidence.py',
         'examples/evidence-fabricated-synthetic.json', 1),
        ('power-mismatch', 'skills/gd-power-hedge/scripts/analyze_coverage.py',
         'examples/power-synthetic.json', 0),
        ('power-duplicate', 'skills/gd-power-hedge/scripts/analyze_coverage.py',
         'examples/power-duplicate-synthetic.json', 1),
    ]
    receipt = {'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
               'python_version': platform.python_version(),
               'data_kind': 'synthetic fixtures; not real papers or market data',
               'cases': []}
    success = True
    for name, script, fixture, expected in cases:
        args = [script, fixture]
        result = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)
        parsed = json.loads(result.stdout)
        (OUTPUT / f'{name}.json').write_text(json.dumps(parsed, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        passed = result.returncode == expected
        success = success and passed
        receipt['cases'].append({'name': name, 'command_args': args,
                                 'expected_exit_code': expected, 'actual_exit_code': result.returncode,
                                 'exit_code_matches': passed, 'stderr': result.stderr})
    args = ['-m', 'unittest', 'discover', '-s', 'tests', '-v']
    result = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)
    (OUTPUT / 'unit-tests.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
    receipt['unit_tests'] = {'command_args': args, 'exit_code': result.returncode,
                             'log': 'unit-tests.txt'}
    success = success and result.returncode == 0
    receipt['all_commands_matched_expected_exit_codes'] = success
    (OUTPUT / 'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'ok': success, 'results_directory': str(OUTPUT)}, ensure_ascii=False))
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
