# -*- coding: utf-8 -*-
"""최종 결과 요약"""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('problems_final_output.json', encoding='utf-8-sig'))

valid = sum(1 for p in data if p.get('is_valid'))
invalid = len(data) - valid

print("=" * 50)
print("        최종 문제 데이터 요약")
print("=" * 50)
print(f"\n총 문제 수: {len(data)}")
print(f"유효한 문제: {valid} ({valid/len(data)*100:.1f}%)")
print(f"무효한 문제: {invalid} ({invalid/len(data)*100:.1f}%)")

# 레벨별 분포
print("\n" + "=" * 50)
print("        레벨별 문제 분포")
print("=" * 50)
level_stats = {}
for p in data:
    lvl = p.get('level', 0)
    if lvl not in level_stats:
        level_stats[lvl] = {'total': 0, 'valid': 0}
    level_stats[lvl]['total'] += 1
    if p.get('is_valid'):
        level_stats[lvl]['valid'] += 1

for lvl in sorted(level_stats.keys()):
    stats = level_stats[lvl]
    valid_pct = stats['valid'] / stats['total'] * 100 if stats['total'] > 0 else 0
    print(f"  Level {lvl:2d}: {stats['valid']:3d}/{stats['total']:3d} 유효 ({valid_pct:5.1f}%)")

# 태그별 분포 (상위 20개)
print("\n" + "=" * 50)
print("        태그별 문제 분포 (상위 20개)")
print("=" * 50)
tag_stats = {}
for p in data:
    for tag in p.get('tags', []):
        if tag not in tag_stats:
            tag_stats[tag] = {'total': 0, 'valid': 0}
        tag_stats[tag]['total'] += 1
        if p.get('is_valid'):
            tag_stats[tag]['valid'] += 1

sorted_tags = sorted(tag_stats.items(), key=lambda x: -x[1]['total'])[:20]
for tag, stats in sorted_tags:
    valid_pct = stats['valid'] / stats['total'] * 100 if stats['total'] > 0 else 0
    print(f"  {tag[:25]:25s}: {stats['valid']:3d}/{stats['total']:3d} 유효 ({valid_pct:5.1f}%)")

# 무효 문제 이유
print("\n" + "=" * 50)
print("        무효 문제 이유 분석")
print("=" * 50)
reasons = {}
for p in data:
    if not p.get('is_valid'):
        r = p.get('invalid_reason', 'unknown')
        reasons[r] = reasons.get(r, 0) + 1

for r, c in sorted(reasons.items(), key=lambda x: -x[1]):
    print(f"  {r:25s}: {c}개")

print("\n" + "=" * 50)
print("파일 저장 위치: problems_final_output.json")
print("=" * 50)
