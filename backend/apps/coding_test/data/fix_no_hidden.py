"""
Hidden test cases가 부족한 문제들에 대해 hidden test 생성
"""

import json
import os
import sys
import subprocess
import random

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'problems_final_output.json')
output_path = os.path.join(script_dir, 'problems_final_output.json')

data = json.load(open(input_path, encoding='utf-8-sig'))


def run_solution(code, test_input, timeout=5):
    try:
        test_input = test_input.replace('\r\n', '\n').replace('\r', '\n')
        result = subprocess.run(
            ['python', '-c', code],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, ""
    except:
        return False, ""


def analyze_input(input_str):
    """입력 형식 분석"""
    lines = input_str.strip().split('\n')
    analysis = {'lines': []}
    for line in lines:
        parts = line.split()
        types = []
        for p in parts:
            try:
                int(p)
                types.append('int')
            except:
                try:
                    float(p)
                    types.append('float')
                except:
                    types.append('str')
        analysis['lines'].append({
            'parts': parts,
            'types': types
        })
    return analysis


def generate_hidden_tests(code, analysis, num=8):
    """Hidden test cases 생성"""
    tests = []
    attempts = 0

    while len(tests) < num and attempts < num * 10:
        attempts += 1

        new_lines = []
        for line in analysis['lines']:
            if not line['parts']:
                new_lines.append('')
                continue

            new_parts = []
            for val, t in zip(line['parts'], line['types']):
                if t == 'int':
                    orig = int(val)
                    if abs(orig) <= 10:
                        new_parts.append(str(random.randint(max(1, orig-5), orig+5)))
                    elif abs(orig) <= 100:
                        new_parts.append(str(random.randint(1, 100)))
                    else:
                        new_parts.append(str(random.randint(1, min(abs(orig) * 2, 10000))))
                elif t == 'float':
                    new_parts.append(str(round(random.uniform(0, float(val) * 2), 2)))
                else:
                    if val.isalpha():
                        chars = 'abcdefghijklmnopqrstuvwxyz'
                        if val.isupper():
                            chars = chars.upper()
                        new_parts.append(''.join(random.choice(chars) for _ in range(len(val))))
                    else:
                        new_parts.append(val)
            new_lines.append(' '.join(new_parts))

        test_input = '\n'.join(new_lines)

        if any(t['input'] == test_input for t in tests):
            continue

        success, output = run_solution(code, test_input)
        if success and output:
            tests.append({'input': test_input, 'output': output})

    return tests


print("=== Hidden Test Cases 생성 시작 ===\n")

generated_count = 0

for p in data:
    if p.get('invalid_reason') != 'insufficient_hidden':
        continue

    pid = p['problem_id']
    ex = p.get('examples', [{}])[0]
    inp = ex.get('input', '')
    code = p.get('solutions', [{}])[0].get('solution_code', '')

    if not inp or not code:
        continue

    analysis = analyze_input(inp)
    existing = p.get('hidden_test_cases', [])
    needed = 8 - len(existing)

    if needed > 0:
        new_tests = generate_hidden_tests(code, analysis, needed)
        if new_tests:
            p['hidden_test_cases'] = existing + new_tests
            if len(p['hidden_test_cases']) >= 5:
                p['is_valid'] = True
                p['invalid_reason'] = ''
                generated_count += 1
                print(f"✓ [{pid}] {p['title'][:30]} - hidden: {len(p['hidden_test_cases'])}개")

print(f"\n생성 완료: {generated_count}개 문제")

# 재검증
valid_count = sum(1 for p in data if p.get('is_valid'))
print(f"현재 유효한 문제: {valid_count}/{len(data)}")

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"저장 완료")
