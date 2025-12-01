"""
모든 문제를 다시 검증 (입력의 \r\n을 \n으로 변환)
"""

import json
import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'problems_all_fixed.json')

data = json.load(open(input_path, encoding='utf-8-sig'))


def run_solution(code, test_input, timeout=5):
    try:
        # 입력의 \r\n을 \n으로 변환
        test_input = test_input.replace('\r\n', '\n').replace('\r', '\n')
        code = code.replace('\\n', '\n')
        result = subprocess.run(
            ['python', '-c', code],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return True, result.stdout.strip(), result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)


def test_solution(code, test_input, expected_output):
    success, actual, err = run_solution(code, test_input)
    if not success:
        return False, actual, err
    # 출력도 정규화
    expected = expected_output.strip().replace('\r\n', '\n').replace('\r', '\n')
    return actual == expected, actual, err


# 검증
valid_count = 0
invalid_count = 0
invalid_list = []

for i, p in enumerate(data):
    ex = p.get('examples', [{}])[0]
    code = p.get('solutions', [{}])[0].get('solution_code', '')

    success, actual, err = test_solution(code, ex.get('input', ''), ex.get('output', ''))

    if success:
        valid_count += 1
    else:
        invalid_count += 1
        if len(invalid_list) < 30:
            invalid_list.append({
                'pid': p['problem_id'],
                'title': p['title'],
                'level': p.get('level', 'N/A'),
                'expected': ex.get('output', '')[:50],
                'actual': actual[:50] if actual else 'N/A',
                'error': err[:80] if err else 'Wrong Answer'
            })

    if (i + 1) % 200 == 0:
        print(f"Progress: {i + 1}/{len(data)}")

print(f"\n=== 결과 ===")
print(f"Valid: {valid_count}")
print(f"Invalid: {invalid_count}")
print(f"Total: {len(data)}")

print(f"\n=== Invalid 샘플 ===")
for p in invalid_list[:20]:
    print(f"\n[{p['pid']}] {p['title']} (Lv.{p['level']})")
    print(f"  Expected: {p['expected']}")
    print(f"  Actual: {p['actual']}")
    print(f"  Error: {p['error']}")
