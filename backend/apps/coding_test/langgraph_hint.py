"""
LangGraph 기반 힌트 시스템

기존 API 방식(hint_api.py)과 병행하여 사용 가능한 LangGraph 기반 힌트 제공 시스템.
그래프 기반으로 힌트 생성 워크플로우를 정의하고 실행합니다.

사용법:
- 기존 방식: POST /coding-test/hints/ (hint_api.request_hint)
- LangGraph 방식: POST /coding-test/hints/langgraph/ (langgraph_hint.request_hint_langgraph)

분기 로직 (A~F):
- A: 문법 오류 있음 → 문법 수정 힌트
- B: completion + 테스트 미통과 → 완성 힌트
- C: completion + 테스트 통과 → 축하 + 다음 별 안내
- D: optimization + 테스트 미통과 → 효율적 완성 힌트
- E1: optimization + 다음 별 달성 → 축하 메시지
- E2: optimization + 다음 별 미달성 → 칭찬 + 개선 위치 명시
- F: optimal (별 3개) → 다른 풀이 제안
"""

from typing import TypedDict, List, Dict, Any, Optional
import json
import requests
import os
from pathlib import Path

# LangGraph imports
try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False
    StateGraph = None
    END = None

# OpenAI 신버전 API
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings

from .models import HintRequest, Problem, AIModelConfig, HintMetrics, ProblemStatus
from .code_analyzer import analyze_code


# ==================== State 정의 ====================

class HintState(TypedDict):
    """LangGraph 힌트 시스템의 상태"""
    # 입력
    problem_id: str
    problem_title: str
    problem_description: str
    user_code: str
    previous_hints: List[str]
    preset: str  # '초급', '중급', '고급', None
    custom_components: Dict[str, bool]  # 6개 구성요소 선택
    user_id: int

    # 분석 결과 - 정적 메트릭 (6개)
    static_metrics: Dict[str, Any]
    # - syntax_errors: 문법 오류 수
    # - test_pass_rate: 테스트 통과율 (%)
    # - execution_time: 실행 시간 (ms)
    # - memory_usage: 메모리 사용량 (KB)
    # - code_quality_score: 품질 점수 (0-100)
    # - pep8_violations: PEP8 위반 수

    # 분석 결과 - LLM 메트릭 (6개, 각 1-5점)
    llm_metrics: Dict[str, int]
    # - algorithm_efficiency: 알고리즘 효율성
    # - code_readability: 코드 가독성
    # - edge_case_handling: 엣지 케이스 처리
    # - code_conciseness: 코드 간결성
    # - test_coverage_estimate: 테스트 커버리지 추정
    # - security_awareness: 보안 인식

    # 별점 관련
    current_star_count: int  # 현재 별점 (0-3)
    hint_purpose: str  # 'completion', 'optimization', 'optimal'

    # 분기 결정
    hint_branch: str  # 'A', 'B', 'C', 'D', 'E1', 'E2', 'F'
    purpose_context: str  # LLM에게 전달할 컨텍스트
    weak_metrics: List[Dict[str, Any]]  # 약점 지표

    # COH (Chain of Hint) 관련
    coh_depth: int  # 현재 COH 깊이 (0 = 기본, 1+ = COH 적용)
    coh_max_depth: int  # 프리셋별 최대 COH 깊이
    hint_level: int  # 최종 힌트 레벨 (1-9, 1=가장 상세)
    filtered_components: Dict[str, bool]  # COH 레벨로 필터링된 구성요소
    blocked_components: List[str]  # 차단된 구성요소 목록
    coh_status: Dict[str, Any]  # COH 상태 정보 (프론트엔드 전달용)

    # 힌트 생성
    llm_prompt: str
    hint_content: Dict[str, Any]  # JSON 형태 힌트 응답
    final_hint: str
    hint_type: str

    # 에러
    error: Optional[str]


# ==================== 노드 함수들 ====================

def input_node(state: HintState) -> HintState:
    """입력 검증 및 문제 정보 로드 노드"""
    json_path = Path(__file__).parent / 'data' / 'problems_final_cleaned.json'

    try:
        with open(json_path, 'r', encoding='utf-8-sig') as f:
            problems = json.load(f)

        problem = next((p for p in problems if p['problem_id'] == str(state['problem_id'])), None)

        if problem:
            state['problem_title'] = problem.get('title', '')
            state['problem_description'] = problem.get('description', '')
        else:
            state['error'] = f"문제 ID {state['problem_id']}를 찾을 수 없습니다."
    except Exception as e:
        state['error'] = f"문제 로드 실패: {str(e)}"

    return state


def purpose_node(state: HintState) -> HintState:
    """별점 조회 및 힌트 목적 결정 노드"""
    if state.get('error'):
        return state

    # DB에서 현재 별점 조회
    try:
        problem_status = ProblemStatus.objects.filter(
            problem__problem_id=state['problem_id'],
            user_id=state.get('user_id')
        ).first()

        if problem_status:
            state['current_star_count'] = problem_status.star_count or 0
        else:
            state['current_star_count'] = 0
    except:
        state['current_star_count'] = 0

    # 힌트 목적 결정
    current_star = state['current_star_count']
    if current_star == 0:
        state['hint_purpose'] = 'completion'
    elif current_star < 3:
        state['hint_purpose'] = 'optimization'
    else:
        state['hint_purpose'] = 'optimal'

    return state


def static_analysis_node(state: HintState) -> HintState:
    """정적 분석 노드 (6개 메트릭)"""
    if state.get('error'):
        return state

    try:
        analysis_result = analyze_code(
            state['user_code'],
            state['problem_id'],
            state.get('previous_hints', [])
        )

        static_metrics = analysis_result.get('static_metrics', {})
        state['static_metrics'] = {
            'syntax_errors': static_metrics.get('syntax_errors', 0),
            'test_pass_rate': static_metrics.get('test_pass_rate', 0),
            'execution_time': static_metrics.get('execution_time', 0),
            'memory_usage': static_metrics.get('memory_usage', 0),
            'code_quality_score': static_metrics.get('code_quality_score', 0),
            'pep8_violations': static_metrics.get('pep8_violations', 0),
            'cyclomatic_complexity': static_metrics.get('cyclomatic_complexity', 0),
        }

    except Exception as e:
        state['error'] = f"정적 분석 실패: {str(e)}"
        state['static_metrics'] = {}

    return state


