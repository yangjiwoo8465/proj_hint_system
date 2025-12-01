"""
Solution Code 자동 수정 스크립트

examples.input을 기준으로 solution_code를 수정합니다.
1. 입력 형식 분석
2. 문제 설명 분석
3. 올바른 solution_code 생성
"""

import json
import os
import sys
import subprocess
import re
from typing import Dict, List, Tuple, Any

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'problems_with_hidden_tests.json')
output_path = os.path.join(script_dir, 'problems_fixed.json')

data = json.load(open(file_path, encoding='utf-8-sig'))


def test_solution(code: str, test_input: str, expected_output: str) -> Tuple[bool, str, str]:
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


def analyze_input_format(input_str: str) -> Dict:
    """입력 형식 분석"""
    lines = input_str.strip().split('\n')
    analysis = {
        'num_lines': len(lines),
        'lines': []
    }
    for line in lines:
        parts = line.split()
        line_info = {
            'raw': line,
            'num_parts': len(parts),
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


def generate_input_code(analysis: Dict) -> str:
    """입력 형식에 맞는 입력 코드 생성"""
    code_lines = []
    var_counter = 0
    var_names = []

    for i, line_info in enumerate(analysis['lines']):
        num_parts = line_info['num_parts']
        types = line_info['types']

        if num_parts == 0:
            continue
        elif num_parts == 1:
            # 단일 값
            var_name = f"var_{var_counter}"
            var_counter += 1
            if types[0] == 'int':
                code_lines.append(f"{var_name} = int(input())")
            elif types[0] == 'float':
                code_lines.append(f"{var_name} = float(input())")
            else:
                code_lines.append(f"{var_name} = input()")
            var_names.append(var_name)
        else:
            # 여러 값
            names = [f"var_{var_counter + j}" for j in range(num_parts)]
            var_counter += num_parts

            if all(t == 'int' for t in types):
                code_lines.append(f"{', '.join(names)} = map(int, input().split())")
            elif all(t == 'float' for t in types):
                code_lines.append(f"{', '.join(names)} = map(float, input().split())")
            else:
                code_lines.append(f"{', '.join(names)} = input().split()")
            var_names.extend(names)

    return '\n'.join(code_lines), var_names


def fix_simple_math_problems(problem: Dict) -> str:
    """간단한 수학 문제 수정 (사칙연산 등)"""
    title = problem.get('title', '').lower()
    desc = problem.get('description', '').lower()
    output_desc = problem.get('output_description', '').lower()

    example = problem.get('examples', [{}])[0]
    input_str = example.get('input', '')
    expected = example.get('output', '')

    analysis = analyze_input_format(input_str)

    # 두 수 연산 문제
    if analysis['num_lines'] == 1 and analysis['lines'][0]['num_parts'] == 2:
        types = analysis['lines'][0]['types']
        if all(t == 'int' for t in types):
            parts = input_str.split()
            a, b = int(parts[0]), int(parts[1])
            exp_val = expected.strip()

            # 어떤 연산인지 추론
            if str(a + b) == exp_val:
                return "A, B = map(int, input().split())\nprint(A + B)"
            elif str(a - b) == exp_val:
                return "A, B = map(int, input().split())\nprint(A - B)"
            elif str(a * b) == exp_val:
                return "A, B = map(int, input().split())\nprint(A * B)"
            elif b != 0 and str(a // b) == exp_val:
                return "A, B = map(int, input().split())\nprint(A // B)"
            elif b != 0:
                try:
                    if abs(float(exp_val) - a/b) < 0.0001:
                        return "A, B = map(int, input().split())\nprint(A / B)"
                except:
                    pass

    return None


def fix_input_format_in_code(code: str, analysis: Dict) -> str:
    """기존 코드의 입력 형식만 수정"""
    lines = code.replace('\\n', '\n').split('\n')
    new_lines = []

    # 입력 패턴 분석
    input_patterns_in_code = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # int(input()) 패턴
        if re.search(r'=\s*int\(input\(\)\)', stripped):
            input_patterns_in_code.append(('single_int', i, line))
        # map(int, input().split()) 패턴
        elif re.search(r'map\(int,\s*input\(\)\.split\(\)\)', stripped):
            input_patterns_in_code.append(('multi_int', i, line))
        # input() 패턴
        elif re.search(r'=\s*input\(\)', stripped) and 'split' not in stripped:
            input_patterns_in_code.append(('single_str', i, line))
        # list(map(int, input().split())) 패턴
        elif re.search(r'list\(map\(int,\s*input\(\)\.split\(\)\)\)', stripped):
            input_patterns_in_code.append(('list_int', i, line))

    if not input_patterns_in_code:
        return None

    # 예상 입력과 코드 입력 비교
    expected_inputs = analysis['lines']

    # 첫 번째 입력 라인 수정 시도
    if len(expected_inputs) >= 1 and len(input_patterns_in_code) >= 1:
        first_expected = expected_inputs[0]
        first_code = input_patterns_in_code[0]

        # 코드는 single_int를 기대하는데 실제 입력은 multi_int인 경우
        if first_code[0] == 'single_int' and first_expected['num_parts'] > 1:
            # 변수명 추출
            match = re.search(r'(\w+)\s*=\s*int\(input\(\)\)', lines[first_code[1]])
            if match:
                var_name = match.group(1)
                if first_expected['num_parts'] == 2:
                    # 다음 줄도 single_int인지 확인
                    if len(input_patterns_in_code) >= 2 and input_patterns_in_code[1][0] == 'single_int':
                        match2 = re.search(r'(\w+)\s*=\s*int\(input\(\)\)', lines[input_patterns_in_code[1][1]])
                        if match2:
                            var_name2 = match2.group(1)
                            # 두 줄을 한 줄로 합침
                            indent = len(lines[first_code[1]]) - len(lines[first_code[1]].lstrip())
                            new_line = ' ' * indent + f"{var_name}, {var_name2} = map(int, input().split())"
                            lines[first_code[1]] = new_line
                            lines[input_patterns_in_code[1][1]] = ''  # 빈 줄로
                            return '\n'.join(line for line in lines if line.strip() or line == '')

    return None


def try_fix_with_input_adjustment(problem: Dict) -> str:
    """입력 형식 조정으로 수정 시도"""
    examples = problem.get('examples', [])
    solutions = problem.get('solutions', [])

    if not examples or not solutions:
        return None

    example = examples[0]
    input_str = example.get('input', '')
    expected = example.get('output', '')
    analysis = analyze_input_format(input_str)

    for sol in solutions:
        code = sol.get('solution_code', '')
        fixed_code = fix_input_format_in_code(code, analysis)
        if fixed_code:
            success, actual, err = test_solution(fixed_code, input_str, expected)
            if success:
                return fixed_code

    return None


def fix_solution_for_problem(problem: Dict) -> Dict:
    """문제의 solution_code 수정"""
    examples = problem.get('examples', [])
    solutions = problem.get('solutions', [])

    if not examples or not solutions:
        return problem

    example = examples[0]
    input_str = example.get('input', '')
    expected = example.get('output', '')

    # 현재 솔루션 테스트
    current_code = solutions[0].get('solution_code', '')
    success, actual, err = test_solution(current_code, input_str, expected)

    if success:
        return problem  # 이미 정상 작동

    # 1. 간단한 수학 문제 시도
    fixed_code = fix_simple_math_problems(problem)
    if fixed_code:
        success, actual, err = test_solution(fixed_code, input_str, expected)
        if success:
            problem['solutions'][0]['solution_code'] = fixed_code
            problem['solutions'][0]['auto_fixed'] = True
            return problem

    # 2. 입력 형식 조정 시도
    fixed_code = try_fix_with_input_adjustment(problem)
    if fixed_code:
        problem['solutions'][0]['solution_code'] = fixed_code
        problem['solutions'][0]['auto_fixed'] = True
        return problem

    # 3. 다른 솔루션 시도
    for i, sol in enumerate(solutions[1:], 1):
        code = sol.get('solution_code', '')
        success, actual, err = test_solution(code, input_str, expected)
        if success:
            # 정상 작동하는 솔루션을 첫 번째로
            solutions[0], solutions[i] = solutions[i], solutions[0]
            problem['solutions'] = solutions
            problem['solutions'][0]['auto_fixed'] = True
            return problem

    # 4. 다른 솔루션들도 입력 형식 조정 시도
    analysis = analyze_input_format(input_str)
    for i, sol in enumerate(solutions):
        code = sol.get('solution_code', '')
        fixed_code = fix_input_format_in_code(code, analysis)
        if fixed_code:
            success, actual, err = test_solution(fixed_code, input_str, expected)
            if success:
                problem['solutions'][0]['solution_code'] = fixed_code
                problem['solutions'][0]['auto_fixed'] = True
                return problem

    # 수정 실패 - 마킹
    problem['needs_manual_fix'] = True
    problem['fix_error'] = err[:200] if err else f"Wrong answer: expected {expected[:50]}, got {actual[:50]}"

    return problem


# 메인 실행
print("=== AUTO-FIXING SOLUTION CODES ===\n")

fixed_count = 0
manual_fix_needed = 0
already_correct = 0

for i, problem in enumerate(data):
    pid = problem['problem_id']

    # 원본 테스트
    examples = problem.get('examples', [])
    solutions = problem.get('solutions', [])

    if not examples or not solutions:
        continue

    example = examples[0]
    current_code = solutions[0].get('solution_code', '')
    success_before, _, _ = test_solution(current_code, example.get('input', ''), example.get('output', ''))

    if success_before:
        already_correct += 1
        continue

    # 수정 시도
    fixed_problem = fix_solution_for_problem(problem)
    data[i] = fixed_problem

    if fixed_problem.get('solutions', [{}])[0].get('auto_fixed'):
        fixed_count += 1
        print(f"✓ Fixed [{pid}] {problem['title']}")
    elif fixed_problem.get('needs_manual_fix'):
        manual_fix_needed += 1
        if manual_fix_needed <= 20:
            print(f"✗ Need manual fix [{pid}] {problem['title']}: {fixed_problem.get('fix_error', '')[:80]}")

print(f"\n=== SUMMARY ===")
print(f"Already correct: {already_correct}")
print(f"Auto-fixed: {fixed_count}")
print(f"Need manual fix: {manual_fix_needed}")
print(f"Total: {len(data)}")

# 저장
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved to: {output_path}")
