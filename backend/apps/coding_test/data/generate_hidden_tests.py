"""
Hidden Test Cases 생성 스크립트

정상 작동하는 solution_code를 실행해서 hidden_test_cases를 생성합니다.
"""

import json
import os
import sys
import subprocess
import random
import re
from typing import Dict, List, Tuple, Any, Optional

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'problems_fixed.json')
output_path = os.path.join(script_dir, 'problems_with_generated_tests.json')

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


def generate_random_value(val_type: str, original_val: str, constraints: Dict = None) -> str:
    """랜덤 값 생성"""
    if val_type == 'int':
        orig = int(original_val)
        # 원본 값 범위에 기반한 랜덤 생성
        if orig == 0:
            return str(random.randint(0, 10))
        elif orig < 0:
            return str(random.randint(orig * 2, 0))
        elif orig <= 10:
            return str(random.randint(1, 10))
        elif orig <= 100:
            return str(random.randint(1, 100))
        elif orig <= 1000:
            return str(random.randint(1, 1000))
        else:
            return str(random.randint(1, min(orig * 2, 100000)))
    elif val_type == 'float':
        orig = float(original_val)
        return str(round(random.uniform(0, abs(orig) * 2), 2))
    else:
        # 문자열 - 원본과 비슷한 길이의 랜덤 문자열
        length = len(original_val)
        if original_val.isalpha():
            chars = 'abcdefghijklmnopqrstuvwxyz'
            if original_val.isupper():
                chars = chars.upper()
            return ''.join(random.choice(chars) for _ in range(length))
        elif original_val.isalnum():
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
            return ''.join(random.choice(chars) for _ in range(length))
        else:
            return original_val  # 특수 형식은 그대로 유지


def generate_test_input(analysis: Dict, variation: int = 0) -> str:
    """테스트 입력 생성"""
    lines = []
    for line_info in analysis['lines']:
        if not line_info['values']:
            lines.append('')
            continue

        new_parts = []
        for i, (val, val_type) in enumerate(zip(line_info['values'], line_info['types'])):
            if variation == 0:
                # 첫 번째 변형: 원본에 가까운 값
                new_val = generate_random_value(val_type, val)
            else:
                # 다른 변형: 더 다양한 값
                new_val = generate_random_value(val_type, val)
            new_parts.append(new_val)
        lines.append(' '.join(new_parts))

    return '\n'.join(lines)


def generate_hidden_test_cases(problem: Dict, num_cases: int = 8) -> List[Dict]:
    """hidden_test_cases 생성"""
    examples = problem.get('examples', [])
    solutions = problem.get('solutions', [])

    if not examples or not solutions:
        return []

    # 첫 번째 예제 분석
    example = examples[0]
    input_str = example.get('input', '')
    analysis = analyze_input_format(input_str)

    # solution_code
    code = solutions[0].get('solution_code', '')

    hidden_cases = []
    attempts = 0
    max_attempts = num_cases * 5  # 최대 시도 횟수

    while len(hidden_cases) < num_cases and attempts < max_attempts:
        attempts += 1

        # 테스트 입력 생성
        test_input = generate_test_input(analysis, variation=attempts % 3)

        # 중복 체크
        if any(tc['input'] == test_input for tc in hidden_cases):
            continue
        if any(ex.get('input') == test_input for ex in examples):
            continue

        # 솔루션 실행
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

    success, actual, err = run_solution(code, example.get('input', ''))
    if not success:
        return False

    expected = example.get('output', '').strip().replace('\r\n', '\n').replace('\r', '\n')
    return actual == expected


# 메인 실행
print("=== GENERATING HIDDEN TEST CASES ===\n")

generated_count = 0
skipped_invalid = 0
already_has_tests = 0

for i, problem in enumerate(data):
    pid = problem['problem_id']
    title = problem['title']

    # 이미 hidden_test_cases가 충분히 있는 경우 스킵
    existing_tests = problem.get('hidden_test_cases', [])
    if len(existing_tests) >= 5:
        already_has_tests += 1
        continue

    # solution_code 검증
    if not is_solution_valid(problem):
        skipped_invalid += 1
        continue

    # hidden_test_cases 생성
    num_needed = 8 - len(existing_tests)
    new_tests = generate_hidden_test_cases(problem, num_needed)

    if new_tests:
        problem['hidden_test_cases'] = existing_tests + new_tests
        generated_count += 1
        print(f"✓ [{pid}] {title}: generated {len(new_tests)} test cases")

    # 진행 상황 출력
    if (i + 1) % 100 == 0:
        print(f"Progress: {i + 1}/{len(data)}")

print(f"\n=== SUMMARY ===")
print(f"Already has tests: {already_has_tests}")
print(f"Generated new tests: {generated_count}")
print(f"Skipped (invalid solution): {skipped_invalid}")
print(f"Total: {len(data)}")

# 저장
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved to: {output_path}")
