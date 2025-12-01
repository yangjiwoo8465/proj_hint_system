# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open(r'C:\Users\playdata2\Desktop\playdata\Workspace\팀프로젝트5\5th-project_mvp\backend\apps\coding_test\data\problems_final_output.json', encoding='utf-8-sig'))

valid = sum(1 for p in data if p.get('is_valid'))
invalid = len(data) - valid

print('=' * 60)
print('              최종 문제 데이터 검증')
print('=' * 60)
print(f'총 문제 수: {len(data)}')
print(f'유효한 문제: {valid} ({valid/len(data)*100:.1f}%)')
print(f'무효한 문제: {invalid}')

# 무효 문제 있으면 표시
if invalid > 0:
    print('\n[무효 문제 목록]')
    for p in data:
        if not p.get('is_valid'):
            print(f"  [{p['problem_id']}] {p.get('title','')} - {p.get('invalid_reason','')}")

# 태그별 분포
print('\n' + '=' * 60)
print('              태그별 문제 분포')
print('=' * 60)
tag_count = {}
for p in data:
    for tag in p.get('tags', []):
        tag_count[tag] = tag_count.get(tag, 0) + 1

sorted_tags = sorted(tag_count.items(), key=lambda x: -x[1])
for tag, cnt in sorted_tags:
    print(f'  {tag:40s}: {cnt:3d}개')

print('\n' + '=' * 60)
print(f'총 태그 종류: {len(tag_count)}개')
print('=' * 60)
