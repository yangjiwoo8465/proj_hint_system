#!/usr/bin/env python
"""LangGraph 테스트 스크립트"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.coding_test.langgraph_hint import run_langgraph_hint

User = get_user_model()
user = User.objects.first()

print("=" * 50)
print("테스트 1: 빈 코드 (분기 A) - LLM 스킵 예상")
print("=" * 50)
success, data, error, status_code = run_langgraph_hint(
    user=user,
    problem_id='1000',  # A+B 문제
    user_code='',
    preset='중급'
)
if success:
    print(f"분기: {data.get('hint_branch')}")
    print(f"힌트 타입: {data.get('hint_type')}")
    print(f"LLM 스킵됨: {data.get('hint_type') == 'syntax_fix'}")
    hint_preview = data.get('hint', '')[:150] if data.get('hint') else 'N/A'
    print(f"힌트 미리보기: {hint_preview}...")
else:
    print(f"오류: {error}")

print()
print("=" * 50)
print("테스트 2: 정상 코드 (분기 B) - LLM 호출 예상")
print("=" * 50)
success2, data2, error2, status_code2 = run_langgraph_hint(
    user=user,
    problem_id='1000',  # A+B 문제
    user_code='print("hello")',
    preset='중급'
)
if success2:
    print(f"분기: {data2.get('hint_branch')}")
    print(f"힌트 타입: {data2.get('hint_type')}")
    skip_types = ['syntax_fix', 'first_complete', 'star_achieved']
    print(f"LLM 호출됨: {data2.get('hint_type') not in skip_types}")
else:
    print(f"오류: {error2}")