def llm_eval_node(state: HintState) -> HintState:
    """LLM 메트릭 평가 노드 (6개 메트릭, GPT-4.1 호출)"""
    if state.get('error'):
        return state

    try:
        ai_config = AIModelConfig.get_config()

        # OpenAI API만 지원
        if ai_config.mode != 'openai' or not ai_config.openai_api_key:
            # LLM 평가 생략, 기본값 사용
            state['llm_metrics'] = {
                'algorithm_efficiency': 3,
                'code_readability': 3,
                'edge_case_handling': 3,
                'code_conciseness': 3,
                'test_coverage_estimate': 3,
                'security_awareness': 3,
            }
            return state

        client = OpenAI(api_key=ai_config.openai_api_key)
        model_name = ai_config.model_name or 'gpt-4.1'

        eval_prompt = f"""당신은 코드 평가 전문가입니다. 아래 코드를 평가하고 JSON으로 응답하세요.

[문제]
{state['problem_title']}
{state['problem_description'][:300]}...

[학생 코드]
```python
{state['user_code'][:1000]}
```

각 항목을 1-5점으로 평가하세요 (1=매우 나쁨, 5=매우 좋음):
1. algorithm_efficiency: 알고리즘 효율성 (시간/공간 복잡도)
2. code_readability: 코드 가독성 (변수명, 구조)
3. edge_case_handling: 엣지 케이스 처리
4. code_conciseness: 코드 간결성
5. test_coverage_estimate: 테스트 커버리지 추정
6. security_awareness: 보안 인식 (입력 검증 등)

JSON 형식으로만 응답:
{{"algorithm_efficiency": N, "code_readability": N, "edge_case_handling": N, "code_conciseness": N, "test_coverage_estimate": N, "security_awareness": N}}"""

        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": eval_prompt}],
            temperature=0.3,
            max_tokens=200
        )

        response_text = response.choices[0].message.content.strip()

        # JSON 파싱
        try:
            # JSON 블록 추출
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0]

            llm_metrics = json.loads(response_text)
            state['llm_metrics'] = llm_metrics
        except:
            # 파싱 실패 시 기본값
            state['llm_metrics'] = {
                'algorithm_efficiency': 3,
                'code_readability': 3,
                'edge_case_handling': 3,
                'code_conciseness': 3,
                'test_coverage_estimate': 3,
                'security_awareness': 3,
            }

    except Exception as e:
        # LLM 호출 실패 시 기본값
        state['llm_metrics'] = {
            'algorithm_efficiency': 3,
            'code_readability': 3,
            'edge_case_handling': 3,
            'code_conciseness': 3,
            'test_coverage_estimate': 3,
            'security_awareness': 3,
        }

    return state


def branch_decision_node(state: HintState) -> HintState:
    """분기 결정 노드 (A~F)"""
    if state.get('error'):
        return state

    static_metrics = state.get('static_metrics', {})
    hint_purpose = state.get('hint_purpose', 'completion')
    current_star = state.get('current_star_count', 0)
    user_code = state.get('user_code', '').strip()

    syntax_errors = static_metrics.get('syntax_errors', 0)
    test_pass_rate = static_metrics.get('test_pass_rate', 0)
    code_quality = static_metrics.get('code_quality_score', 0)

    # 분기 결정 로직
    # 분기 A: 코드 없음 또는 문법 오류
    if not user_code or syntax_errors > 0:
        state['hint_branch'] = 'A'
        if not user_code:
            state['purpose_context'] = """
[힌트 목적: 코드 작성 시작] (분기 A)

⚠️ 아직 코드가 작성되지 않았습니다.
먼저 코드를 작성해주세요.

힌트 제공 시:
1. 문제의 입력/출력 형식을 설명하세요
2. 기본적인 코드 구조를 안내하세요
3. 시작점을 제시하세요
"""
        else:
            state['purpose_context'] = f"""
[힌트 목적: 문법 오류 수정] (분기 A)

⚠️ 코드에 문법 오류가 {syntax_errors}개 있습니다.
문법 오류를 먼저 수정해야 합니다.

힌트 제공 시:
1. 오류가 있는 줄 번호를 명시하세요
2. 오류 원인을 설명하세요
3. 수정 방법을 제시하세요
"""
    elif hint_purpose == 'completion':
        if test_pass_rate >= 100:
            # 분기 C: completion + 테스트 통과
            state['hint_branch'] = 'C'
            state['purpose_context'] = f"""
[축하! 테스트 통과!] (분기 C)

🌟 테스트를 처음 통과했습니다!
현재 코드 품질: {code_quality}/100점

다음 목표: 별 2개 (품질 70점 이상)
더 나은 코드를 위한 개선점을 제안해주세요.
"""
        else:
            # 분기 B: completion + 테스트 미통과
            state['hint_branch'] = 'B'
            state['purpose_context'] = f"""
[힌트 목적: 코드 완성] (분기 B)

테스트 통과율: {test_pass_rate}%
아직 테스트를 통과하지 못했습니다.

힌트 제공 시:
1. 입력 처리 방법
2. 적절한 자료구조
3. 핵심 로직의 방향
을 안내해주세요.
"""
    elif hint_purpose == 'optimization':
        if test_pass_rate < 100:
            # 분기 D: optimization + 테스트 미통과
            state['hint_branch'] = 'D'
            state['purpose_context'] = f"""
[힌트 목적: 효율적 완성] (분기 D)

현재 별점: {current_star}개
테스트 통과율: {test_pass_rate}% (아직 미통과)

이전에 통과했지만 코드를 수정하면서 테스트를 통과하지 못하게 되었습니다.
효율성을 고려하면서도 먼저 테스트를 통과하도록 도와주세요.
"""
        else:
            # 테스트 통과한 상태에서 최적화
            # 다음 별 달성 여부 확인
            if current_star == 1 and code_quality >= 70:
                new_star = 2
            elif current_star == 2 and code_quality >= 90:
                new_star = 3
            else:
                new_star = current_star

            if new_star > current_star:
                # 분기 E1: 다음 별 달성
                state['hint_branch'] = 'E1'
                state['purpose_context'] = f"""
[축하! 별 획득!] (분기 E1)

🌟 별 {new_star}개를 획득했습니다!
현재 코드 품질: {code_quality}/100점

{'최고 등급 달성! 다른 풀이 방법도 시도해보세요.' if new_star >= 3 else f'다음 목표: 별 {new_star + 1}개 (품질 90점 필요)'}
"""
            else:
                # 분기 E2: 다음 별 미달성 → 약점 개선
                state['hint_branch'] = 'E2'

                # 약점 분석
                weak_metrics = _identify_weak_metrics(state)
                state['weak_metrics'] = weak_metrics

                if weak_metrics:
                    weak_desc = "\n".join([f"- {w['description']}" for w in weak_metrics])
                    state['purpose_context'] = f"""
[힌트 목적: 코드 품질 개선] (분기 E2)

✅ 좋은 소식: 코드가 정상적으로 동작합니다! 테스트를 모두 통과했습니다.
현재 별점: {current_star}개 ⭐

🎯 다음 별({current_star + 1}개)을 획득하려면 아래 부분을 개선해야 합니다:
{weak_desc}

📍 힌트 제공 시 반드시 포함할 내용:
1. "코드가 정상 동작한다"는 칭찬을 먼저 해주세요
2. 개선이 필요한 **구체적인 코드 위치**(몇 번째 줄, 어떤 함수/변수)를 명시하세요
3. 왜 그 부분이 문제인지 설명하세요
4. 어떻게 수정하면 되는지 구체적인 방법을 제시하세요

다음 별 조건:
- 별 2개: 코드 품질 70점 이상 (현재: {code_quality}점)
- 별 3개: 코드 품질 90점 이상
"""
                else:
                    state['purpose_context'] = f"""
[힌트 목적: 코드 품질 개선] (분기 E2)

✅ 훌륭합니다! 코드가 정상적으로 동작하고, 품질도 우수합니다!
현재 별점: {current_star}개 ⭐

코드가 이미 좋은 상태이지만, 더 나은 코드를 위한 추가 개선점을 찾아보세요.
힌트 제공 시 "코드가 잘 작성되었다"는 점을 먼저 인정해주세요.
"""

    elif hint_purpose == 'optimal':
        # 분기 F: 이미 최적 (별 3개)
        state['hint_branch'] = 'F'
        state['purpose_context'] = f"""
[최고 등급 달성!] (분기 F)

🌟🌟🌟 별 3개 (최적)를 이미 달성했습니다!
현재 코드 품질: {code_quality}/100점

이 문제에 대해 다른 알고리즘이나 자료구조를 사용한 풀이 방법을 제안해주세요.
예: 다른 시간복잡도의 해법, 다른 접근 방식 등
"""
    else:
        state['hint_branch'] = 'B'
        state['purpose_context'] = "[힌트 목적: 일반 도움]"

    return state


