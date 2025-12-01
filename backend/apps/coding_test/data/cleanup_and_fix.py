"""
1. 미사용 속성 삭제 (solution_id, logic_steps 등)
2. 401개 문제 추가 수정 시도
3. hidden_test_cases 재생성
"""

import json
import os
import sys
import subprocess
import re
from typing import Dict, List, Tuple, Any, Optional

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'problems_with_generated_tests.json')
output_path = os.path.join(script_dir, 'problems_cleaned.json')

data = json.load(open(input_path, encoding='utf-8-sig'))


def run_solution(code: str, test_input: str, timeout: int = 5) -> Tuple[bool, str, str]:
    """solution_code 실행"""
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
    """solution_code 테스트"""
    success, actual, err = run_solution(code, test_input)
    if not success:
        return False, actual, err
    expected = expected_output.strip().replace('\r\n', '\n').replace('\r', '\n')
    return actual == expected, actual, err


def cleanup_solutions(problem: Dict) -> Dict:
    """solutions에서 미사용 속성 삭제"""
    solutions = problem.get('solutions', [])
    cleaned_solutions = []

    for sol in solutions:
        cleaned_sol = {
            'solution_name': sol.get('solution_name', ''),
            'solution_code': sol.get('solution_code', '')
        }
        # auto_fixed 플래그는 유지
        if sol.get('auto_fixed'):
            cleaned_sol['auto_fixed'] = True
        cleaned_solutions.append(cleaned_sol)

    problem['solutions'] = cleaned_solutions
    return problem


def cleanup_problem(problem: Dict) -> Dict:
    """문제에서 미사용 속성 삭제"""
    # needs_manual_fix, fix_error 삭제 (내부 플래그)
    problem.pop('needs_manual_fix', None)
    problem.pop('fix_error', None)

    # solutions 정리
    problem = cleanup_solutions(problem)

    return problem


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


def generate_test_input(analysis: Dict, variation: int = 0) -> str:
    """테스트 입력 생성"""
    import random
    lines = []
    for line_info in analysis['lines']:
        if not line_info['values']:
            lines.append('')
            continue

        new_parts = []
        for i, (val, val_type) in enumerate(zip(line_info['values'], line_info['types'])):
            if val_type == 'int':
                orig = int(val)
                if orig == 0:
                    new_val = str(random.randint(0, 10))
                elif orig < 0:
                    new_val = str(random.randint(orig * 2, 0))
                elif orig <= 10:
                    new_val = str(random.randint(1, 10))
                elif orig <= 100:
                    new_val = str(random.randint(1, 100))
                elif orig <= 1000:
                    new_val = str(random.randint(1, 1000))
                else:
                    new_val = str(random.randint(1, min(orig * 2, 100000)))
            elif val_type == 'float':
                orig = float(val)
                new_val = str(round(random.uniform(0, abs(orig) * 2), 2))
            else:
                # 문자열
                length = len(val)
                if val.isalpha():
                    chars = 'abcdefghijklmnopqrstuvwxyz'
                    if val.isupper():
                        chars = chars.upper()
                    new_val = ''.join(random.choice(chars) for _ in range(length))
                elif val.isalnum():
                    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
                    new_val = ''.join(random.choice(chars) for _ in range(length))
                else:
                    new_val = val
            new_parts.append(new_val)
        lines.append(' '.join(new_parts))

    return '\n'.join(lines)


def generate_hidden_test_cases(problem: Dict, num_cases: int = 8) -> List[Dict]:
    """hidden_test_cases 생성"""
    examples = problem.get('examples', [])
    solutions = problem.get('solutions', [])

    if not examples or not solutions:
        return []

    example = examples[0]
    input_str = example.get('input', '')
    analysis = analyze_input_format(input_str)
    code = solutions[0].get('solution_code', '')

    hidden_cases = []
    attempts = 0
    max_attempts = num_cases * 5

    while len(hidden_cases) < num_cases and attempts < max_attempts:
        attempts += 1
        test_input = generate_test_input(analysis, variation=attempts % 3)

        if any(tc['input'] == test_input for tc in hidden_cases):
            continue
        if any(ex.get('input') == test_input for ex in examples):
            continue

        success, output, err = run_solution(code, test_input)

        if success and output:
            hidden_cases.append({
                'input': test_input,
                'output': output
            })

    return hidden_cases


def is_solution_valid(problem: Dict) -> bool:
    """solution_code가 example과 일치하는지 확인"""
    examples = problem.get('examples', [])
    solutions = problem.get('solutions', [])

    if not examples or not solutions:
        return False

    example = examples[0]
    code = solutions[0].get('solution_code', '')

    success, actual, err = test_solution(code, example.get('input', ''), example.get('output', ''))
    return success


# 메인 실행
print("=== CLEANUP AND FIX ===\n")

# Step 1: 미사용 속성 삭제
print("Step 1: Removing unused attributes...")
for problem in data:
    cleanup_problem(problem)
print("Done.\n")

# Step 2: 현재 상태 확인
valid_count = 0
invalid_count = 0
for problem in data:
    if is_solution_valid(problem):
        valid_count += 1
    else:
        invalid_count += 1

print(f"Current status: {valid_count} valid, {invalid_count} invalid\n")

# Step 3: hidden_test_cases가 부족한 문제들 재생성
print("Step 3: Regenerating hidden_test_cases for valid problems...")
regenerated = 0
for i, problem in enumerate(data):
    existing_tests = problem.get('hidden_test_cases', [])

    # 이미 충분하면 스킵
    if len(existing_tests) >= 8:
        continue

    # solution_code가 유효하지 않으면 스킵
    if not is_solution_valid(problem):
        continue

    # hidden_test_cases 생성
    num_needed = 8 - len(existing_tests)
    new_tests = generate_hidden_test_cases(problem, num_needed)

    if new_tests:
        problem['hidden_test_cases'] = existing_tests + new_tests
        regenerated += 1

    if (i + 1) % 200 == 0:
        print(f"  Progress: {i + 1}/{len(data)}")

print(f"Regenerated tests for {regenerated} problems\n")

# Step 4: 최종 통계
print("=== FINAL STATISTICS ===")
print(f"Total problems: {len(data)}")

hidden_counts = {}
for p in data:
    cnt = len(p.get('hidden_test_cases', []))
    hidden_counts[cnt] = hidden_counts.get(cnt, 0) + 1

print("\nHidden test cases distribution:")
for cnt in sorted(hidden_counts.keys()):
    print(f"  {cnt} cases: {hidden_counts[cnt]} problems")

valid_with_tests = sum(1 for p in data if is_solution_valid(p) and len(p.get('hidden_test_cases', [])) >= 5)
print(f"\nComplete problems (valid + >=5 hidden tests): {valid_with_tests}")

# 저장
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved to: {output_path}")
