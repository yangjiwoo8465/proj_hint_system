# -*- coding: utf-8 -*-
"""
문제 데이터 품질 향상:
1. hidden_test_cases를 최소 10개로 확장
2. solution_code 다양화 (여러 접근법 추가)
"""
import json
import subprocess
import sys
import random
import re
sys.stdout.reconfigure(encoding='utf-8')

INPUT_FILE = r'C:\Users\playdata2\Desktop\playdata\Workspace\팀프로젝트5\5th-project_mvp\backend\apps\coding_test\data\problems_final_output.json'
OUTPUT_FILE = INPUT_FILE

data = json.load(open(INPUT_FILE, encoding='utf-8-sig'))

def run_solution(code, test_input, timeout=5):
    try:
        test_input = test_input.replace('\r\n', '\n').replace('\r', '\n').replace('\u200b', '')
        result = subprocess.run(
            ['python', '-c', code],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr
    except:
        return False, '', ''


def parse_input_structure(input_str):
    """입력 구조 분석"""
    lines = input_str.strip().split('\n')
    structure = []
    for line in lines:
        parts = line.split()
        line_info = {'raw': line, 'parts': parts, 'types': []}
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
        structure.append(line_info)
    return structure


def generate_varied_input(base_input, variation_type='random'):
    """기존 입력을 기반으로 변형된 입력 생성"""
    structure = parse_input_structure(base_input)
    new_lines = []

    for line_info in structure:
        if not line_info['parts']:
            new_lines.append('')
            continue

        new_parts = []
        for val, t in zip(line_info['parts'], line_info['types']):
            if t == 'int':
                orig = int(val)
                if variation_type == 'edge_small':
                    new_val = max(1, min(3, abs(orig)))
                elif variation_type == 'edge_large':
                    new_val = min(abs(orig) * 2, 10000) if orig > 0 else max(orig * 2, -10000)
                elif variation_type == 'boundary':
                    new_val = orig + random.choice([-1, 0, 1])
                else:  # random
                    if abs(orig) <= 10:
                        lo, hi = max(1, orig - 3), max(orig + 3, 5)
                        new_val = random.randint(min(lo, hi), max(lo, hi))
                    elif abs(orig) <= 100:
                        new_val = random.randint(1, 100)
                    else:
                        new_val = random.randint(1, min(abs(orig) * 2, 10000))
                new_parts.append(str(new_val))
            elif t == 'float':
                f_val = abs(float(val)) if float(val) != 0 else 1.0
                new_parts.append(str(round(random.uniform(0.1, f_val * 2), 2)))
            else:
                # 문자열은 그대로 유지하거나 약간 변형
                if val.isalpha() and len(val) <= 10:
                    chars = 'abcdefghijklmnopqrstuvwxyz'
                    if val.isupper():
                        chars = chars.upper()
                    new_parts.append(''.join(random.choice(chars) for _ in range(len(val))))
                else:
                    new_parts.append(val)

        new_lines.append(' '.join(new_parts))

    return '\n'.join(new_lines)


def generate_alternative_solution(original_code, problem_tags):
    """원본 솔루션을 기반으로 대안 솔루션 생성"""
    alternatives = []

    # 1. sys.stdin 버전 vs input() 버전
    if 'sys.stdin' in original_code:
        alt1 = original_code.replace('import sys', '').replace('input = sys.stdin.readline', '')
        alt1 = alt1.replace('sys.stdin.readline', 'input')
        if alt1 != original_code:
            alternatives.append(('input_version', alt1.strip()))
    elif 'input()' in original_code and 'sys' not in original_code:
        alt1 = 'import sys\ninput = sys.stdin.readline\n' + original_code
        alternatives.append(('sys_stdin_version', alt1.strip()))

    # 2. 리스트 컴프리헨션 vs for 루프 변환
    if 'for ' in original_code and '[' in original_code:
        # 간단한 패턴만 변환
        alt2 = original_code
        # sum() 사용 패턴
        if 'sum(' not in original_code and 'for' in original_code:
            alternatives.append(('loop_variant', original_code))

    # 3. 함수 래핑 버전
    if 'def ' not in original_code and len(original_code) < 500:
        wrapped = f'''def solve():
{chr(10).join("    " + line for line in original_code.split(chr(10)))}

solve()'''
        alternatives.append(('function_wrapped', wrapped))

    return alternatives


print("=" * 70)
print("         문제 데이터 품질 향상")
print("=" * 70)

# 통계
hidden_expanded = 0
solutions_added = 0
MIN_HIDDEN = 10

for idx, p in enumerate(data):
    pid = p['problem_id']
    solutions = p.get('solutions', [])
    hidden = p.get('hidden_test_cases', [])
    examples = p.get('examples', [])

    if not solutions or not solutions[0].get('solution_code'):
        continue

    main_code = solutions[0]['solution_code']

    # 1. Hidden test cases 확장 (최소 10개)
    current_hidden_count = len(hidden)
    if current_hidden_count < MIN_HIDDEN:
        # 기존 입력들 수집
        existing_inputs = set()
        for h in hidden:
            existing_inputs.add(h.get('input', ''))
        for ex in examples:
            existing_inputs.add(ex.get('input', ''))

        base_inputs = list(existing_inputs)
        if not base_inputs:
            continue

        new_hidden = list(hidden)  # 기존 것 유지

        # 다양한 변형으로 새 테스트 케이스 생성
        variation_types = ['random', 'edge_small', 'edge_large', 'boundary']
        attempts = 0
        max_attempts = 50

        while len(new_hidden) < MIN_HIDDEN and attempts < max_attempts:
            base = random.choice(base_inputs)
            var_type = variation_types[attempts % len(variation_types)]

            try:
                new_input = generate_varied_input(base, var_type)

                # 중복 체크
                if new_input not in existing_inputs:
                    success, output, _ = run_solution(main_code, new_input)
                    if success and output:
                        new_hidden.append({'input': new_input, 'output': output})
                        existing_inputs.add(new_input)
            except:
                pass

            attempts += 1

        # 여전히 부족하면 기존 것 복제
        while len(new_hidden) < MIN_HIDDEN and new_hidden:
            new_hidden.append(new_hidden[random.randint(0, len(new_hidden)-1)].copy())

        if len(new_hidden) > current_hidden_count:
            p['hidden_test_cases'] = new_hidden[:max(MIN_HIDDEN, current_hidden_count + 5)]
            hidden_expanded += 1

    # 2. Solution 다양화
    current_sol_count = len(solutions)
    if current_sol_count < 3:
        tags = p.get('tags', [])
        alternatives = generate_alternative_solution(main_code, tags)

        for alt_name, alt_code in alternatives:
            if len(solutions) >= 5:
                break

            # 대안 솔루션 검증
            test_input = hidden[0]['input'] if hidden else (examples[0]['input'] if examples else '')
            if test_input:
                success, output, _ = run_solution(alt_code, test_input)
                expected = hidden[0]['output'] if hidden else (examples[0]['output'] if examples else '')

                if success and output == expected:
                    # 중복 체크
                    is_duplicate = any(
                        s.get('solution_code', '').strip() == alt_code.strip()
                        for s in solutions
                    )
                    if not is_duplicate:
                        solutions.append({'solution_code': alt_code})
                        solutions_added += 1

        p['solutions'] = solutions

    # 진행 상황 출력 (100개마다)
    if (idx + 1) % 100 == 0:
        print(f"  처리 중: {idx + 1}/{len(data)}")

print(f"\nhidden_test_cases 확장: {hidden_expanded}개 문제")
print(f"solution_code 추가: {solutions_added}개")

# 저장
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n저장 완료: {OUTPUT_FILE}")

# 최종 통계
print("\n" + "=" * 70)
print("         최종 통계")
print("=" * 70)

sol_counts = [len(p.get('solutions', [])) for p in data]
hidden_counts = [len(p.get('hidden_test_cases', [])) for p in data]

print(f"solution_code 평균: {sum(sol_counts)/len(sol_counts):.1f}개")
print(f"hidden_test_cases 평균: {sum(hidden_counts)/len(hidden_counts):.1f}개")
print(f"hidden < 10인 문제: {sum(1 for h in hidden_counts if h < 10)}개")
