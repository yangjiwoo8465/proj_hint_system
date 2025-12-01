# -*- coding: utf-8 -*-
"""현재 상태 확인"""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('problems_final_output.json', encoding='utf-8-sig'))

valid = sum(1 for p in data if p.get('is_valid'))
invalid = len(data) - valid

print(f"Total: {len(data)}")
print(f"Valid: {valid}")
print(f"Invalid: {invalid}")
print()

# Invalid reasons
reasons = {}
for p in data:
    if not p.get('is_valid'):
        r = p.get('invalid_reason', 'unknown')
        reasons[r] = reasons.get(r, 0) + 1

print("Invalid reasons:")
for r, c in sorted(reasons.items(), key=lambda x: -x[1]):
    print(f"  {r}: {c}")
