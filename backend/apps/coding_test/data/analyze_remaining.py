"""
남은 invalid 문제들 상세 분석
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
    expected = expected_output.strip().replace('\r\n', '\n').replace('\r', '\n')
    return actual == expected, actual, err


# Invalid 문제 수집
invalid_problems = []

for p in data:
    examples = p.get('examples', [])
    solutions = p.get('solutions', [])

    if not examples or not solutions:
        continue

    ex = examples[0]
    code = solutions[0].get('solution_code', '')

    success, actual, err = test_solution(code, ex.get('input', ''), ex.get('output', ''))

    if not success:
        invalid_problems.append({
            'problem_id': p['problem_id'],
            'title': p['title'],
            'level': p.get('level', 'N/A'),
            'tags': p.get('tags', []),
            'input': ex.get('input', ''),
            'expected': ex.get('output', ''),
            'actual': actual,
            'error': err,
            'code': code[:200] + '...' if len(code) > 200 else code
        })

print(f"=== 남은 Invalid 문제 분석 ({len(invalid_problems)}개) ===\n")

# 입력 형식별 분류
input_patterns = {}
for p in invalid_problems:
    inp = p['input']
    lines = inp.strip().split('\n')
    pattern = []
    for line in lines[:3]:  # 처음 3줄만
        parts = line.split()
        part_types = []
        for part in parts:
            try:
                int(part)
                part_types.append('int')
            except:
                try:
                    float(part)
                    part_types.append('float')
                except:
                    part_types.append('str')
        pattern.append(f"{len(parts)}:{','.join(part_types)}" if part_types else "empty")

    pattern_key = ' | '.join(pattern)
    if pattern_key not in input_patterns:
        input_patterns[pattern_key] = []
    input_patterns[pattern_key].append(p)

print("=== 입력 패턴별 분류 ===")
for pattern, probs in sorted(input_patterns.items(), key=lambda x: -len(x[1]))[:30]:
    print(f"\n[{len(probs)}개] {pattern}")
    for p in probs[:3]:
        print(f"  - [{p['problem_id']}] {p['title']}")
        print(f"    입력: {p['input'][:50]}...")
        print(f"    기대: {p['expected'][:30]}...")
        if p['error']:
            print(f"    에러: {p['error'][:50]}")

# 레벨별 분포
print("\n\n=== 레벨별 분포 ===")
level_dist = {}
for p in invalid_problems:
    lvl = p['level']
    level_dist[lvl] = level_dist.get(lvl, 0) + 1

for lvl in sorted(level_dist.keys()):
    print(f"  레벨 {lvl}: {level_dist[lvl]}문제")

# 태그별 분포 (상위 20개)
print("\n=== 태그별 분포 (상위 20개) ===")
tag_dist = {}
for p in invalid_problems:
    for tag in p['tags']:
        tag_dist[tag] = tag_dist.get(tag, 0) + 1

for tag, cnt in sorted(tag_dist.items(), key=lambda x: -x[1])[:20]:
    print(f"  {tag}: {cnt}")

# 에러 유형별 분포
print("\n=== 에러 유형별 분포 ===")
error_types = {}
for p in invalid_problems:
    err = p['error']
    if 'ValueError' in err:
        err_type = 'ValueError'
    elif 'IndexError' in err:
        err_type = 'IndexError'
    elif 'EOFError' in err:
        err_type = 'EOFError'
    elif 'Timeout' in err:
        err_type = 'Timeout'
    elif err:
        err_type = 'Other Error'
    else:
        err_type = 'Wrong Answer'

    error_types[err_type] = error_types.get(err_type, 0) + 1

for err_type, cnt in sorted(error_types.items(), key=lambda x: -x[1]):
    print(f"  {err_type}: {cnt}")

# 샘플 문제들 상세 출력
print("\n\n=== 샘플 문제 상세 (처음 20개) ===")
for p in invalid_problems[:20]:
    print(f"\n[{p['problem_id']}] {p['title']} (레벨 {p['level']})")
    print(f"  태그: {', '.join(p['tags'][:5])}")
    print(f"  입력:\n    {p['input'].replace(chr(10), chr(10) + '    ')}")
    print(f"  기대 출력: {p['expected'][:80]}")
    print(f"  실제 출력: {p['actual'][:80] if p['actual'] else 'N/A'}")
    print(f"  에러: {p['error'][:100] if p['error'] else 'N/A'}")
    print(f"  코드: {p['code'][:100]}...")
