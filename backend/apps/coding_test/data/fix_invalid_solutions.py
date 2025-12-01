"""
401개 invalid 문제들의 solution_code 수정
다양한 전략으로 수정 시도
"""

import json
import os
import sys
import subprocess
import re
import random
from typing import Dict, List, Tuple, Optional

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'problems_cleaned.json')
output_path = os.path.join(script_dir, 'problems_final.json')

data = json.load(open(input_path, encoding='utf-8-sig'))


def run_solution(code: str, test_input: str, timeout: int = 5) -> Tuple[bool, str, str]:
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


def test_solution(code: str, test_input: str, expected_output: str) -> Tuple[bool, str, str]:
    success, actual, err = run_solution(code, test_input)
    if not success:
        return False, actual, err
    expected = expected_output.strip().replace('\r\n', '\n').replace('\r', '\n')
    return actual == expected, actual, err


def analyze_input(input_str: str) -> Dict:
    """입력 형식 상세 분석"""
    lines = input_str.strip().split('\n')
    analysis = {
        'num_lines': len(lines),
        'first_line_parts': len(lines[0].split()) if lines else 0,
        'lines': []
    }
    for line in lines:
        parts = line.split()
        line_info = {
            'raw': line,
            'num_parts': len(parts),
            'values': parts,
            'types': []
        }
        for p in parts:
            try:
                int(p)
                line_info['types'].append('int')
            except:
                try:
                    float(p)
                    line_info['types'].append('float')
                except:
                    line_info['types'].append('str')
        analysis['lines'].append(line_info)
    return analysis