# ==================== COH (Chain of Hint) 노드 함수들 ====================

# COH 상수 정의
COH_MAX_DEPTH = {
    '초급': 3,  # 초급 COH3 → 초급 COH2 → 초급 COH1 → 초급
    '중급': 2,  # 중급 COH2 → 중급 COH1 → 중급
    '고급': 1,  # 고급 COH1 → 고급
}

COH_BASE_LEVEL = {
    '초급': 4,  # 기본 레벨 4
    '중급': 7,  # 기본 레벨 7
    '고급': 9,  # 기본 레벨 9
}

# 레벨별 허용 구성요소
# 레벨 1-4 (초급): 모든 6개 구성요소 허용
# 레벨 5-7 (중급): libraries + complexity_hint, edge_cases, improvements
# 레벨 8-9 (고급): complexity_hint, edge_cases, improvements만
ALWAYS_ALLOWED_COMPONENTS = ['complexity_hint', 'edge_cases', 'improvements']
LEVEL_COMPONENTS = {
    1: ['libraries', 'code_example', 'step_by_step', 'complexity_hint', 'edge_cases', 'improvements'],
    2: ['libraries', 'code_example', 'step_by_step', 'complexity_hint', 'edge_cases', 'improvements'],
    3: ['libraries', 'code_example', 'step_by_step', 'complexity_hint', 'edge_cases', 'improvements'],
    4: ['libraries', 'code_example', 'step_by_step', 'complexity_hint', 'edge_cases', 'improvements'],
    5: ['libraries', 'complexity_hint', 'edge_cases', 'improvements'],
    6: ['libraries', 'complexity_hint', 'edge_cases', 'improvements'],
    7: ['libraries', 'complexity_hint', 'edge_cases', 'improvements'],
    8: ['complexity_hint', 'edge_cases', 'improvements'],
    9: ['complexity_hint', 'edge_cases', 'improvements'],
}

import hashlib

def _compute_code_hash(code: str) -> str:
    """코드의 정규화된 해시 계산 (공백/주석 제거 후)"""
    # 공백 정규화
    lines = code.strip().split('\n')
    normalized_lines = []
    for line in lines:
        # 주석 제거
        if '#' in line:
            line = line[:line.index('#')]
        # 공백 정규화
        line = ' '.join(line.split())
        if line:
            normalized_lines.append(line)
    normalized_code = '\n'.join(normalized_lines)
    return hashlib.md5(normalized_code.encode()).hexdigest()


def coh_check_node(state: HintState) -> HintState:
    """
    COH 체크 노드: 이전 힌트 기록을 확인하여 COH 깊이 계산

    플로우차트 기반 COH 결정 로직:
    1. 같은 분기? → 아니오 → COH 초기화 (depth=0)
    2. 문제 해결? → 예 → COH 초기화 (depth=0)
    3. 코드 변경? → 예 → COH 유지 (이전 depth)
    4. 코드 동일 → COH 증가 (depth+1, 최대값 제한)
    """
    if state.get('error'):
        return state

    preset = state.get('preset', '중급')
    hint_branch = state.get('hint_branch', '')
    user_id = state.get('user_id')
    problem_id = state.get('problem_id')
    current_code = state.get('code', '')

    # 현재 코드의 해시 계산
    current_code_hash = _compute_code_hash(current_code)
    state['code_hash'] = current_code_hash

    # 프리셋별 최대 COH 깊이
    max_depth = COH_MAX_DEPTH.get(preset, 2)
    state['coh_max_depth'] = max_depth

    try:
        # 최근 힌트 기록 조회 (같은 문제, 같은 사용자, LangGraph 방식)
        last_hint = HintRequest.objects.filter(
            user_id=user_id,
            problem_str_id=problem_id,
            is_langgraph=True
        ).order_by('-created_at').first()

        if not last_hint:
            # 이전 힌트 없음 → COH 초기화
            state['coh_depth'] = 0
            state['coh_decision'] = 'init_no_history'
            return state

        # 이전 힌트의 분기 확인
        prev_branch = last_hint.hint_branch or ''
        prev_code_hash = last_hint.code_hash or ''
        prev_coh_depth = last_hint.coh_depth or 0

        # 1. 같은 분기인지 확인
        if prev_branch != hint_branch:
            # 분기 변경 → COH 초기화
            state['coh_depth'] = 0
            state['coh_decision'] = 'init_branch_changed'
            return state

        # 2. 문제 해결 분기인지 확인 (C: first_complete, E1: star_achieved)
        solved_branches = ['C', 'E1']
        if prev_branch in solved_branches:
            # 해결 분기에서 같은 분기로 다시 요청 → COH 초기화
            state['coh_depth'] = 0
            state['coh_decision'] = 'init_problem_solved'
            return state

        # 3. 코드 변경 확인
        if prev_code_hash and prev_code_hash != current_code_hash:
            # 코드 변경됨 → COH 유지 (이전 깊이 그대로)
            state['coh_depth'] = min(prev_coh_depth, max_depth)
            state['coh_decision'] = 'keep_code_changed'
            return state

        # 4. 코드 동일 → COH 증가
        new_depth = min(prev_coh_depth + 1, max_depth)
        state['coh_depth'] = new_depth
        state['coh_decision'] = 'increase_same_code'

    except Exception as e:
        # 오류 시 기본값
        state['coh_depth'] = 0
        state['coh_decision'] = f'error: {str(e)}'

    return state


