"""
레벨 1-5 중 남은 invalid 문제들 상세 분석
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


# 레벨 1-10 invalid 문제 수집
easy_invalid = []

for p in data:
    level = p.get('level', 99)
    if level > 10:
        continue

    examples = p.get('examples', [])
    solutions = p.get('solutions', [])

    if not examples or not solutions:
        continue

    ex = examples[0]
    code = solutions[0].get('solution_code', '')

    success, actual, err = test_solution(code, ex.get('input', ''), ex.get('output', ''))

    if not success:
        easy_invalid.append({
            'problem_id': p['problem_id'],
            'title': p['title'],
            'level': level,
            'tags': p.get('tags', []),
            'input': ex.get('input', ''),
            'expected': ex.get('output', ''),
            'actual': actual,
            'error': err,
            'code': code
        })

print(f"=== 레벨 1-10 Invalid 문제 ({len(easy_invalid)}개) ===\n")

for p in easy_invalid:
    print(f"\n{'='*60}")
    print(f"[{p['problem_id']}] {p['title']} (레벨 {p['level']})")
    print(f"태그: {', '.join(p['tags'][:5])}")
    print(f"\n입력:")
    for line in p['input'].split('\n')[:5]:
        print(f"  {line}")
    if len(p['input'].split('\n')) > 5:
        print(f"  ... ({len(p['input'].split(chr(10)))} lines)")
    print(f"\n기대 출력: {p['expected'][:100]}...")
    print(f"실제 출력: {p['actual'][:100] if p['actual'] else 'N/A'}...")
    print(f"에러: {p['error'][:100] if p['error'] else 'N/A'}")
    print(f"\n코드 (처음 20줄):")
    code_lines = p['code'].split('\n')[:20]
    for i, line in enumerate(code_lines, 1):
        print(f"  {i:3d} | {line}")
