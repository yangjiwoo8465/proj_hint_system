"""
힌트 챗봇 API
"""
import json
import requests
import os
from pathlib import Path
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from .models import HintRequest, Problem, AIModelConfig


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_hint(request):
    """힌트 요청 API - AI 설정에 따라 API 또는 로컬 모델 사용"""
    problem_id = request.data.get('problem_id')
    user_code = request.data.get('user_code', '')

    # AI 설정 가져오기
    ai_config = AIModelConfig.get_config()

    if not problem_id:
        return Response({
            'success': False,
            'message': '문제 ID가 필요합니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Load problem from JSON
    try:
        problems_file = Path(settings.BASE_DIR) / 'apps' / 'coding_test' / 'data' / 'problems_multi_solution_complete_fixed.json'
        with open(problems_file, 'r', encoding='utf-8') as f:
            problems = json.load(f)

        problem = next((p for p in problems if p.get('problem_id') == problem_id), None)
        if not problem:
            return Response({
                'success': False,
                'message': '문제를 찾을 수 없습니다.'
            }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'문제 로드 실패: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    solution_code = problem.get('solution_code', '')
    problem_description = problem.get('description', '')
    problem_title = problem.get('title', '')

    # Qwen 모델 프롬프트 작성
    prompt = f"""당신은 코딩 교육 전문가입니다. 소크라테스 학습법을 사용하여 학생이 스스로 문제를 해결할 수 있도록 힌트를 제공해야 합니다.

**중요 규칙:**
1. 절대로 정답 코드를 직접 알려주지 마세요
2. 질문을 통해 학생이 스스로 생각하도록 유도하세요
3. 힌트는 구체적이되, 답을 직접 주지 않아야 합니다
4. 한 번에 하나의 힌트만 제공하세요 (200자 이내)

**문제 정보:**
제목: {problem_title}
설명: {problem_description}

**정답 코드 (참고용, 학생에게 보여주지 마세요):**
```python
{solution_code}
```

**학생이 작성한 코드:**
```python
{user_code if user_code else '(아직 작성하지 않음)'}
```

학생의 코드를 분석하고, 정답 코드와 비교하여:
1. 학생이 어느 단계까지 올바르게 작성했는지 파악하세요
2. 다음에 해결해야 할 로직이 무엇인지 식별하세요
3. 소크라테스식 질문이나 간단한 힌트를 제공하세요

힌트 (200자 이내):"""

    # AI 설정에 따라 힌트 생성 방식 결정
    if ai_config.mode == 'api':
        # API 방식: Hugging Face Inference API 사용
        api_key = ai_config.api_key if ai_config.api_key else os.environ.get('HUGGINGFACE_API_KEY', '')

        if not api_key:
            # API 키가 없으면 간단한 fallback 힌트 제공
            if not user_code or len(user_code.strip()) < 10:
                hint_response = "먼저 문제를 단계별로 나누어 생각해보세요. 입력을 어떻게 처리하고, 어떤 연산을 해야 할까요?"
            else:
                hint_response = "작성하신 코드를 보니 좋은 시작입니다! 다음 단계로, 엣지 케이스(예: 빈 입력, 최소값/최대값)를 고려해보셨나요?"
        else:
            try:
                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                }
                payload = {
                    'inputs': prompt,
                    'parameters': {
                        'max_new_tokens': 200,
                        'temperature': 0.7,
                        'top_p': 0.9,
                        'return_full_text': False
                    }
                }

                response = requests.post(
                    f'https://api-inference.huggingface.co/models/{ai_config.model_name}',
                    headers=headers,
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        hint_response = result[0].get('generated_text', '').strip()
                    elif isinstance(result, dict):
                        hint_response = result.get('generated_text', '').strip()
                    else:
                        hint_response = "힌트를 생성하는 중 오류가 발생했습니다. 문제를 다시 읽고 예제를 분석해보세요."
                else:
                    error_detail = response.text
                    print(f'Hugging Face API Error (Status {response.status_code}): {error_detail}')
                    hint_response = f"힌트 생성 실패 (상태 코드: {response.status_code}). 문제의 입출력 예시를 먼저 분석해보세요."
            except Exception as e:
                print(f'Qwen API Error: {str(e)}')
                hint_response = "힌트: 문제의 입력과 출력 형식을 먼저 파악하고, 단계별로 로직을 구성해보세요."

    elif ai_config.mode == 'local':
        # 로컬 모드: 모델이 로드되어 있는지 확인
        if not ai_config.is_model_loaded:
            hint_response = "모델이 로드되지 않았습니다. 관리자에게 문의하세요."
        else:
            # TODO: 실제 로컬 모델 사용 로직 구현
            # from transformers import AutoModelForCausalLM, AutoTokenizer
            # model, tokenizer = get_loaded_model()
            # inputs = tokenizer(prompt, return_tensors="pt")
            # outputs = model.generate(**inputs, max_new_tokens=200)
            # hint_response = tokenizer.decode(outputs[0])
            hint_response = "[로컬 모델] 문제를 단계별로 나누어 생각해보세요."
    else:
        hint_response = "알 수 없는 AI 모드입니다."

    # Save hint request to database
    try:
        problem_obj, _ = Problem.objects.get_or_create(
            problem_id=problem_id,
            defaults={
                'title': problem_title,
                'description': problem_description,
                'level': problem.get('level', 1),
                'step_title': problem.get('step_title', ''),
                'input_description': problem.get('input_description', ''),
                'output_description': problem.get('output_description', ''),
                'tags': problem.get('tags', []),
                'examples': problem.get('examples', []),
                'solutions': problem.get('solutions', [])
            }
        )

        model_used = f"{ai_config.get_mode_display()}: {ai_config.model_name}"
        HintRequest.objects.create(
            user=request.user,
            problem=problem_obj,
            hint_level='medium',  # 기본값
            user_code=user_code or '(empty)',
            hint_response=hint_response,
            model_used=model_used
        )
    except Exception as e:
        print(f'Failed to save hint request: {str(e)}')

    return Response({
        'success': True,
        'data': {
            'hint': hint_response,
            'problem_id': problem_id
        }
    })
