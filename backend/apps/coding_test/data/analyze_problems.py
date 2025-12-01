import json
import os
import sys
import subprocess
import re

sys.stdout.reconfigure(encoding='utf-8')

if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'problems_with_hidden_tests.json')

data = json.load(open(file_path, encoding='utf-8-sig'))

# === INPUT PATTERN ANALYSIS ===
print('=== INPUT PATTERN ANALYSIS ===')
input_patterns = {}
for p in data[:50]:  # 처음 50개 분석
    for ex in p.get('examples', []):
        inp = ex.get('input', '')
        lines = inp.strip().split('\n')
        pattern = f"lines={len(lines)}"
        if len(lines) == 1:
            parts = lines[0].split()
            pattern += f", parts={len(parts)}"
        input_patterns[pattern] = input_patterns.get(pattern, 0) + 1

print("Input patterns (first 50 problems):")
for pat, cnt in sorted(input_patterns.items(), key=lambda x: -x[1]):
    print(f"  {pat}: {cnt}")

# === SOLUTION CODE VALIDATION ===
print('\n=== SOLUTION CODE VALIDATION (sample) ===')
def test_solution(code, test_input, expected_output):
    """solution_code를 실행해서 expected_output과 비교"""
    try:
        # \\n을 실제 줄바꿈으로 변환
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

# 처음 100개 문제 테스트
test_results = []
for p in data[:100]:
    pid = p['problem_id']
    title = p['title']
    examples = p.get('examples', [])
    solutions = p.get('solutions', [])

    if not examples or not solutions:
        continue

    ex = examples[0]
    sol = solutions[0]
    code = sol.get('solution_code', '')

    success, actual, err = test_solution(code, ex['input'], ex['output'])
    test_results.append({
        'pid': pid,
        'title': title,
        'success': success,
        'expected': ex['output'][:50],
        'actual': actual[:50] if actual else '',
        'error': err[:100] if err else ''
    })

success_count = sum(1 for r in test_results if r['success'])
fail_count = len(test_results) - success_count
print(f"Tested {len(test_results)} problems: {success_count} passed, {fail_count} failed ({fail_count/len(test_results)*100:.1f}% failure rate)")

# 실패 원인 분류
error_types = {
    'ValueError': 0,
    'EOFError': 0,
    'TypeError': 0,
    'Wrong Answer': 0,
    'Other': 0
}
for r in test_results:
    if r['success']:
        continue
    err = r['error']
    if 'ValueError' in err:
        error_types['ValueError'] += 1
    elif 'EOFError' in err:
        error_types['EOFError'] += 1
    elif 'TypeError' in err:
        error_types['TypeError'] += 1
    elif not err and r['actual']:
        error_types['Wrong Answer'] += 1
    else:
        error_types['Other'] += 1

print("\nError type breakdown:")
for etype, cnt in error_types.items():
    if cnt > 0:
        print(f"  {etype}: {cnt}")

print("\nFailed problems:")
for r in test_results:
    if not r['success']:
        print(f"  ✗ [{r['pid']}] {r['title']}")

print('\n=== DESCRIPTION QUALITY CHECK ===')
empty_desc = [p['problem_id'] for p in data if not p.get('description') or len(p.get('description','')) < 10]
print(f'Empty/short descriptions: {len(empty_desc)}')

empty_input_desc = [p['problem_id'] for p in data if not p.get('input_description')]
print(f'Missing input_description: {len(empty_input_desc)}')

empty_output_desc = [p['problem_id'] for p in data if not p.get('output_description')]
print(f'Missing output_description: {len(empty_output_desc)}')

print('\n=== EXAMPLES CHECK ===')
no_examples = [p['problem_id'] for p in data if not p.get('examples') or len(p.get('examples',[])) == 0]
print(f'Problems with no examples: {len(no_examples)}')

empty_example_output = []
for p in data:
    for ex in p.get('examples', []):
        if ex.get('output', '') == '':
            empty_example_output.append(p['problem_id'])
            break
print(f'Problems with empty example output: {len(empty_example_output)}')
if empty_example_output[:10]: print(f'  IDs: {empty_example_output[:10]}')

print('\n=== HIDDEN TEST CASES CHECK ===')
no_hidden = [p['problem_id'] for p in data if not p.get('hidden_test_cases') or len(p.get('hidden_test_cases',[])) == 0]
print(f'Problems with no hidden_test_cases: {len(no_hidden)}')

empty_hidden_output = []
for p in data:
    for tc in p.get('hidden_test_cases', []):
        if tc.get('output', '') == '':
            empty_hidden_output.append(p['problem_id'])
            break
print(f'Problems with empty hidden output: {len(empty_hidden_output)}')
if empty_hidden_output[:10]: print(f'  IDs: {empty_hidden_output[:10]}')

hidden_counts = {}
for p in data:
    cnt = len(p.get('hidden_test_cases', []))
    hidden_counts[cnt] = hidden_counts.get(cnt, 0) + 1
print(f'Hidden test case count distribution: {dict(sorted(hidden_counts.items()))}')

print('\n=== TAGS ANALYSIS ===')
all_tags = {}
for p in data:
    for tag in p.get('tags', []):
        all_tags[tag] = all_tags.get(tag, 0) + 1

print(f'Total unique tags: {len(all_tags)}')
sorted_tags = sorted(all_tags.items(), key=lambda x: -x[1])
print('Top 30 tags:')
for tag, count in sorted_tags[:30]:
    print(f'  {tag}: {count}')

print('\nAll tags:')
for tag, count in sorted_tags:
    print(f'  {tag}: {count}')