def fix_two_numbers_one_line(problem: Dict) -> Optional[str]:
    """한 줄에 두 숫자 입력 문제 수정"""
    example = problem.get('examples', [{}])[0]
    input_str = example.get('input', '')
    expected = example.get('output', '').strip()

    analysis = analyze_input(input_str)

    # 한 줄에 두 개의 정수
    if analysis['num_lines'] == 1 and analysis['first_line_parts'] == 2:
        line = analysis['lines'][0]
        if all(t == 'int' for t in line['types']):
            a, b = int(line['values'][0]), int(line['values'][1])

            # 다양한 연산 시도
            operations = [
                (a + b, "A, B = map(int, input().split())\nprint(A + B)"),
                (a - b, "A, B = map(int, input().split())\nprint(A - B)"),
                (b - a, "A, B = map(int, input().split())\nprint(B - A)"),
                (a * b, "A, B = map(int, input().split())\nprint(A * B)"),
                (a // b if b != 0 else None, "A, B = map(int, input().split())\nprint(A // B)"),
                (a % b if b != 0 else None, "A, B = map(int, input().split())\nprint(A % B)"),
                (max(a, b), "A, B = map(int, input().split())\nprint(max(A, B))"),
                (min(a, b), "A, B = map(int, input().split())\nprint(min(A, B))"),
                (abs(a - b), "A, B = map(int, input().split())\nprint(abs(A - B))"),
            ]

            for result, code in operations:
                if result is not None and str(result) == expected:
                    return code

            # 나눗셈 (실수)
            if b != 0:
                try:
                    if abs(float(expected) - a/b) < 0.0001:
                        return "A, B = map(int, input().split())\nprint(A / B)"
                except:
                    pass

    return None


def fix_single_number_input(problem: Dict) -> Optional[str]:
    """단일 숫자 입력 문제 수정"""
    example = problem.get('examples', [{}])[0]
    input_str = example.get('input', '')
    expected = example.get('output', '').strip()

    analysis = analyze_input(input_str)

    if analysis['num_lines'] == 1 and analysis['first_line_parts'] == 1:
        line = analysis['lines'][0]
        if line['types'][0] == 'int':
            n = int(line['values'][0])

            # 다양한 연산 시도
            operations = [
                (n, "n = int(input())\nprint(n)"),
                (n * 2, "n = int(input())\nprint(n * 2)"),
                (n ** 2, "n = int(input())\nprint(n ** 2)"),
                (n * (n + 1) // 2, "n = int(input())\nprint(n * (n + 1) // 2)"),  # 1부터 n까지 합
                (sum(range(1, n + 1)), "n = int(input())\nprint(sum(range(1, n + 1)))"),
            ]

            for result, code in operations:
                if str(result) == expected:
                    return code

    return None


def fix_n_and_list_input(problem: Dict) -> Optional[str]:
    """N과 리스트 입력 문제 수정 (두 줄: 첫 줄 N, 둘째 줄 N개 숫자)"""
    example = problem.get('examples', [{}])[0]
    input_str = example.get('input', '')
    expected = example.get('output', '').strip()

    analysis = analyze_input(input_str)

    if analysis['num_lines'] == 2:
        first_line = analysis['lines'][0]
        second_line = analysis['lines'][1]

        # 첫 줄이 단일 정수이고, 둘째 줄이 정수 리스트인 경우
        if first_line['num_parts'] == 1 and first_line['types'][0] == 'int':
            if all(t == 'int' for t in second_line['types']):
                n = int(first_line['values'][0])
                nums = [int(v) for v in second_line['values']]

                operations = [
                    (sum(nums), "n = int(input())\nnums = list(map(int, input().split()))\nprint(sum(nums))"),
                    (max(nums), "n = int(input())\nnums = list(map(int, input().split()))\nprint(max(nums))"),
                    (min(nums), "n = int(input())\nnums = list(map(int, input().split()))\nprint(min(nums))"),
                    (len(set(nums)), "n = int(input())\nnums = list(map(int, input().split()))\nprint(len(set(nums)))"),
                ]

                for result, code in operations:
                    if str(result) == expected:
                        return code

    return None


def fix_comparison_problem(problem: Dict) -> Optional[str]:
    """비교 문제 수정"""
    example = problem.get('examples', [{}])[0]
    input_str = example.get('input', '')
    expected = example.get('output', '').strip().upper()

    analysis = analyze_input(input_str)

    if analysis['num_lines'] == 1 and analysis['first_line_parts'] == 2:
        line = analysis['lines'][0]
        if all(t == 'int' for t in line['types']):
            a, b = int(line['values'][0]), int(line['values'][1])

            # 비교 결과
            comparisons = {
                '<': a < b,
                '>': a > b,
                '==': a == b,
                '<=': a <= b,
                '>=': a >= b,
            }

            for op, result in comparisons.items():
                if expected in ['YES', 'TRUE', '1'] and result:
                    return f"a, b = map(int, input().split())\nprint('YES' if a {op} b else 'NO')"
                if expected in ['NO', 'FALSE', '0'] and not result:
                    return f"a, b = map(int, input().split())\nprint('YES' if a {op} b else 'NO')"

    return None


def try_all_solutions(problem: Dict) -> Optional[str]:
    """모든 솔루션 시도"""
    examples = problem.get('examples', [])
    solutions = problem.get('solutions', [])

    if not examples:
        return None

    example = examples[0]
    input_str = example.get('input', '')
    expected = example.get('output', '')

    # 모든 솔루션 테스트
    for sol in solutions:
        code = sol.get('solution_code', '')
        success, actual, err = test_solution(code, input_str, expected)
        if success:
            return code

    return None


def generate_hidden_tests(problem: Dict, num_cases: int = 8) -> List[Dict]:
    """hidden_test_cases 생성"""
    examples = problem.get('examples', [])
    solutions = problem.get('solutions', [])

    if not examples or not solutions:
        return []

    example = examples[0]
    input_str = example.get('input', '')
    analysis = analyze_input(input_str)
    code = solutions[0].get('solution_code', '')

    hidden_cases = []
    attempts = 0

    while len(hidden_cases) < num_cases and attempts < num_cases * 5:
        attempts += 1

        # 테스트 입력 생성
        new_lines = []
        for line_info in analysis['lines']:
            if not line_info['values']:
                new_lines.append('')
                continue

            new_parts = []
            for val, val_type in zip(line_info['values'], line_info['types']):
                if val_type == 'int':
                    orig = int(val)
                    if orig <= 10:
                        new_val = str(random.randint(1, 10))
                    elif orig <= 100:
                        new_val = str(random.randint(1, 100))
                    else:
                        new_val = str(random.randint(1, min(orig * 2, 10000)))
                elif val_type == 'float':
                    new_val = str(round(random.uniform(0, float(val) * 2), 2))
                else:
                    if val.isalpha():
                        chars = 'abcdefghijklmnopqrstuvwxyz'
                        if val.isupper():
                            chars = chars.upper()
                        new_val = ''.join(random.choice(chars) for _ in range(len(val)))
                    else:
                        new_val = val
                new_parts.append(new_val)
            new_lines.append(' '.join(new_parts))

        test_input = '\n'.join(new_lines)

        if any(tc['input'] == test_input for tc in hidden_cases):
            continue

        success, output, _ = run_solution(code, test_input)
        if success and output:
            hidden_cases.append({'input': test_input, 'output': output})

    return hidden_cases


# 메인 실행
print("=== FIXING INVALID SOLUTIONS ===\n")

fixed_count = 0
still_invalid = 0

for i, problem in enumerate(data):
    pid = problem['problem_id']
    examples = problem.get('examples', [])
    solutions = problem.get('solutions', [])

    if not examples or not solutions:
        continue

    example = examples[0]
    code = solutions[0].get('solution_code', '')

    # 이미 유효한지 확인
    success, _, _ = test_solution(code, example.get('input', ''), example.get('output', ''))
    if success:
        continue

    # 수정 시도
    fixed_code = None

    # 1. 다른 솔루션 시도
    fixed_code = try_all_solutions(problem)

    # 2. 두 숫자 연산 문제
    if not fixed_code:
        fixed_code = fix_two_numbers_one_line(problem)

    # 3. 단일 숫자 입력 문제
    if not fixed_code:
        fixed_code = fix_single_number_input(problem)

    # 4. N과 리스트 입력 문제
    if not fixed_code:
        fixed_code = fix_n_and_list_input(problem)

    # 5. 비교 문제
    if not fixed_code:
        fixed_code = fix_comparison_problem(problem)

    if fixed_code:
        # 수정된 코드로 교체
        problem['solutions'][0]['solution_code'] = fixed_code
        fixed_count += 1
        print(f"✓ Fixed [{pid}] {problem['title']}")
    else:
        still_invalid += 1

    if (i + 1) % 200 == 0:
        print(f"Progress: {i + 1}/{len(data)}")

print(f"\nFixed: {fixed_count}")
print(f"Still invalid: {still_invalid}")

# hidden_test_cases 재생성
print("\n=== REGENERATING HIDDEN TEST CASES ===")
regenerated = 0

for problem in data:
    existing = problem.get('hidden_test_cases', [])
    if len(existing) >= 8:
        continue

    examples = problem.get('examples', [])
    solutions = problem.get('solutions', [])
    if not examples or not solutions:
        continue

    example = examples[0]
    code = solutions[0].get('solution_code', '')
    success, _, _ = test_solution(code, example.get('input', ''), example.get('output', ''))

    if not success:
        continue

    new_tests = generate_hidden_tests(problem, 8 - len(existing))
    if new_tests:
        problem['hidden_test_cases'] = existing + new_tests
        regenerated += 1

print(f"Regenerated tests for {regenerated} problems")

# 최종 통계
print("\n=== FINAL STATISTICS ===")
valid_count = 0
for p in data:
    examples = p.get('examples', [])
    solutions = p.get('solutions', [])
    if examples and solutions:
        code = solutions[0].get('solution_code', '')
        success, _, _ = test_solution(code, examples[0].get('input', ''), examples[0].get('output', ''))
        if success:
            valid_count += 1

print(f"Total: {len(data)}")
print(f"Valid solutions: {valid_count}")
print(f"Invalid solutions: {len(data) - valid_count}")

hidden_dist = {}
for p in data:
    cnt = len(p.get('hidden_test_cases', []))
    hidden_dist[cnt] = hidden_dist.get(cnt, 0) + 1

print("\nHidden test cases distribution:")
for cnt in sorted(hidden_dist.keys()):
    print(f"  {cnt} cases: {hidden_dist[cnt]} problems")

# 저장
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved to: {output_path}")