def coh_level_node(state: HintState) -> HintState:
    """
    COH 레벨 계산 노드: 프리셋과 COH 깊이로 최종 힌트 레벨 계산

    레벨 계산 공식:
    hint_level = base_level - min(coh_depth, max_depth)

    레벨 의미:
    - 레벨 1 (초급 COH3): 거의 정답 수준의 상세 힌트
    - 레벨 4 (초급 기본): 직접적이지만 정답은 아닌 힌트
    - 레벨 7 (중급 기본): 개념적 힌트
    - 레벨 9 (고급 기본): 소크라테스식 질문
    """
    if state.get('error'):
        return state

    preset = state.get('preset', '중급')
    coh_depth = state.get('coh_depth', 0)

    base_level = COH_BASE_LEVEL.get(preset, 7)
    hint_level = base_level - coh_depth

    # 레벨 범위 제한 (1-9)
    hint_level = max(1, min(9, hint_level))
    state['hint_level'] = hint_level

    return state


def component_filter_node(state: HintState) -> HintState:
    """
    구성요소 필터링 노드: 힌트 레벨에 따라 허용되는 구성요소 필터링

    필터링 규칙:
    - 레벨 1-4: 모든 구성요소 허용
    - 레벨 5-6: libraries + always_allowed
    - 레벨 7-9: always_allowed만 (complexity_hint, edge_cases, improvements)
    """
    if state.get('error'):
        return state

    hint_level = state.get('hint_level', 7)
    custom_components = state.get('custom_components', {})

    # 해당 레벨에서 허용되는 구성요소
    allowed_components = LEVEL_COMPONENTS.get(hint_level, ALWAYS_ALLOWED_COMPONENTS)

    # 사용자가 선택한 구성요소 중 허용되는 것만 필터링
    filtered_components = {}
    blocked_components = []

    for comp, selected in custom_components.items():
        if selected:
            if comp in allowed_components:
                filtered_components[comp] = True
            else:
                blocked_components.append(comp)
                filtered_components[comp] = False
        else:
            filtered_components[comp] = False

    state['filtered_components'] = filtered_components
    state['blocked_components'] = blocked_components

    # COH 상태 정보 구성 (프론트엔드 전달용)
    preset = state.get('preset', '중급')
    coh_depth = state.get('coh_depth', 0)
    max_depth = state.get('coh_max_depth', COH_MAX_DEPTH.get(preset, 2))

    # 레벨 이름 생성
    if coh_depth == 0:
        level_name = f"{preset} 기본"
    else:
        level_name = f"{preset} COH{coh_depth}"

    state['coh_status'] = {
        'preset': preset,
        'coh_depth': coh_depth,
        'max_depth': max_depth,
        'hint_level': hint_level,
        'level_name': level_name,
        'allowed_components': allowed_components,
        'blocked_components': blocked_components,
        'can_get_more_detailed': coh_depth < max_depth,
        'next_level_hint': f"같은 유형의 힌트를 {max_depth - coh_depth}번 더 요청하면 더 상세한 힌트를 받을 수 있습니다." if coh_depth < max_depth else "이미 가장 상세한 힌트 레벨입니다."
    }

    return state


def _identify_weak_metrics(state: HintState) -> List[Dict[str, Any]]:
    """약점 지표 식별"""
    weak_metrics = []
    static_metrics = state.get('static_metrics', {})
    llm_metrics = state.get('llm_metrics', {})

    # 정적 메트릭 기준
    if static_metrics.get('cyclomatic_complexity', 0) > 10:
        weak_metrics.append({
            'metric': 'cyclomatic_complexity',
            'value': static_metrics['cyclomatic_complexity'],
            'description': '순환 복잡도가 높습니다. 함수를 분리하세요.'
        })

    if static_metrics.get('pep8_violations', 0) > 5:
        weak_metrics.append({
            'metric': 'pep8_violations',
            'value': static_metrics['pep8_violations'],
            'description': 'PEP8 위반이 많습니다. 코드 스타일을 정리하세요.'
        })

    if static_metrics.get('code_quality_score', 100) < 70:
        weak_metrics.append({
            'metric': 'code_quality_score',
            'value': static_metrics['code_quality_score'],
            'description': '코드 품질 점수가 낮습니다.'
        })

    # LLM 메트릭 기준 (3점 미만은 약점)
    llm_metric_names = {
        'algorithm_efficiency': '알고리즘 효율성이 낮습니다.',
        'code_readability': '코드 가독성이 낮습니다.',
        'edge_case_handling': '엣지 케이스 처리가 부족합니다.',
        'code_conciseness': '코드가 불필요하게 복잡합니다.',
        'test_coverage_estimate': '테스트 커버리지가 부족해 보입니다.',
        'security_awareness': '입력 검증이 부족합니다.',
    }

    for metric, description in llm_metric_names.items():
        if llm_metrics.get(metric, 3) < 3:
            weak_metrics.append({
                'metric': metric,
                'value': llm_metrics[metric],
                'description': description
            })

    return weak_metrics


