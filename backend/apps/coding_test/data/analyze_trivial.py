# -*- coding: utf-8 -*-
"""
Trivial solution 문제 분석 및 수정 계획
"""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

INPUT_FILE = r'C:\Users\playdata2\Desktop\playdata\Workspace\팀프로젝트5\5th-project_mvp\backend\apps\coding_test\data\problems_final_output.json'

data = json.load(open(INPUT_FILE, encoding='utf-8-sig'))

# trivial solution 찾기
trivial_patterns = ['print(0)', 'print(1)', 'print(-1)', 'print("YES")', 'print("NO")', 'print(12)']
trivial_problems = []

for p in data:
    solutions = p.get('solutions', [])
    if not solutions:
        continue
    code = solutions[0].get('solution_code', '').strip()

    # 매우 짧은 코드 (50자 미만)이면서 단순 출력
    if len(code) < 50:
        is_trivial = False
        for pattern in trivial_patterns:
            if pattern in code:
                is_trivial = True
                break
        if code.startswith('print(') and len(code) < 20:
            is_trivial = True

        if is_trivial:
            trivial_problems.append({
                'id': p['problem_id'],
                'title': p['title'],
                'level': p.get('level', 0),
                'tags': p.get('tags', []),
                'code': code,
                'category': p.get('category', ''),
                'description': p.get('description', '')[:200],
                'examples': p.get('examples', [])
            })

print(f'Trivial solution 문제: {len(trivial_problems)}개')
print()
print('=' * 80)

# 카테고리별 분류
by_category = {}
for tp in trivial_problems:
    cat = tp['category']
    if cat not in by_category:
        by_category[cat] = []
    by_category[cat].append(tp)

for cat, probs in sorted(by_category.items(), key=lambda x: -len(x[1])):
    print(f"\n[{cat}] - {len(probs)}개")
    for p in probs[:5]:
        print(f"  {p['id']:>6s} | {p['title'][:30]:30s} | L{p['level']:2d} | {p['tags'][:3]}")

# 상세 분석 (처음 10개)
print()
print('=' * 80)
print("상세 분석 (처음 20개)")
print('=' * 80)

for tp in trivial_problems[:20]:
    print(f"\n[{tp['id']}] {tp['title']}")
    print(f"  레벨: {tp['level']} | 카테고리: {tp['category']}")
    print(f"  태그: {tp['tags']}")
    print(f"  현재 코드: {tp['code']}")
    if tp['examples']:
        ex = tp['examples'][0]
        print(f"  예시 입력: {ex.get('input', '')[:50]}")
        print(f"  예시 출력: {ex.get('output', '')[:50]}")
