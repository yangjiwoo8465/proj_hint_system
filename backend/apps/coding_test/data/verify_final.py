"""
최종 출력 파일 검증
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'problems_final_output.json')

data = json.load(open(file_path, encoding='utf-8-sig'))

print(f"총 문제 수: {len(data)}")

print("\n샘플 문제 (처음 3개):")
for p in data[:3]:
    print(f"  [{p['problem_id']}] {p['title']}")
    print(f"    레벨: {p['level']}")
    print(f"    태그: {p['tags'][:5]}")
    print(f"    hidden_test_cases: {len(p.get('hidden_test_cases', []))}개")
    print()

print("\n레벨 범위:", min(p['level'] for p in data), "-", max(p['level'] for p in data))

# 모든 문제에 필수 필드가 있는지 확인
required_fields = ['problem_id', 'title', 'level', 'tags', 'description', 'examples', 'solutions', 'hidden_test_cases']
missing = []
for p in data:
    for field in required_fields:
        if field not in p:
            missing.append((p['problem_id'], field))

if missing:
    print(f"\n경고: {len(missing)}개의 누락된 필드가 있습니다:")
    for pid, field in missing[:10]:
        print(f"  [{pid}] {field}")
else:
    print("\n모든 필수 필드가 존재합니다.")

# hidden_test_cases 검증
min_hidden = min(len(p.get('hidden_test_cases', [])) for p in data)
max_hidden = max(len(p.get('hidden_test_cases', [])) for p in data)
print(f"\nhidden_test_cases 범위: {min_hidden} - {max_hidden}개")

# solution_code 검증
empty_solutions = [p['problem_id'] for p in data if not p.get('solutions', [{}])[0].get('solution_code')]
if empty_solutions:
    print(f"\n경고: {len(empty_solutions)}개의 빈 solution_code가 있습니다")
else:
    print("\n모든 문제에 solution_code가 있습니다.")

print("\n검증 완료!")