def build_prompt_node(state: HintState) -> HintState:
    """프롬프트 구성 노드 (COH 레벨 반영)"""
    if state.get('error'):
        return state

    preset = state.get('preset', '중급')
    # COH로 필터링된 구성요소 사용 (없으면 원본 사용)
    custom_components = state.get('filtered_components', state.get('custom_components', {}))
    purpose_context = state.get('purpose_context', '')
    previous_hints = state.get('previous_hints', [])
    hint_level = state.get('hint_level', 7)
    coh_depth = state.get('coh_depth', 0)

    # COH 레벨에 따른 힌트 스타일 결정
    # 레벨 1-2: 거의 정답 수준
    # 레벨 3-4: 직접적 힌트
    # 레벨 5-6: 개념적 힌트
    # 레벨 7-8: 추상적 힌트
    # 레벨 9: 소크라테스식 질문

    if hint_level <= 2:
        level_instruction = f"""
[힌트 레벨: {hint_level}/9 - 매우 상세 (COH{coh_depth})]
- 거의 정답에 가까운 상세한 설명을 제공하세요
- 사용할 함수명, 라이브러리명, 구체적인 로직을 설명하세요
- 코드 구조와 흐름을 단계별로 자세히 안내하세요
- 학생이 따라 작성할 수 있을 정도로 구체적으로 설명하세요
"""
    elif hint_level <= 4:
        level_instruction = f"""
[힌트 레벨: {hint_level}/9 - 직접적 ({preset})]
- 직접적으로 설명해주세요
- 사용할 함수명, 라이브러리명을 언급해도 됩니다
- 구체적인 예시를 들어주세요
- 정답 코드 전체를 제공하지는 마세요
"""
    elif hint_level <= 6:
        level_instruction = f"""
[힌트 레벨: {hint_level}/9 - 개념적 ({preset} COH{coh_depth if coh_depth > 0 else '기본'})]
- 개념적으로 설명해주세요
- 자료구조, 알고리즘 개념으로 힌트를 제공하세요
- 구체적인 코드는 제공하지 마세요
- 방향만 제시하고 학생이 스스로 구현하게 하세요
"""
    elif hint_level <= 8:
        level_instruction = f"""
[힌트 레벨: {hint_level}/9 - 추상적 ({preset})]
- 높은 수준의 개념만 언급하세요
- 구체적인 구현 방법은 제시하지 마세요
- "~를 생각해보세요" 형태로 방향만 제시하세요
"""
    else:  # 레벨 9
        level_instruction = f"""
[힌트 레벨: {hint_level}/9 - 소크라테스식 (고급)]
- 직접적인 답을 주지 마세요
- 질문 형태로 힌트를 제공하세요
- "이 문제에서 중복을 피하려면 어떤 자료구조가 적합할까요?" 같은 형태
- 학생이 스스로 답을 찾아가도록 유도하세요
"""

    # 선택된 구성요소
    components_instruction = """
[응답에 포함할 항목]
- summary: 힌트 요약 (필수, 위 레벨에 맞게)
"""

    component_descriptions = {
        'libraries': '- libraries: 사용하면 좋은 라이브러리 목록 (리스트)',
        'code_example': '- code_example: 참고할 코드 예시 (문자열, 5-10줄의 실행 가능한 Python 코드. 리스트가 아닌 단일 문자열로 작성)',
        'step_by_step': '- step_by_step: 단계별 해결 방법 (리스트)',
        'complexity_hint': '- complexity_hint: 시간/공간 복잡도 힌트',
        'edge_cases': '- edge_cases: 고려해야 할 엣지 케이스 목록',
        'improvements': '- improvements: 현재 코드 개선점 (리스트)',
    }

    for comp, desc in component_descriptions.items():
        if custom_components.get(comp, False):
            components_instruction += f"\n{desc}"

    # 이전 힌트 컨텍스트
    previous_context = ""
    if previous_hints and isinstance(previous_hints, list) and len(previous_hints) > 0:
        # previous_hints가 문자열 리스트인지, 딕셔너리 리스트인지 확인
        hints_text = []
        for i, h in enumerate(previous_hints[-3:]):
            if isinstance(h, str):
                hint_text = h[:100]
            elif isinstance(h, dict):
                # 딕셔너리인 경우 hint_text 또는 hint 키 사용
                hint_text = str(h.get('hint_text', h.get('hint', str(h))))[:100]
            else:
                hint_text = str(h)[:100]
            hints_text.append(f'{i+1}. {hint_text}...')

        previous_context = f"""
[이전에 제공한 힌트들]
{chr(10).join(hints_text)}

위 힌트들과 중복되지 않는 새로운 관점의 힌트를 제공해주세요.
"""

    prompt = f"""당신은 코딩 테스트 힌트를 제공하는 AI 튜터입니다.

{purpose_context}

{level_instruction}

[문제 정보]
제목: {state['problem_title']}
설명: {state['problem_description'][:500]}...

[학생의 현재 코드]
```python
{state['user_code'][:1500]}
```

[코드 분석 결과]
- 테스트 통과율: {state['static_metrics'].get('test_pass_rate', 0)}%
- 코드 품질: {state['static_metrics'].get('code_quality_score', 0)}/100
- 순환 복잡도: {state['static_metrics'].get('cyclomatic_complexity', 0)}
- PEP8 위반: {state['static_metrics'].get('pep8_violations', 0)}개

[LLM 평가 결과]
- 알고리즘 효율성: {state['llm_metrics'].get('algorithm_efficiency', 3)}/5
- 코드 가독성: {state['llm_metrics'].get('code_readability', 3)}/5
- 엣지 케이스 처리: {state['llm_metrics'].get('edge_case_handling', 3)}/5
{previous_context}

{components_instruction}

[중요 규칙]
1. 직접적인 정답 코드를 제공하지 마세요
2. 학생이 스스로 해결할 수 있도록 방향을 제시하세요
3. 한국어로 친절하게 답변하세요
4. JSON 형식으로 응답하세요

응답 예시:
{{
    "summary": "힌트 요약 내용...",
    "libraries": ["collections", "itertools"],
    "code_example": "# 예시 코드\\ndef example_func():\\n    data = [1, 2, 3]\\n    return sum(data)",
    "step_by_step": ["1단계: ...", "2단계: ..."],
    "complexity_hint": "시간복잡도 O(n), 공간복잡도 O(1)",
    "edge_cases": ["빈 배열 입력", "음수 값"],
    "improvements": ["변수명 개선", "중복 코드 제거"]
}}

[중요: code_example은 리스트가 아닌 단일 문자열로 작성하세요. 줄바꿈은 \\n으로 표현합니다.]

JSON으로 응답하세요:"""

    state['llm_prompt'] = prompt
    return state


