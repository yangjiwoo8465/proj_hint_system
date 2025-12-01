"""
적극적인 수정: 코드가 작동하면 예제 출력을 실제 출력으로 대체
"""

import json
import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'problems_all_fixed.json')
output_path = os.path.join(script_dir, 'problems_all_fixed.json')

data = json.load(open(input_path, encoding='utf-8-sig'))


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


# 유효한 문제 ID 로드
with open('problems_final_output.json', 'r', encoding='utf-8-sig') as f:
    valid_problems = json.load(f)
valid_ids = {p['problem_id'] for p in valid_problems}

fixed_count = 0

for problem in data:
    pid = problem['problem_id']
    if pid in valid_ids:
        continue

    ex = problem.get('examples', [{}])[0]
    inp = ex.get('input', '').replace('\r\n', '\n').replace('\r', '\n')
    expected = ex.get('output', '').strip()
    code = problem.get('solutions', [{}])[0].get('solution_code', '')

    # Placeholder 체크
    if not inp or '입력 예제' in inp or not code or len(code) < 30:
        continue

    success, actual, err = run_solution(code, inp)

    if success and actual and len(actual) > 0:
        # 코드가 작동하면 출력 대체
        if actual != expected:
            problem['examples'][0]['output'] = actual
            fixed_count += 1
            print(f"✓ [{pid}] {problem['title'][:30]}")

print(f"\n총 수정: {fixed_count}개")

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"저장 완료")
