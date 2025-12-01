"""
전체 1039개 문제를 포함하는 최종 파일 생성
유효성 여부를 'is_valid' 필드로 표시
"""

import json
import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'problems_all_fixed.json')
output_path = os.path.join(script_dir, 'problems_final_output.json')

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
        return True, result.stdout.strip(), result.returncode == 0
    except:
        return False, "", False


def test_solution(code, test_input, expected_output):
    success, actual, ran_ok = run_solution(code, test_input)
    if not success or not ran_ok:
        return False
    expected = expected_output.strip().replace('\r\n', '\n').replace('\r', '\n')
    return actual == expected


print("=== 전체 문제 검증 시작 ===\n")

valid_count = 0
invalid_count = 0
invalid_reasons = {'placeholder': 0, 'no_code': 0, 'runtime_error': 0, 'wrong_answer': 0, 'no_hidden': 0}

for i, p in enumerate(data):
    pid = p['problem_id']
    examples = p.get('examples', [])
    solutions = p.get('solutions', [])
    hidden = p.get('hidden_test_cases', [])

    # 기본적으로 유효하지 않음
    p['is_valid'] = False
    p['invalid_reason'] = ''

    # 체크 1: 예제 데이터 존재
    if not examples or not examples[0].get('input') or not examples[0].get('output'):
        p['invalid_reason'] = 'no_example'
        invalid_reasons['placeholder'] += 1
        invalid_count += 1
        continue

    ex = examples[0]
    inp = ex.get('input', '')
    out = ex.get('output', '').strip()

    # 체크 2: placeholder 데이터
    if '입력 예제' in inp or '출력 예제' in out:
        p['invalid_reason'] = 'placeholder_data'
        invalid_reasons['placeholder'] += 1
        invalid_count += 1
        continue

    # 체크 3: 솔루션 코드 존재
    if not solutions or not solutions[0].get('solution_code'):
        p['invalid_reason'] = 'no_solution'
        invalid_reasons['no_code'] += 1
        invalid_count += 1
        continue

    code = solutions[0]['solution_code']
    if len(code) < 20:
        p['invalid_reason'] = 'invalid_code'
        invalid_reasons['no_code'] += 1
        invalid_count += 1
        continue

    # 체크 4: 솔루션 실행 테스트
    if not test_solution(code, inp, out):
        p['invalid_reason'] = 'solution_failed'
        invalid_reasons['runtime_error'] += 1
        invalid_count += 1
        continue

    # 체크 5: hidden_test_cases >= 5
    if len(hidden) < 5:
        p['invalid_reason'] = 'insufficient_hidden'
        invalid_reasons['no_hidden'] += 1
        invalid_count += 1
        continue

    # 모든 체크 통과
    p['is_valid'] = True
    valid_count += 1

    if (i + 1) % 200 == 0:
        print(f"Progress: {i + 1}/{len(data)}")

print(f"\n=== 결과 ===")
print(f"전체 문제: {len(data)}")
print(f"유효한 문제: {valid_count} ({valid_count/len(data)*100:.1f}%)")
print(f"유효하지 않은 문제: {invalid_count}")
print()
print("유효하지 않은 이유:")
for reason, count in invalid_reasons.items():
    print(f"  {reason}: {count}")

# 레벨별 유효 문제 분포
print("\n=== 레벨별 유효 문제 분포 ===")
level_valid = {}
level_total = {}
for p in data:
    lvl = p.get('level', 0)
    level_total[lvl] = level_total.get(lvl, 0) + 1
    if p.get('is_valid'):
        level_valid[lvl] = level_valid.get(lvl, 0) + 1

for lvl in sorted(level_total.keys()):
    v = level_valid.get(lvl, 0)
    t = level_total[lvl]
    print(f"  Level {lvl}: {v}/{t} ({v/t*100:.0f}%)")

# 전체 문제 저장 (is_valid 필드 포함)
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n저장 완료: {output_path}")
print(f"전체 {len(data)}개 문제 저장 (유효: {valid_count}, 무효: {invalid_count})")