def generate_hint_node(state: HintState) -> HintState:
    """힌트 생성 노드 (GPT-4.1 호출)"""
    if state.get('error'):
        return state

    try:
        ai_config = AIModelConfig.get_config()

        if ai_config.mode != 'openai' or not ai_config.openai_api_key:
            state['error'] = 'OpenAI API 키가 설정되지 않았습니다.'
            return state

        client = OpenAI(api_key=ai_config.openai_api_key)
        model_name = ai_config.model_name or 'gpt-4.1'

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "당신은 코딩 교육 전문가입니다. JSON 형식으로만 응답하세요."},
                {"role": "user", "content": state['llm_prompt']}
            ],
            temperature=0.5,
            max_tokens=1000
        )

        response_text = response.choices[0].message.content.strip()

        # JSON 파싱
        try:
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0]

            hint_content = json.loads(response_text)
            state['hint_content'] = hint_content
        except:
            state['hint_content'] = {
                'summary': response_text
            }

    except Exception as e:
        state['error'] = f"힌트 생성 실패: {str(e)}"

    return state


def format_hint_node(state: HintState) -> HintState:
    """최종 힌트 포맷팅 노드"""
    if state.get('error'):
        state['final_hint'] = f"힌트 생성 중 오류가 발생했습니다: {state['error']}"
        state['hint_type'] = 'error'
        return state

    hint_content = state.get('hint_content', {})
    branch = state.get('hint_branch', '')

    # 분기에 따른 힌트 타입 결정
    hint_type_map = {
        'A': 'syntax_fix',
        'B': 'completion',
        'C': 'first_complete',
        'D': 'efficient_completion',
        'E1': 'star_achieved',
        'E2': 'quality_improvement',
        'F': 'alternative_solution'
    }

    state['hint_type'] = hint_type_map.get(branch, 'general')

    # 최종 힌트 포맷팅
    final_hint = hint_content.get('summary', '')

    if hint_content.get('libraries'):
        final_hint += f"\n\n📚 추천 라이브러리: {', '.join(hint_content['libraries'])}"

    if hint_content.get('step_by_step'):
        final_hint += "\n\n📝 단계별 접근:\n" + "\n".join(hint_content['step_by_step'])

    if hint_content.get('complexity_hint'):
        final_hint += f"\n\n⏱️ 복잡도 힌트: {hint_content['complexity_hint']}"

    if hint_content.get('edge_cases'):
        final_hint += "\n\n⚠️ 엣지 케이스:\n- " + "\n- ".join(hint_content['edge_cases'])

    if hint_content.get('improvements'):
        final_hint += "\n\n💡 개선 사항:\n- " + "\n- ".join(hint_content['improvements'])

    if hint_content.get('code_example'):
        code_example = hint_content['code_example']
        # 리스트로 왔을 경우 문자열로 변환
        if isinstance(code_example, list):
            code_example = '\n'.join(code_example)
        # \\n을 실제 줄바꿈으로 변환
        code_example = code_example.replace('\\n', '\n')
        final_hint += f"\n\n💻 코드 예시:\n```python\n{code_example}\n```"

    state['final_hint'] = final_hint
    return state


def save_node(state: HintState) -> HintState:
    """메트릭 저장 및 배지 체크 노드 (code_hash, hint_branch 포함)"""
    # 힌트 기록은 API 엔드포인트에서 저장하지만,
    # 여기서 code_hash와 hint_branch가 state에 있는지 확인
    # (coh_check_node에서 code_hash 설정, branch_node에서 hint_branch 설정)
    return state


# ==================== 병렬 실행 및 스킵 노드 ====================

def parallel_analysis_node(state: HintState) -> HintState:
    """
    병렬 분석 노드: static_analysis와 llm_eval을 동시에 실행
    (Python의 concurrent.futures 사용)
    """
    if state.get('error'):
        return state

    import concurrent.futures

    def run_static():
        return static_analysis_node(state.copy())

    def run_llm_eval():
        return llm_eval_node(state.copy())

    # 병렬 실행
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_static = executor.submit(run_static)
        future_llm = executor.submit(run_llm_eval)

        static_result = future_static.result()
        llm_result = future_llm.result()

    # 결과 병합
    state['static_metrics'] = static_result.get('static_metrics', {})
    state['llm_metrics'] = llm_result.get('llm_metrics', {})

    # 에러 체크
    if static_result.get('error'):
        state['error'] = static_result['error']
    elif llm_result.get('error'):
        state['error'] = llm_result['error']

    return state


# 간단한 케이스 스킵용 정적 힌트 메시지
SKIP_HINTS = {
    'A': {  # 코드 없음 / 문법 오류
        'message': """⚠️ 먼저 코드를 작성하거나 문법 오류를 수정해주세요.

📝 기본 구조 힌트:
1. `input()`으로 입력을 받으세요
2. 문제의 조건에 맞게 로직을 작성하세요
3. `print()`로 결과를 출력하세요

💡 Python 기본 문법을 다시 확인해보세요.""",
        'hint_type': 'syntax_fix'
    },
    'C': {  # 첫 정답 축하
        'message': """🎉 축하합니다! 테스트를 처음 통과했습니다!

⭐ 별 1개를 획득했습니다!

💡 다음 단계:
- 별 2개: 코드 품질 70점 이상 달성
- 별 3개: 코드 품질 90점 이상 달성

코드 품질을 높이려면:
- 불필요한 코드 제거
- 변수명 개선
- 효율적인 알고리즘 적용

'힌트 받기'를 다시 눌러 개선점 확인하세요!""",
        'hint_type': 'first_complete'
    },
    'E1': {  # 별 획득 축하
        'message': """🌟 축하합니다! 별을 획득했습니다!

코드 품질이 크게 향상되었습니다.

💡 최고 등급(별 3개)을 위해:
- 시간 복잡도 최적화
- 공간 복잡도 개선
- 더 효율적인 알고리즘 적용

다른 풀이 방법도 시도해보세요!""",
        'hint_type': 'star_achieved'
    }
}


def should_skip_coh(state: HintState) -> str:
    """
    COH 계산을 스킵할지 결정하는 라우터 함수 (branch_node 직후)
    A, C, E1 분기는 정적 메시지를 반환하므로 COH 계산 불필요
    Returns: 'skip' 또는 'continue'
    """
    hint_branch = state.get('hint_branch', '')
    if hint_branch in SKIP_HINTS:
        return 'skip'
    return 'continue'


def should_skip_llm(state: HintState) -> str:
    """
    LLM 호출을 스킵할지 결정하는 라우터 함수
    Returns: 'skip' 또는 'continue'
    """
    hint_branch = state.get('hint_branch', '')

    # 스킵 가능한 분기: A (코드 없음/문법 오류), C (첫 정답), E1 (별 획득)
    if hint_branch in SKIP_HINTS:
        return 'skip'
    return 'continue'


