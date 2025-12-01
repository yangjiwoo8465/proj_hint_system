import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'problems_with_generated_tests.json')

data = json.load(open(file_path, encoding='utf-8-sig'))

print('=== FINAL STATISTICS ===')
print(f'Total problems: {len(data)}')

# hidden_test_cases 분포
hidden_counts = {}
for p in data:
    cnt = len(p.get('hidden_test_cases', []))
    hidden_counts[cnt] = hidden_counts.get(cnt, 0) + 1
print(f'\nHidden test cases distribution:')
for cnt in sorted(hidden_counts.keys()):
    print(f'  {cnt} cases: {hidden_counts[cnt]} problems')

# 0개인 문제들
no_hidden = [p['problem_id'] for p in data if len(p.get('hidden_test_cases', [])) == 0]
print(f'\nProblems with 0 hidden tests: {len(no_hidden)}')
if no_hidden[:10]:
    print(f'  First 10: {no_hidden[:10]}')

# needs_manual_fix 개수
needs_fix = sum(1 for p in data if p.get('needs_manual_fix'))
print(f'\nNeeds manual fix: {needs_fix}')

# auto_fixed 개수
auto_fixed = sum(1 for p in data if p.get('solutions', [{}])[0].get('auto_fixed'))
print(f'Auto-fixed: {auto_fixed}')

# 완전한 문제 (hidden_test_cases >= 5 and no needs_manual_fix)
complete = sum(1 for p in data if len(p.get('hidden_test_cases', [])) >= 5 and not p.get('needs_manual_fix'))
print(f'\nComplete problems (>=5 hidden tests, no fix needed): {complete}')
