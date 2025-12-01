import json
import os
import sys
import subprocess
import re

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'problems_with_hidden_tests.json')

data = json.load(open(file_path, encoding='utf-8-sig'))

def test_solution(code, test_input, expected_output):
    """solution_code를 실행해서 expected_output과 비교"""
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
        return actual == expected, actual, result.stderr
    except Exception as e:
        return False, str(e), ""

def analyze_input_format(input_str):
    """입력 형식 분석"""
    lines = input_str.strip().split('\n')
    analysis = {
        'num_lines': len(lines),
        'lines': []
    }
    for line in lines:
        parts = line.split()
        analysis['lines'].append({
            'raw': line,
            'parts': len(parts),
            'types': [guess_type(p) for p in parts]
        })
    return analysis

def guess_type(s):
    """문자열의 타입 추측"""
    try:
        int(s)
        return 'int'
    except:
        pass
    try:
        float(s)
        return 'float'
    except:
        pass
    return 'str'

# 실패한 문제들 상세 분석
print("=== DETAILED ANALYSIS OF FAILED PROBLEMS ===\n")

failed_problems = []
for p in data:
    pid = p['problem_id']
    examples = p.get('examples', [])
    solutions = p.get('solutions', [])

    if not examples or not solutions:
        continue

    ex = examples[0]
    sol = solutions[0]
    code = sol.get('solution_code', '')

    success, actual, err = test_solution(code, ex['input'], ex['output'])

    if not success:
        failed_problems.append({
            'problem_id': pid,
            'title': p['title'],
            'description': p.get('description', '')[:200],
            'input_desc': p.get('input_description', '')[:200],
            'example_input': ex['input'],
            'example_output': ex['output'],
            'solution_code': code,
            'actual_output': actual,
            'error': err[:300] if err else '',
            'input_analysis': analyze_input_format(ex['input'])
        })

print(f"Total failed: {len(failed_problems)} out of {len(data)}\n")

# 처음 20개 실패 케이스 상세 출력
for i, fp in enumerate(failed_problems[:20]):
    print(f"{'='*60}")
    print(f"[{fp['problem_id']}] {fp['title']}")
    print(f"{'='*60}")
    print(f"Description: {fp['description'][:100]}...")
    print(f"\nInput format: {fp['input_analysis']}")
    print(f"\nExample Input:\n{fp['example_input']}")
    print(f"\nExpected Output: {fp['example_output']}")
    print(f"\nActual Output: {fp['actual_output']}")
    print(f"\nSolution Code:\n{fp['solution_code'][:500]}")
    if fp['error']:
        print(f"\nError: {fp['error']}")
    print()