def skip_llm_node(state: HintState) -> HintState:
    """
    LLM 호출 스킵 노드: 정적 메시지로 힌트 생성
    """
    hint_branch = state.get('hint_branch', '')
    skip_config = SKIP_HINTS.get(hint_branch, {})

    # 정적 메시지 사용
    state['hint_content'] = {'summary': skip_config.get('message', '')}
    state['final_hint'] = skip_config.get('message', '')
    state['hint_type'] = skip_config.get('hint_type', 'static')

    return state


# ==================== 그래프 빌드 ====================

def build_hint_graph():
    """
    LangGraph 힌트 그래프 빌드 (병렬 분석 + 조건부 COH/LLM 스킵)

    플로우:
    input → purpose → parallel_analysis → branch → [조건부 분기 1: should_skip_coh]
        - skip (A,C,E1): skip_llm → save → END
        - continue (B,D,E2,F): coh_check → coh_level → component_filter
                              → prompt → llm_hint → format → save → END
    """
    if not LANGGRAPH_AVAILABLE:
        return None

    workflow = StateGraph(HintState)

    # 노드 추가
    workflow.add_node("input_node", input_node)
    workflow.add_node("purpose_node", purpose_node)
    workflow.add_node("parallel_analysis_node", parallel_analysis_node)  # 병렬 분석
    workflow.add_node("branch_node", branch_decision_node)
    # COH 관련 노드 (B, D, E2, F 분기만 사용)
    workflow.add_node("coh_check_node", coh_check_node)
    workflow.add_node("coh_level_node", coh_level_node)
    workflow.add_node("component_filter_node", component_filter_node)
    # LLM 스킵 노드 (A, C, E1 분기용)
    workflow.add_node("skip_llm_node", skip_llm_node)
    # LLM 호출 노드
    workflow.add_node("prompt_node", build_prompt_node)
    workflow.add_node("llm_hint_node", generate_hint_node)
    workflow.add_node("format_node", format_hint_node)
    workflow.add_node("save_node", save_node)

    # 엣지 연결
    workflow.set_entry_point("input_node")
    workflow.add_edge("input_node", "purpose_node")
    workflow.add_edge("purpose_node", "parallel_analysis_node")  # 병렬 분석
    workflow.add_edge("parallel_analysis_node", "branch_node")

    # 조건부 분기 1: COH 스킵 여부 (branch_node 직후)
    # A, C, E1 → 정적 메시지 반환 (COH 계산 불필요)
    # B, D, E2, F → COH 계산 필요
    workflow.add_conditional_edges(
        "branch_node",
        should_skip_coh,
        {
            "skip": "skip_llm_node",      # A, C, E1: COH 스킵 → 정적 힌트
            "continue": "coh_check_node"  # B, D, E2, F: COH 계산 진행
        }
    )

    # COH 경로 (B, D, E2, F 분기)
    workflow.add_edge("coh_check_node", "coh_level_node")
    workflow.add_edge("coh_level_node", "component_filter_node")
    workflow.add_edge("component_filter_node", "prompt_node")
    workflow.add_edge("prompt_node", "llm_hint_node")
    workflow.add_edge("llm_hint_node", "format_node")
    workflow.add_edge("format_node", "save_node")

    # 스킵 경로 (A, C, E1 분기)
    workflow.add_edge("skip_llm_node", "save_node")

    workflow.add_edge("save_node", END)

    return workflow.compile()


# 전역 그래프 인스턴스 (싱글톤)
_hint_graph = None

def get_hint_graph():
    """힌트 그래프 인스턴스 반환"""
    global _hint_graph
    if _hint_graph is None:
        _hint_graph = build_hint_graph()
    return _hint_graph


# ==================== 내부 함수 (hint_api.py에서 호출용) ====================

