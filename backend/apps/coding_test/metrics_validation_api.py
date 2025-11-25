"""
관리자용 메트릭 검증 API
코드 입력 시 12가지 지표를 모두 계산하고, 지표를 반영한 힌트를 제공
"""
import json
import requests
import os
import time
import tracemalloc
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .code_analyzer import analyze_code, evaluate_code_with_llm
from .models import AIModelConfig
from .code_executor import CodeExecutor
from pathlib import Path


def load_problem_json():
    """문제 JSON 파일 로드"""
    json_path = Path(__file__).parent / 'data' / 'problems_final_cleaned.json'
    with open(json_path, 'r', encoding='utf-8-sig') as f:
        return json.load(f)


def format_code_indentation(code_text):
    """
    LLM 응답에서 코드 블록의 들여쓰기를 정리합니다.
    JSON 문자열로 전달되면서 들여쓰기가 사라지는 문제를 보정합니다.

    Args:
        code_text: LLM이 생성한 코드 문자열

    Returns:
        str: 적절한 들여쓰기가 적용된 코드
    """
    if not code_text:
        return code_text

    lines = code_text.strip().split('\n')
    formatted_lines = []
    indent_level = 0

    for line in lines:
        stripped = line.strip()
        if not stripped:
            formatted_lines.append('')
            continue

        # 들여쓰기 감소: elif, else, except, finally 등
        if stripped.startswith(('elif ', 'else:', 'except', 'except:', 'finally:')):
            indent_level = max(0, indent_level - 1)

        # 현재 줄 추가 (들여쓰기 적용)
        formatted_lines.append('    ' * indent_level + stripped)

        # 다음 줄 들여쓰기 증가: def, class, if, for, while, try 등으로 끝나는 경우
        if stripped.endswith(':'):
            indent_level += 1
        # 들여쓰기 감소: return, break, continue, pass, raise로 블록이 끝나는 경우도 고려
        # (단, 함수 내에서 return이 나와도 함수는 계속되므로 조심해야 함)

    return '\n'.join(formatted_lines)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def validate_metrics(request):
    """
    관리자용 메트릭 검증 API (문제 풀이 힌트와 동일한 메커니즘)

    ⚠️ 주의: DB 저장 및 배지 획득은 하지 않음 (관리자 테스트 전용)

    Request Body:
        - code: 검증할 코드
        - problem_id: 문제 ID (필수)
        - preset: 힌트 프리셋 ('초급', '중급', '고급', '커스텀')
        - hint_purpose: 힌트 목적 ('completion' or 'optimization')
        - custom_components: 커스텀 구성 요소 (preset이 '커스텀'일 때)
        - previous_hints: 이전 힌트 이력 (Chain of Hints)

    Response:
        - static_metrics: 정적 지표 6개
        - llm_metrics: LLM 지표 6개
        - hint: 지표를 반영한 힌트 (문제 풀이와 동일)
        - hint_purpose: 힌트 목적
        - weak_metrics: 약한 메트릭 (optimization인 경우만)
        - preset: 사용된 프리셋
        - hint_components: 힌트에 포함된 구성 요소
        - total_score: 종합 점수
    """
    user_code = request.data.get('code', '')
    problem_id = request.data.get('problem_id')
    preset = request.data.get('preset', '초급')
    hint_purpose = request.data.get('hint_purpose', 'completion')  # 수동 목적 설정
    custom_components = request.data.get('custom_components')
    previous_hints = request.data.get('previous_hints', [])

    if not user_code:
        return Response({
            'success': False,
            'error': '코드를 입력해주세요.'
        }, status=status.HTTP_400_BAD_REQUEST)

    if not problem_id:
        return Response({
            'success': False,
            'error': '문제 ID를 입력해주세요.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # 문제 정보 가져오기
    problems = load_problem_json()
    problem = next((p for p in problems if p['problem_id'] == str(problem_id)), None)

    if not problem:
        return Response({
            'success': False,
            'error': f'문제 ID {problem_id}를 찾을 수 없습니다.'
        }, status=status.HTTP_404_NOT_FOUND)

    problem_title = problem.get('title', '')
    problem_description = problem.get('description', '')
    test_cases = problem.get('examples', [])

    # 코드 실행하여 execution_results 생성
    execution_results = []
    if user_code.strip() and test_cases:
        executor = CodeExecutor(timeout=5)
        for test_case in test_cases:
            test_input = test_case.get('input', '')
            expected_output = test_case.get('output', '').strip()

            # 실행 시간 및 메모리 측정
            tracemalloc.start()
            start_time = time.time()

            try:
                result = executor.execute_python(user_code, test_input)
                execution_time = time.time() - start_time
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                actual_output = result.get('output', '').strip()
                is_correct = (actual_output == expected_output and result.get('success', False))

                execution_results.append({
                    'is_correct': is_correct,
                    'execution_time': execution_time,
                    'memory_usage': peak,
                    'input': test_input,
                    'expected_output': expected_output,
                    'actual_output': actual_output,
                    'error': result.get('error', '')
                })
            except Exception as e:
                tracemalloc.stop()
                execution_results.append({
                    'is_correct': False,
                    'execution_time': 0,
                    'memory_usage': 0,
                    'input': test_input,
                    'expected_output': expected_output,
                    'actual_output': '',
                    'error': str(e)
                })

    # 프리셋에 따른 힌트 구성 요소 결정
    # custom_components가 제공되면 우선 사용, 없으면 프리셋 기본값 사용
    if custom_components:
        hint_components = custom_components
        # summary는 항상 True로 강제
        hint_components['summary'] = True
    else:
        # 프리셋 기본 구성
        if preset == '초급':
            hint_components = {
                'summary': True, 'libraries': True, 'code_example': True,
                'step_by_step': False, 'complexity_hint': False,
                'edge_cases': False, 'improvements': False
            }
        elif preset == '중급':
            hint_components = {
                'summary': True, 'libraries': True, 'code_example': False,
                'step_by_step': False, 'complexity_hint': False,
                'edge_cases': False, 'improvements': False
            }
        elif preset == '고급':
            hint_components = {
                'summary': True, 'libraries': False, 'code_example': False,
                'step_by_step': False, 'complexity_hint': False,
                'edge_cases': False, 'improvements': False
            }
        else:
            # 기본값 (초급)
            hint_components = {
                'summary': True, 'libraries': True, 'code_example': True,
                'step_by_step': False, 'complexity_hint': False,
                'edge_cases': False, 'improvements': False
            }

    # 1단계: 정적 지표 계산 (6개) - execution_results 전달하여 실행 시간/메모리 계산
    try:
        static_metrics = analyze_code(user_code, problem_id, execution_results=execution_results if execution_results else None)
    except Exception as e:
        print(f'Static analysis error: {str(e)}')
        static_metrics = {
            'syntax_errors': 0,
            'test_pass_rate': 0.0,
            'execution_time': 0.0,
            'memory_usage': 0.0,
            'code_quality_score': 0.0,
            'pep8_violations': 0
        }

    # 2단계: LLM 지표 계산 (6개)
    try:
        llm_metrics = evaluate_code_with_llm(user_code, problem_description, static_metrics)
    except Exception as e:
        print(f'LLM evaluation error: {str(e)}')
        llm_metrics = {
            'algorithm_efficiency': 3,
            'code_readability': 3,
            'design_pattern_fit': 3,
            'edge_case_handling': 3,
            'code_conciseness': 3,
            'function_separation': 3
        }

    # 3단계: 지표를 반영한 힌트 생성 (문제 풀이와 동일한 로직)
    hint_text = generate_hint_like_user_facing(
        user_code,
        problem_description,
        static_metrics,
        llm_metrics,
        hint_components,
        previous_hints,
        preset
    )

    response_data = {
        'static_metrics': static_metrics,
        'llm_metrics': llm_metrics,
        'hint': hint_text,
        'hint_purpose': hint_purpose,  # 'completion' or 'optimization'
        'preset': preset,
        'hint_components': hint_components,
        'total_score': calculate_total_score(static_metrics, llm_metrics)
    }

    # Note: weak_metrics는 hint_api.py의 로직을 사용할 때만 계산됨
    # 관리자 검증 API는 단순화된 버전이므로 hint_purpose만 전달

    return Response({
        'success': True,
        'data': response_data
    })


def calculate_total_score(static_metrics, llm_metrics):
    """
    전체 점수 계산 (0-100점)

    정적 지표 50% + LLM 지표 50%
    """
    # 정적 지표 점수화 (0-100)
    static_score = 0

    # 1. 문법 오류 (0개 = 20점, 1개 이상 = 0점)
    static_score += 20 if static_metrics['syntax_errors'] == 0 else 0

    # 2. 테스트 통과율 (0-25점)
    static_score += (static_metrics['test_pass_rate'] / 100) * 25

    # 3. 실행 시간 (100ms 이하 = 15점, 선형 감소)
    execution_time = static_metrics.get('execution_time', 0)
    if execution_time <= 100:
        static_score += 15
    elif execution_time <= 1000:
        static_score += 15 - ((execution_time - 100) / 900) * 15

    # 4. 메모리 사용량 (1000KB 이하 = 10점, 선형 감소)
    memory_usage = static_metrics.get('memory_usage', 0)
    if memory_usage <= 1000:
        static_score += 10
    elif memory_usage <= 10000:
        static_score += 10 - ((memory_usage - 1000) / 9000) * 10

    # 5. 코드 품질 (0-20점)
    static_score += (static_metrics['code_quality_score'] / 100) * 20

    # 6. PEP8 위반 (0개 = 10점, 선형 감소)
    pep8_violations = static_metrics['pep8_violations']
    if pep8_violations == 0:
        static_score += 10
    elif pep8_violations <= 10:
        static_score += 10 - pep8_violations

    # LLM 지표 점수화 (각 1-5점을 0-100점으로 변환)
    llm_score = sum(llm_metrics.values()) / 6  # 평균 (1-5)
    llm_score = ((llm_score - 1) / 4) * 100  # 0-100 변환

    # 최종 점수 (정적 50% + LLM 50%)
    total_score = (static_score * 0.5) + (llm_score * 0.5)

    return round(total_score, 2)


def generate_hint_like_user_facing(user_code, problem_description, static_metrics, llm_metrics, hint_components, previous_hints, preset='초급'):
    """
    문제 풀이 화면과 동일한 힌트 생성 로직

    hint_api.py의 request_hint()와 완전히 동일한 메커니즘 사용
    """
    try:
        ai_config = AIModelConfig.objects.first()
        if not ai_config or ai_config.mode != 'api':
            return generate_fallback_hint_with_emoji(hint_components, user_code, preset)

        api_key = ai_config.api_key if ai_config.api_key else os.environ.get('HUGGINGFACE_API_KEY', '')
        if not api_key:
            return generate_fallback_hint_with_emoji(hint_components, user_code, preset)

        # 레벨별 요약 스타일 정의 (hint_api.py와 동일)
        summary_style = ""
        if preset == '초급':
            summary_style = """
💡 요약 (summary): 1-2줄로 핵심 개념을 초보자 친화적으로 설명
  ⚠️ 반드시 지켜야 할 규칙:
  - 필요한 함수명이나 라이브러리명을 직접적으로 언급하세요 (예: "collections.Counter를 사용하여 각 문자의 빈도를 세고...")
  - 구체적인 작업이 무엇인지 단계별로 명확히 설명하세요
  - "어떻게"를 중심으로 구체적인 방법을 제시하세요
  - 추상적인 개념이나 질문은 절대 사용하지 마세요"""
        elif preset == '중급':
            summary_style = """
💡 요약 (summary): 1-2줄로 핵심 개념을 중급자에게 설명
  ⚠️ 반드시 지켜야 할 규칙:
  - 함수명이나 라이브러리명을 직접 언급하지 말고, 자료구조나 알고리즘 개념으로만 설명하세요 (예: "해시 테이블을 활용하여 빈도를 추적하고...")
  - "무엇을" 사용해야 하는지에 집중하세요
  - 구체적인 함수명 대신 개념적 접근법을 제시하세요
  - 질문 형식은 사용하지 마세요"""
        elif preset == '고급':
            summary_style = """
💡 요약 (summary): 소크라테스식 질문으로 사고를 유도
  ⚠️ 반드시 지켜야 할 규칙:
  - 반드시 질문 형식으로만 작성하세요 (반드시 '?'로 끝나야 합니다)
  - 직접적인 답이나 해결책을 절대 제시하지 마세요
  - 구체적인 함수명이나 라이브러리명을 절대 언급하지 마세요
  - 학습자가 스스로 사고하도록 핵심 질문으로만 유도하세요 (예: "이 문제에서 중복 계산을 피하려면 어떤 자료구조가 필요할까요?")
  - 2개 이상의 연계된 질문을 사용하여 사고의 흐름을 유도하세요"""
        else:
            summary_style = "💡 요약 (summary): 1-2줄로 핵심 개념 설명"

        # 커스텀 구성 기반 프롬프트 생성 (hint_api.py와 동일)
        prompt_components = [summary_style]  # 요약은 항상 포함

        if hint_components.get('libraries'):
            prompt_components.append("""📚 사용 라이브러리 (libraries): 필요한 Python 라이브러리/함수 목록
  ⚠️ 중요: 코드 예시(code_example)에서 실제로 사용하는 라이브러리만 추천하세요
  - 코드 예시가 없거나 표준 내장 함수만 사용한다면, 이 항목은 null로 반환하세요""")
        if hint_components.get('code_example'):
            if preset == '고급':
                prompt_components.append("""📝 코드 예시 (code_example): 학생이 작성한 코드에 이어서 사용할 수 있는 핵심 로직
  ⚠️ 중요:
  - "..."이나 생략 기호를 절대 사용하지 마세요
  - 완전하고 실행 가능한 코드를 작성하세요
  - 학생의 기존 코드(입력 처리 등)를 활용할 수 있는 방식으로 제시하세요
  - 함수 분리와 알고리즘적 사고를 유도하는 구조로 작성하세요
  - 코드 블록은 반드시 올바른 Python 들여쓰기(4칸 스페이스)를 포함해야 합니다""")
            else:
                prompt_components.append("""📝 코드 예시 (code_example): 간단한 코드 예제 (5-10줄, 핵심 로직 포함)
  ⚠️ 중요: 코드 블록은 반드시 올바른 Python 들여쓰기(4칸 스페이스)를 포함해야 합니다""")
        if hint_components.get('step_by_step'):
            prompt_components.append("📋 단계별 해결 방법 (step_by_step): 문제 해결 단계를 순서대로 나열")
        if hint_components.get('complexity_hint'):
            prompt_components.append("⏱️ 시간/공간 복잡도 힌트 (complexity_hint): 목표 복잡도와 최적화 방법")
        if hint_components.get('edge_cases'):
            prompt_components.append("⚠️ 엣지 케이스 (edge_cases): 고려해야 할 특수 케이스 목록")
        if hint_components.get('improvements'):
            prompt_components.append("✨ 개선 사항 (improvements): 현재 코드의 개선점 제안")

        components_str = "\n".join(prompt_components)

        # 이전 힌트 컨텍스트 생성 (Chain of Hints)
        previous_hints_str = ""
        if previous_hints:
            hints_list = []
            for i, prev_hint in enumerate(previous_hints, 1):
                hint_text = prev_hint.get('hint_text', '')
                level = prev_hint.get('level', '커스텀')
                timestamp = prev_hint.get('timestamp', '')
                hints_list.append(f"{i}. [{level}] {hint_text[:100]}...")
            previous_hints_str = f"""
# 이전 힌트 이력 (참고용)
학생이 이미 받은 힌트들입니다. 이를 바탕으로 더 발전된 힌트를 제공하세요:
{chr(10).join(hints_list)}

⚠️ 중요: 위 힌트들에서 언급한 내용은 반복하지 말고, 다음 단계나 새로운 관점의 힌트를 제공하세요.
"""

        # 통합 프롬프트 생성 (hint_api.py와 동일)
        prompt = f"""당신은 Python 코딩 교육 전문가입니다.

# 문제 정보
{problem_description}

# 학생 코드
{user_code if user_code else '(아직 작성하지 않음)'}

# 현재 코드 분석 결과 (12개 지표)

## 정적 지표 (6개)
- 문법 오류: {static_metrics['syntax_errors']}개
- 테스트 통과율: {static_metrics['test_pass_rate']}%
- 실행 시간: {static_metrics.get('execution_time', 0)}ms
- 메모리 사용량: {static_metrics.get('memory_usage', 0)}KB
- 코드 품질 점수: {static_metrics['code_quality_score']}/100
- PEP8 위반: {static_metrics['pep8_violations']}개

## LLM 평가 지표 (6개, 각 1-5점)
- 알고리즘 효율성: {llm_metrics['algorithm_efficiency']}/5
- 코드 가독성: {llm_metrics['code_readability']}/5
- 엣지 케이스 처리: {llm_metrics['edge_case_handling']}/5
- 코드 간결성: {llm_metrics['code_conciseness']}/5
- 테스트 커버리지 추정: {llm_metrics.get('test_coverage_estimate', 3)}/5
- 보안 인식: {llm_metrics.get('security_awareness', 3)}/5
{previous_hints_str}
# 요청 사항
위 12개 지표를 모두 반영하여 다음 항목만 포함한 힌트를 제공하세요:
{components_str}

⚠️ 중요:
- 12개 지표를 모두 고려하여 종합적인 피드백을 제공하세요
- 가장 시급한 개선 사항을 우선적으로 다루세요

# 응답 형식 (JSON)
{{
  "hint_content": {{
    "summary": "..." or null,
    "libraries": [...] or null,
    "code_example": "..." or null,
    "step_by_step": [...] or null,
    "complexity_hint": "..." or null,
    "edge_cases": [...] or null,
    "improvements": [...] or null
  }}
}}

위 구성만 포함하여 응답하세요. 선택되지 않은 항목은 null로 반환하세요.
"""

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': ai_config.model_name,
            'messages': [
                {'role': 'system', 'content': '당신은 코딩 교육 전문가입니다. 12개 지표를 모두 반영하여 JSON 형식으로 힌트를 반환해야 합니다.'},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 1000,
            'temperature': 0.7,
            'top_p': 0.9
        }

        response = requests.post(
            'https://router.huggingface.co/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                llm_response_text = result['choices'][0]['message']['content'].strip()

                # JSON 파싱 시도 (hint_api.py와 동일)
                try:
                    llm_data = json.loads(llm_response_text)
                    hint_content = llm_data.get('hint_content', {})

                    # 코드 예시 들여쓰기 보정
                    if hint_content.get('code_example'):
                        hint_content['code_example'] = format_code_indentation(hint_content['code_example'])

                    # 힌트 내용 구성 (이모지 포함)
                    hint_parts = []
                    if hint_content.get('summary'):
                        hint_parts.append(f"💡 {hint_content['summary']}")
                    if hint_content.get('libraries'):
                        hint_parts.append(f"📚 사용 라이브러리: {', '.join(hint_content['libraries'])}")
                    if hint_content.get('code_example'):
                        hint_parts.append(f"📝 코드 예시:\n{hint_content['code_example']}")
                    if hint_content.get('step_by_step'):
                        steps = '\n'.join(f"{i+1}. {step}" for i, step in enumerate(hint_content['step_by_step']))
                        hint_parts.append(f"📋 단계별 방법:\n{steps}")
                    if hint_content.get('complexity_hint'):
                        hint_parts.append(f"⏱️ 복잡도: {hint_content['complexity_hint']}")
                    if hint_content.get('edge_cases'):
                        cases = '\n'.join(f"- {case}" for case in hint_content['edge_cases'])
                        hint_parts.append(f"⚠️ 엣지 케이스:\n{cases}")
                    if hint_content.get('improvements'):
                        improvements = '\n'.join(f"- {imp}" for imp in hint_content['improvements'])
                        hint_parts.append(f"✨ 개선 사항:\n{improvements}")

                    return '\n\n'.join(hint_parts) if hint_parts else "힌트를 생성하는 중 오류가 발생했습니다."

                except json.JSONDecodeError:
                    # JSON 파싱 실패 시 원문 반환
                    return llm_response_text

        return generate_fallback_hint_with_emoji(hint_components, user_code, preset)

    except Exception as e:
        print(f'Hint generation error: {str(e)}')
        return generate_fallback_hint_with_emoji(hint_components, user_code, preset)


def generate_fallback_hint_with_emoji(hint_components, user_code, preset='초급'):
    """
    API 실패 시 기본 힌트 생성 - 레벨별로 차별화된 힌트 제공
    """
    # 코드가 없거나 매우 짧을 때
    if not user_code or len(user_code.strip()) < 10:
        if preset == '초급':
            return "먼저 문제를 단계별로 나누어 생각해보세요. input() 함수로 입력을 받고, split() 메서드로 데이터를 분리한 후, 필요한 연산을 수행하세요."
        elif preset == '중급':
            return "문제를 분석하여 입력 처리, 핵심 로직, 출력 형식을 파악하세요. 어떤 자료구조가 적합할지 고민해보세요."
        else:  # 고급
            return "이 문제의 본질은 무엇일까요? 입력과 출력의 관계를 분석하고, 최적의 알고리즘 접근 방식을 스스로 찾아보세요."

    # 레벨별 힌트 생성
    hint_parts = []

    # 💡 요약 (레벨별로 다르게)
    if hint_components.get('summary'):
        if preset == '초급':
            hint_parts.append("💡 이 문제는 입력을 받아 처리한 후 결과를 출력하는 구조입니다. input()과 split()을 사용하여 데이터를 받고, 반복문이나 조건문으로 처리한 뒤 print()로 출력하세요.")
        elif preset == '중급':
            hint_parts.append("💡 입력 데이터의 패턴을 분석하고, 적절한 자료구조(리스트, 딕셔너리, 집합 등)를 활용하여 효율적으로 처리하는 방법을 고민해보세요.")
        else:  # 고급
            hint_parts.append("💡 이 문제의 핵심은 무엇일까요? 시간 복잡도를 최적화하려면 어떤 알고리즘적 접근이 필요할까요? 중복 연산을 제거할 방법은 없을까요?")

    # 📚 사용 라이브러리 (레벨별로 다르게)
    if hint_components.get('libraries'):
        if preset == '초급':
            hint_parts.append("📚 사용 라이브러리: 이 문제는 Python 표준 내장 함수(input, print, split, int, str, len 등)만으로 해결할 수 있습니다. 특별한 라이브러리는 필요하지 않습니다.")
        elif preset == '중급':
            hint_parts.append("📚 사용 라이브러리: 표준 라이브러리의 collections(Counter, defaultdict, deque), itertools(combinations, permutations) 등을 고려해볼 수 있습니다. 하지만 기본 자료구조만으로도 충분할 수 있습니다.")
        else:  # 고급
            hint_parts.append("📚 사용 라이브러리: 문제의 특성에 따라 적절한 라이브러리를 선택하세요. 시간 복잡도 개선이 필요하다면 bisect(이진 탐색), heapq(우선순위 큐) 등을 고려해보세요.")

    # 📝 코드 예시 (레벨별로 다르게)
    if hint_components.get('code_example'):
        if preset == '초급':
            hint_parts.append("""📝 코드 예시:
```python
# 입력 받기
data = input().split()
a, b = int(data[0]), int(data[1])

# 연산 수행
result = a + b

# 결과 출력
print(result)
```
위 코드는 두 수를 입력받아 더하는 기본 예시입니다. 문제에 맞게 로직을 수정하세요.""")
        elif preset == '중급':
            hint_parts.append("""📝 코드 예시:
```python
# 입력 처리
n = int(input())
numbers = list(map(int, input().split()))

# 자료구조 활용
result = []
for num in numbers:
    # 조건에 따라 처리
    if num > 0:
        result.append(num * 2)

# 출력
print(' '.join(map(str, result)))
```
리스트와 반복문을 활용한 데이터 처리 패턴입니다.""")
        else:  # 고급
            hint_parts.append("""📝 코드 예시:
현재 코드를 기반으로 핵심 로직을 추가하는 방법을 생각해보세요:
```python
# 기존 입력 처리 후...
# (여러분의 a, b = input().split() 코드 다음에)

# 핵심 로직 추가 예시
def calculate_result(a, b):
    # 알고리즘 적용
    result = 0
    for i in range(a, b + 1):
        if is_valid(i):  # 조건 검사
            result += process(i)  # 처리
    return result

# 실행
answer = calculate_result(int(a), int(b))
print(answer)
```
함수로 분리하여 로직을 명확히 하고, 필요한 알고리즘을 적용하세요.""")

    # 📋 단계별 방법 (레벨별로 다르게)
    if hint_components.get('step_by_step'):
        if preset == '초급':
            hint_parts.append("""📋 단계별 방법:
1. **입력 받기**: input()으로 데이터를 읽고, 필요하면 split()으로 분리하세요
2. **형변환**: 숫자가 필요하면 int() 또는 float()로 변환하세요
3. **연산 수행**: 조건문(if), 반복문(for/while)을 사용해 문제 요구사항을 처리하세요
4. **결과 저장**: 계산 결과를 변수나 리스트에 저장하세요
5. **출력**: print()로 결과를 출력하세요. 여러 값은 공백이나 줄바꿈으로 구분하세요""")
        elif preset == '중급':
            hint_parts.append("""📋 단계별 방법:
1. **문제 분석**: 입력/출력 형식을 정확히 파악하고, 필요한 자료구조를 결정하세요
2. **데이터 구조화**: 리스트, 딕셔너리, 집합 등 적절한 자료구조에 데이터를 저장하세요
3. **알고리즘 설계**: 정렬, 탐색, 필터링 등 필요한 알고리즘을 적용하세요
4. **최적화 검토**: 불필요한 반복이나 중복 연산이 있는지 확인하세요
5. **검증**: 예제 입력으로 테스트하고, 엣지 케이스를 점검하세요""")
        else:  # 고급
            hint_parts.append("""📋 단계별 방법:
1. **문제 본질 파악**: 이 문제가 어떤 유형(그리디, DP, 그래프, 이진탐색 등)인지 분석하세요
2. **시간복잡도 설계**: 입력 크기를 고려해 목표 시간복잡도를 설정하세요 (예: O(n log n))
3. **알고리즘 선택**: 최적의 알고리즘을 선택하고, 필요한 자료구조를 결정하세요
4. **구현 및 최적화**: 코드를 작성하되, 상수 최적화와 메모리 효율도 고려하세요
5. **검증 및 개선**: 시간/공간 복잡도를 재확인하고, 더 나은 방법이 있는지 탐색하세요""")

    # ⏱️ 복잡도 힌트 (레벨별로 다르게)
    if hint_components.get('complexity_hint'):
        if preset == '초급':
            hint_parts.append("⏱️ 복잡도: 입력 크기가 작다면 단순한 반복문(O(n))이나 이중 반복문(O(n²))으로도 충분합니다. 코드가 제한 시간 내에 실행되는지 확인하세요.")
        elif preset == '중급':
            hint_parts.append("⏱️ 복잡도: 입력 크기가 크다면 O(n²) 알고리즘은 느릴 수 있습니다. 정렬(O(n log n))이나 해시 테이블(O(n))을 활용해 최적화를 고려하세요.")
        else:  # 고급
            hint_parts.append("⏱️ 복잡도: 입력 크기와 제한 시간을 분석하여 목표 시간복잡도를 도출하세요. 100만 이상이라면 O(n) 또는 O(n log n)이 필요할 수 있습니다. 공간복잡도도 함께 고려하세요.")

    # ⚠️ 엣지 케이스 (레벨별로 다르게)
    if hint_components.get('edge_cases'):
        if preset == '초급':
            hint_parts.append("""⚠️ 엣지 케이스:
- **빈 입력**: 입력이 없거나 빈 문자열일 때 에러가 나지 않는지 확인하세요
- **최소/최대 값**: 입력이 0, 1, 또는 매우 큰 수일 때도 정상 작동하는지 테스트하세요
- **특수 문자**: 공백, 줄바꿈 등이 예상대로 처리되는지 확인하세요
- **자료형**: 정수와 문자열을 혼동하지 않도록 주의하세요""")
        elif preset == '중급':
            hint_parts.append("""⚠️ 엣지 케이스:
- **중복 데이터**: 같은 값이 여러 번 나타날 때 올바르게 처리되는지 확인하세요
- **경계값**: 입력의 최소/최대 범위에서 오버플로우나 언더플로우가 발생하지 않는지 점검하세요
- **정렬 상태**: 입력이 정렬되어 있거나, 역순일 때도 동작하는지 확인하세요
- **빈 컬렉션**: 리스트나 딕셔너리가 비어있을 때의 동작을 검증하세요""")
        else:  # 고급
            hint_parts.append("""⚠️ 엣지 케이스:
- **시간 제한**: 최악의 입력(예: 모두 같은 값, 역순 정렬)에서도 제한 시간 내에 실행되는지 확인하세요
- **메모리 제한**: 대량의 데이터를 처리할 때 메모리 초과가 발생하지 않는지 점검하세요
- **수치 범위**: 정수 오버플로우, 부동소수점 오차 등을 고려하세요
- **알고리즘 특성**: 선택한 알고리즘이 모든 입력 케이스에 대해 올바른 결과를 보장하는지 증명하세요""")

    # ✨ 개선 사항 (레벨별로 다르게)
    if hint_components.get('improvements'):
        if preset == '초급':
            hint_parts.append("""✨ 개선 사항:
- **변수명 개선**: a, b 대신 first_number, second_number처럼 의미 있는 이름을 사용하세요
- **주석 추가**: 각 코드 블록이 무엇을 하는지 간단히 주석으로 설명하세요
- **들여쓰기**: Python은 들여쓰기가 중요합니다. 일관된 들여쓰기(보통 스페이스 4칸)를 유지하세요
- **공백 활용**: 연산자 주변에 공백을 추가하면 가독성이 좋아집니다 (예: a+b → a + b)""")
        elif preset == '중급':
            hint_parts.append("""✨ 개선 사항:
- **함수 분리**: 긴 코드는 기능별로 함수로 분리하면 재사용성과 가독성이 향상됩니다
- **리스트 컴프리헨션**: 간단한 반복문은 리스트 컴프리헨션으로 간결하게 표현할 수 있습니다
- **내장 함수 활용**: sum(), max(), min(), sorted() 등 내장 함수를 적극 활용하세요
- **불필요한 변수 제거**: 한 번만 사용되는 임시 변수는 제거해 코드를 간결하게 만드세요
- **PEP 8 준수**: Python 코딩 컨벤션을 따르면 다른 개발자가 읽기 쉬운 코드가 됩니다""")
        else:  # 고급
            hint_parts.append("""✨ 개선 사항:
- **알고리즘 최적화**: 더 효율적인 알고리즘이나 자료구조는 없는지 재검토하세요
- **메모이제이션**: 중복 계산이 있다면 캐싱이나 DP를 활용해 최적화하세요
- **조기 종료**: 조건을 만족하는 순간 바로 반환하여 불필요한 연산을 줄이세요
- **공간-시간 트레이드오프**: 메모리를 더 사용해 시간을 줄이거나, 그 반대의 방법을 고려하세요
- **프로파일링**: 실제 병목 지점을 파악하여 최적화 우선순위를 정하세요
- **수학적 최적화**: 문제를 수학적으로 재정의하면 더 간단한 해법이 나올 수 있습니다""")

    if hint_parts:
        return '\n\n'.join(hint_parts)
    else:
        if preset == '초급':
            return "작성하신 코드를 보니 좋은 시작입니다! input()으로 입력을 받고, 조건문과 반복문으로 처리한 후, print()로 출력하는 구조를 기억하세요."
        elif preset == '중급':
            return "코드의 기본 구조는 잘 잡혀있습니다. 이제 자료구조 선택과 알고리즘 효율성을 고민해보세요. 엣지 케이스 처리도 잊지 마세요."
        else:  # 고급
            return "구현은 완료된 것 같습니다. 이제 시간/공간 복잡도를 분석하고, 더 최적화된 접근 방법이 있는지 탐구해보세요. 수학적 증명도 고려해보세요."
