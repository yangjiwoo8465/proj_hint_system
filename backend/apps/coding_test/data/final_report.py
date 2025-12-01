"""
최종 결과 리포트 및 유효한 문제만 추출
"""

import json
import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'problems_final.json')
valid_output_path = os.path.join(script_dir, 'problems_valid_only.json')

data = json.load(open(input_path, encoding='utf-8-sig'))


def test_solution(code, test_input, expected_output):
    try:
        code = code.replace('\\n', '\n')
        result = subprocess.run(
            ['python', '-c', code],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=5
        )
        actual = result.stdout.strip()
        expected = expected_output.strip().replace('\r\n', '\n').replace('\r', '\n')
        return actual == expected
    except:
        return False


# 유효한 문제만 필터링
valid_problems = []
invalid_problems = []

for p in data:
    examples = p.get('examples', [])
    solutions = p.get('solutions', [])
    hidden = p.get('hidden_test_cases', [])

    if not examples or not solutions:
        invalid_problems.append(p)
        continue

    code = solutions[0].get('solution_code', '')
    is_valid = test_solution(code, examples[0].get('input', ''), examples[0].get('output', ''))

    if is_valid and len(hidden) >= 5:
        valid_problems.append(p)
    else:
        invalid_problems.append(p)

print("=" * 60)
print("최종 결과 리포트")
print("=" * 60)

print(f"\n전체 문제 수: {len(data)}")
print(f"유효한 문제 (solution 정상 + hidden >= 5): {len(valid_problems)}")
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

# 유효하지 않은 문제 중 일부 출력
print("\n=== 유효하지 않은 문제 샘플 (처음 10개) ===")
for p in invalid_problems[:10]:
    pid = p.get('problem_id', 'N/A')
    title = p.get('title', 'N/A')
    hidden_cnt = len(p.get('hidden_test_cases', []))
    print(f"  [{pid}] {title} (hidden: {hidden_cnt})")

# 유효한 문제만 저장
with open(valid_output_path, 'w', encoding='utf-8') as f:
    json.dump(valid_problems, f, ensure_ascii=False, indent=2)

print(f"\n유효한 문제만 저장: {valid_output_path}")
print(f"저장된 문제 수: {len(valid_problems)}")
