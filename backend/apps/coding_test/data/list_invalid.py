# -*- coding: utf-8 -*-
"""무효 문제 목록 출력"""
import json
import sys
import subprocess
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('problems_final_output.json', encoding='utf-8-sig'))

def run_solution(code, test_input, timeout=5):
    try:
        test_input = test_input.replace('\r\n', '\n').replace('\r', '\n')
        result = subprocess.run(
            ['python', '-c', code],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)

print("=== 무효 문제 상세 목록 ===\n")

for p in data:
    if p.get('is_valid'):
        continue

    pid = p['problem_id']
    title = p.get('title', '')[:30]
    reason = p.get('invalid_reason', '')
    level = p.get('level', 0)

    ex = p.get('examples', [{}])[0]
    inp = ex.get('input', '')[:50].replace('\n', '\\n')
    out = ex.get('output', '')[:50].replace('\n', '\\n')
    code = p.get('solutions', [{}])[0].get('solution_code', '')
    hidden_count = len(p.get('hidden_test_cases', []))

    print(f"[{pid}] {title}")
    print(f"  Level: {level}, Reason: {reason}")
    print(f"  Input: {inp}")
    print(f"  Expected: {out}")
    print(f"  Code len: {len(code)}, Hidden: {hidden_count}")

    if code and inp and reason == 'solution_failed':
        success, actual, err = run_solution(code, inp)
        if success:
            print(f"  Actual: {actual[:50]}")
        else:
            print(f"  Error: {err[:100]}")
    print()