def run_langgraph_hint(user, problem_id, user_code, preset='중급', custom_components=None, previous_hints=None):
    """
    LangGraph 힌트 생성 내부 함수
    hint_api.py에서 직접 호출 가능

    Returns:
        tuple: (success: bool, data: dict, error: str or None, status_code: int)
    """
    if custom_components is None:
        custom_components = {}
    if previous_hints is None:
        previous_hints = []

    if not LANGGRAPH_AVAILABLE:
        return (
            False,
            None,
            'LangGraph가 설치되지 않았습니다. pip install langgraph langchain-core를 실행하세요.',
            503
        )

    if not problem_id:
        return (False, None, '문제 ID가 필요합니다.', 400)

    # 초기 상태 구성 (COH 필드 포함)
    initial_state: HintState = {
        'problem_id': str(problem_id),
        'problem_title': '',
        'problem_description': '',
        'user_code': user_code,
        'code': user_code,  # coh_check_node에서 code_hash 계산용
        'previous_hints': previous_hints,
        'preset': preset,
        'custom_components': custom_components,
        'user_id': user.id,
        'static_metrics': {},
        'llm_metrics': {},
        'current_star_count': 0,
        'hint_purpose': '',
        'hint_branch': '',
        'purpose_context': '',
        'weak_metrics': [],
        # COH 관련 필드 초기화
        'coh_depth': 0,
        'coh_max_depth': COH_MAX_DEPTH.get(preset, 2),
        'hint_level': COH_BASE_LEVEL.get(preset, 7),
        'code_hash': '',  # coh_check_node에서 계산됨
        'coh_decision': '',  # COH 결정 이유
        'filtered_components': {},
        'blocked_components': [],
        'coh_status': {},
        # 힌트 생성 필드
        'llm_prompt': '',
        'hint_content': {},
        'final_hint': '',
        'hint_type': '',
        'error': None
    }

    import sys
    import logging
    logger = logging.getLogger(__name__)

    try:
        logger.error(f"[LangGraph DEBUG] Starting run_langgraph_hint for user={user.id}, problem={problem_id}")
        sys.stderr.write(f"[LangGraph DEBUG] Starting run_langgraph_hint for user={user.id}, problem={problem_id}\n")
        sys.stderr.flush()

        graph = get_hint_graph()
        if graph is None:
            logger.error("[LangGraph DEBUG] Graph is None!")
            return (False, None, 'LangGraph 초기화 실패', 500)

        logger.error(f"[LangGraph DEBUG] Invoking graph with initial_state...")
        sys.stderr.write(f"[LangGraph DEBUG] Invoking graph...\n")
        sys.stderr.flush()

        # 그래프 실행
        final_state = graph.invoke(initial_state)

        logger.error(f"[LangGraph DEBUG] Graph invoke complete. final_hint length={len(final_state.get('final_hint', ''))}")
        sys.stderr.write(f"[LangGraph DEBUG] Graph invoke complete. final_hint length={len(final_state.get('final_hint', ''))}\n")
        sys.stderr.flush()

        # 힌트 기록 저장 (code_hash, hint_branch, coh_depth 포함)
        logger.error(f"[LangGraph DEBUG] Saving HintRequest...")
        hint_record = HintRequest.objects.create(
            user=user,
            problem_str_id=problem_id,
            user_code=user_code,
            hint_response=final_state.get('final_hint', ''),
            hint_type=final_state.get('hint_type', 'langgraph'),
            is_langgraph=True,
            # COH 관련 필드 저장
            code_hash=final_state.get('code_hash', ''),
            hint_branch=final_state.get('hint_branch', ''),
            coh_depth=final_state.get('coh_depth', 0)
        )
        logger.error(f"[LangGraph DEBUG] HintRequest saved: id={hint_record.id}, branch={final_state.get('hint_branch')}, code_hash={final_state.get('code_hash', '')[:8]}...")

        result_data = {
            'hint': final_state.get('final_hint', ''),
            'hint_content': final_state.get('hint_content', {}),
            'hint_type': final_state.get('hint_type', ''),
            'hint_branch': final_state.get('hint_branch', ''),
            'current_star': final_state.get('current_star_count', 0),
            'hint_purpose': final_state.get('hint_purpose', ''),
            'static_metrics': final_state.get('static_metrics', {}),
            'llm_metrics': final_state.get('llm_metrics', {}),
            'weak_metrics': final_state.get('weak_metrics', []),
            # COH 관련 정보 추가
            'coh_status': final_state.get('coh_status', {}),
            'hint_level': final_state.get('hint_level', 7),
            'coh_depth': final_state.get('coh_depth', 0),
            'coh_decision': final_state.get('coh_decision', ''),  # COH 결정 이유
            'code_hash': final_state.get('code_hash', ''),  # 코드 해시
            'filtered_components': final_state.get('filtered_components', {}),
            'blocked_components': final_state.get('blocked_components', []),
            'method': 'langgraph'
        }

        logger.error(f"[LangGraph DEBUG] Returning success response")
        sys.stderr.write(f"[LangGraph DEBUG] Returning success response\n")
        sys.stderr.flush()

        return (True, result_data, None, 200)

    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        logger.error(f"[LangGraph Error] {error_detail}")
        sys.stderr.write(f"[LangGraph Error] {error_detail}\n")
        sys.stderr.flush()
        return (
            False,
            None,
            f'LangGraph 실행 오류: {str(e)}\n{error_detail}',
            500
        )


# ==================== API 엔드포인트 ====================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_hint_langgraph(request):
    """
    LangGraph 기반 힌트 요청 API

    Request Body:
    - problem_id: 문제 ID (필수)
    - user_code: 사용자 코드 (필수)
    - preset: 힌트 레벨 ('초급', '중급', '고급') - 기본: '중급'
    - custom_components: 선택할 구성요소 dict
        - libraries: bool
        - code_example: bool
        - step_by_step: bool
        - complexity_hint: bool
        - edge_cases: bool
        - improvements: bool
    - previous_hints: 이전 힌트 목록 (선택)
    """
    problem_id = request.data.get('problem_id')
    user_code = request.data.get('user_code', '')
    preset = request.data.get('preset', '중급')
    custom_components = request.data.get('custom_components', {})
    previous_hints = request.data.get('previous_hints', [])

    success, data, error, status_code = run_langgraph_hint(
        user=request.user,
        problem_id=problem_id,
        user_code=user_code,
        preset=preset,
        custom_components=custom_components,
        previous_hints=previous_hints
    )

    if success:
        return Response({'success': True, 'data': data})
    else:
        return Response({
            'success': False,
            'error': error,
            'fallback_available': True,
            'message': '기존 API 방식(/coding-test/hints/)을 사용해주세요.'
        }, status=status_code)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_langgraph_status(request):
    """LangGraph 시스템 상태 확인 (COH 정보 포함)"""
    return Response({
        'success': True,
        'data': {
            'langgraph_available': LANGGRAPH_AVAILABLE,
            'openai_available': OPENAI_AVAILABLE,
            'graph_initialized': get_hint_graph() is not None if LANGGRAPH_AVAILABLE else False,
            'nodes': [
                'input_node - 입력 검증 및 문제 로드',
                'purpose_node - 별점 조회 및 목적 결정',
                'static_node - 정적 분석 (6개 메트릭)',
                'llm_eval_node - LLM 평가 (6개 메트릭)',
                'branch_node - 분기 결정 (A~F)',
                'coh_check_node - COH 깊이 계산',
                'coh_level_node - 힌트 레벨 계산 (1-9)',
                'component_filter_node - 구성요소 필터링',
                'prompt_node - 프롬프트 구성',
                'llm_hint_node - 힌트 생성 (GPT-4.1)',
                'format_node - 힌트 포맷팅',
                'save_node - 저장'
            ],
            'branches': {
                'A': '문법 오류 수정',
                'B': '코드 완성 힌트',
                'C': '테스트 통과 축하',
                'D': '효율적 완성',
                'E1': '별 획득 축하',
                'E2': '품질 개선',
                'F': '다른 풀이 제안'
            },
            'presets': ['초급', '중급', '고급'],
            'components': ['libraries', 'code_example', 'step_by_step', 'complexity_hint', 'edge_cases', 'improvements'],
            # COH 관련 정보
            'coh_system': {
                'description': 'Chain of Hint - 같은 유형의 힌트 반복 요청 시 점점 상세해지는 시스템',
                'max_depth_per_preset': COH_MAX_DEPTH,
                'base_level_per_preset': COH_BASE_LEVEL,
                'hint_levels': {
                    '1-2': '매우 상세 (거의 정답 수준)',
                    '3-4': '직접적 (초급)',
                    '5-6': '개념적 (중급)',
                    '7-8': '추상적',
                    '9': '소크라테스식 질문 (고급)'
                },
                'component_availability': {
                    'level_1_4': '모든 구성요소 허용',
                    'level_5_6': 'libraries + complexity_hint + edge_cases + improvements',
                    'level_7_9': 'complexity_hint + edge_cases + improvements만'
                }
            }
        }
    })
