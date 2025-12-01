"""
최종 처리:
1. hidden_test_cases 재생성
2. 유효한 문제만 추출
3. 최종 통계 출력
"""

import json
import os
import sys
import subprocess
import random

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'problems_all_fixed.json')
output_path = os.path.join(script_dir, 'problems_final_output.json')

data = json.load(open(input_path, encoding='utf-8-sig'))


def run_solution(code, test_input, timeout=5):
    try:
        # 입력 정규화: \r\n -> \n
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
        return False
    expected = expected_output.strip().replace('\r\n', '\n').replace('\r', '\n')
    return actual == expected


def analyze_input(input_str):
    lines = input_str.strip().split('\n')
    analysis = {'lines': []}
    for line in lines:
        parts = line.split()
        types = []
        for p in parts:
            try:
                int(p)
                types.append('int')
            except:
                try:
                    float(p)
                    types.append('float')
                except:
                    types.append('str')
        analysis['lines'].append({
            'parts': parts,
            'types': types
        })
    return analysis


def generate_hidden_tests(code, analysis, num=8):
    tests = []
    attempts = 0

    while len(tests) < num and attempts < num * 5:
        attempts += 1

        new_lines = []
        for line in analysis['lines']:
            if not line['parts']:
                new_lines.append('')
                continue

            new_parts = []
            for val, t in zip(line['parts'], line['types']):
                if t == 'int':
                    orig = int(val)
                    if orig <= 10:
                        new_parts.append(str(random.randint(1, 10)))
                    elif orig <= 100:
                        new_parts.append(str(random.randint(1, 100)))
                    else:
                        new_parts.append(str(random.randint(1, min(orig * 2, 10000))))
                elif t == 'float':
                    new_parts.append(str(round(random.uniform(0, float(val) * 2), 2)))
                else:
                    if val.isalpha():
                        chars = 'abcdefghijklmnopqrstuvwxyz'
                        if val.isupper():
                            chars = chars.upper()
                        new_parts.append(''.join(random.choice(chars) for _ in range(len(val))))
                    else:
                        new_parts.append(val)
            new_lines.append(' '.join(new_parts))

        test_input = '\n'.join(new_lines)

        if any(t['input'] == test_input for t in tests):
            continue

        success, output, _ = run_solution(code, test_input)
        if success and output:
            tests.append({'input': test_input, 'output': output})

    return tests


# 유효한 문제 추출 및 hidden_test_cases 재생성
print("=== 최종 처리 시작 ===\n")

valid_problems = []
invalid_problems = []
regenerated = 0

for i, p in enumerate(data):
    examples = p.get('examples', [])
    solutions = p.get('solutions', [])

    if not examples or not solutions:
        invalid_problems.append(p)
        continue

    ex = examples[0]
    code = solutions[0].get('solution_code', '')

    if not test_solution(code, ex.get('input', ''), ex.get('output', '')):
        invalid_problems.append(p)
        continue

    # hidden_test_cases 확인 및 재생성
    existing = p.get('hidden_test_cases', [])
    if len(existing) < 5:
        analysis = analyze_input(ex.get('input', ''))
        new_tests = generate_hidden_tests(code, analysis, 8 - len(existing))
        if new_tests:
            p['hidden_test_cases'] = existing + new_tests
            regenerated += 1

    # 최소 5개의 hidden_test_cases가 있어야 유효
    if len(p.get('hidden_test_cases', [])) >= 5:
        valid_problems.append(p)
    else:
        invalid_problems.append(p)

    if (i + 1) % 200 == 0:
        print(f"Progress: {i + 1}/{len(data)}")

print(f"\nRegenerated hidden tests for {regenerated} problems")

# 최종 통계
print("\n" + "=" * 60)
print("최종 결과")
print("=" * 60)

print(f"\n전체 문제 수: {len(data)}")
print(f"유효한 문제 (solution OK + hidden >= 5): {len(valid_problems)}")
print(f"유효하지 않은 문제: {len(invalid_problems)}")

# 레벨별 분포
print("\n=== 레벨별 유효 문제 분포 ===")
level_dist = {}
for p in valid_problems:
    lvl = p.get('level', 'N/A')
    level_dist[lvl] = level_dist.get(lvl, 0) + 1

for lvl in sorted(level_dist.keys()):
    print(f"  레벨 {lvl}: {level_dist[lvl]}문제")

# 태그별 분포 (상위 20개)
print("\n=== 태그별 유효 문제 분포 (상위 20개) ===")
tag_dist = {}
for p in valid_problems:
    for tag in p.get('tags', []):
        tag_dist[tag] = tag_dist.get(tag, 0) + 1

sorted_tags = sorted(tag_dist.items(), key=lambda x: -x[1])[:20]
for tag, cnt in sorted_tags:
    print(f"  {tag}: {cnt}")

# hidden_test_cases 분포
print("\n=== Hidden Test Cases 분포 ===")
hidden_dist = {}
for p in valid_problems:
    cnt = len(p.get('hidden_test_cases', []))
    hidden_dist[cnt] = hidden_dist.get(cnt, 0) + 1

for cnt in sorted(hidden_dist.keys()):
    print(f"  {cnt}개: {hidden_dist[cnt]}문제")

# 유효한 문제만 저장
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(valid_problems, f, ensure_ascii=False, indent=2)

print(f"\n유효한 문제만 저장: {output_path}")
print(f"저장된 문제 수: {len(valid_problems)}")

# Invalid 문제 샘플
print("\n=== 유효하지 않은 문제 샘플 (처음 15개) ===")
for p in invalid_problems[:15]:
    pid = p.get('problem_id', 'N/A')
    title = p.get('title', 'N/A')
    level = p.get('level', 'N/A')
    hidden_cnt = len(p.get('hidden_test_cases', []))
    print(f"  [{pid}] {title} (레벨 {level}, hidden: {hidden_cnt})")
