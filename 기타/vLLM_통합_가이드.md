# vLLM 통합 가이드

## 📚 vLLM 개요

### vLLM이란?
- **Very Large Language Model serving**의 약자
- UC Berkeley LMSYS 연구팀 개발
- **고성능 LLM 추론 및 서빙 엔진**

### 핵심 기술

#### 1. PagedAttention
```
기존 방식:              vLLM PagedAttention:
┌─────────────┐        ┌───┬───┬───┬───┐
│ KV Cache    │        │ P1│ P2│ P3│ P4│  페이지 단위 관리
│ (연속 할당) │        ├───┼───┼───┼───┤
│             │        │ P5│   │   │   │  필요한 만큼만 할당
│ [낭비 많음] │        └───┴───┴───┴───┘
└─────────────┘        [메모리 효율 24배↑]
```

- GPU 메모리를 페이지 단위로 관리
- KV 캐시 동적 할당으로 메모리 낭비 최소화
- **처리량 24배 향상**

#### 2. Continuous Batching
```
기존 Static Batching:
Batch 1: [Req1, Req2, Req3] → 모두 완료될 때까지 대기
         ▼ GPU 유휴
Batch 2: [Req4, Req5, Req6]

vLLM Continuous Batching:
[Req1, Req2, Req3] → Req2 완료 즉시 Req4 투입
        ▼ GPU 항상 100% 활용
[Req1, Req4, Req3] → Req1 완료 즉시 Req5 투입
```

#### 3. 성능 비교

| 항목 | Hugging Face | vLLM | TensorRT-LLM |
|------|--------------|------|--------------|
| **처리량** | 1x | **24x** | 10x |
| **지연시간** | 높음 | **낮음** | 낮음 |
| **메모리 효율** | 낮음 | **매우 높음** | 높음 |
| **구축 난이도** | 쉬움 | **쉬움** | 어려움 |
| **OpenAI API** | ✗ | **✓** | ✗ |

---

## 🚀 프로젝트 통합 방법

### 1. vLLM Docker Compose 설정

**파일: `docker-compose.vllm.yml`**

```yaml
version: '3.8'

services:
  vllm-server:
    image: vllm/vllm-openai:latest
    container_name: hint_system_vllm
    ports:
      - "8001:8000"
    volumes:
      - ./models:/root/.cache/huggingface  # 모델 캐시
    environment:
      - HUGGING_FACE_HUB_TOKEN=${HF_TOKEN}
    command: >
      --model ModelCloud/Brumby-14B-Base-GPTQMODEL-W4A16-v2
      --host 0.0.0.0
      --port 8000
      --tensor-parallel-size 1
      --gpu-memory-utilization 0.9
      --max-model-len 4096
      --trust-remote-code
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    networks:
      - hint_system_network
    restart: unless-stopped

networks:
  hint_system_network:
    external: true
```

### 2. Backend AI 설정 모델 업데이트

**파일: `backend/apps/coding_test/models.py`**

```python
class AIModelConfig(models.Model):
    """AI 모델 설정"""
    MODE_CHOICES = [
        ('api', 'API 방식 (Hugging Face)'),
        ('vllm', 'vLLM 서버'),  # 추가
        ('local', '로컬 모델'),
    ]

    MODEL_CHOICES = [
        ('Qwen/Qwen2.5-Coder-32B-Instruct', 'Qwen 2.5 Coder 32B'),
        ('Qwen/Qwen2.5-Coder-7B-Instruct', 'Qwen 2.5 Coder 7B'),
        ('ModelCloud/Brumby-14B-Base-GPTQMODEL-W4A16-v2', 'Brumby 14B (Quantized)'),  # 추가
    ]

    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='api')
    model_name = models.CharField(max_length=200, default='Qwen/Qwen2.5-Coder-7B-Instruct')
    api_key = models.CharField(max_length=200, blank=True, null=True)
    vllm_url = models.CharField(max_length=200, default='http://vllm-server:8000', blank=True)  # 추가
    # ... 기존 필드
```

### 3. vLLM API 연동

**파일: `backend/apps/coding_test/vllm_client.py` (신규 생성)**

```python
"""vLLM 클라이언트"""
import requests
from typing import Optional, Dict, Any

class vLLMClient:
    """vLLM OpenAI 호환 API 클라이언트"""

    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url.rstrip('/')
        self.chat_endpoint = f"{self.base_url}/v1/chat/completions"
        self.models_endpoint = f"{self.base_url}/v1/models"

    def check_health(self) -> bool:
        """서버 상태 확인"""
        try:
            response = requests.get(self.models_endpoint, timeout=5)
            return response.status_code == 200
        except:
            return False

    def generate_hint(
        self,
        prompt: str,
        model: str = "ModelCloud/Brumby-14B-Base-GPTQMODEL-W4A16-v2",
        max_tokens: int = 200,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> Optional[str]:
        """힌트 생성"""
        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "당신은 소크라테스식 학습법을 사용하는 코딩 교육 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "stream": False
            }

            response = requests.post(
                self.chat_endpoint,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                print(f"vLLM API Error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"vLLM Client Error: {str(e)}")
            return None
```

### 4. 힌트 API 업데이트

**파일: `backend/apps/coding_test/hint_api.py`**

```python
from .vllm_client import vLLMClient

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_hint(request):
    """힌트 요청 API"""
    # ... 기존 코드 ...

    ai_config = AIModelConfig.get_config()

    # vLLM 모드 추가
    if ai_config.mode == 'vllm':
        try:
            vllm_client = vLLMClient(base_url=ai_config.vllm_url)

            if not vllm_client.check_health():
                hint_response = "vLLM 서버에 연결할 수 없습니다. 관리자에게 문의하세요."
            else:
                hint_response = vllm_client.generate_hint(
                    prompt=prompt,
                    model=ai_config.model_name,
                    max_tokens=200,
                    temperature=0.7
                )

                if not hint_response:
                    hint_response = "힌트를 생성하는 중 오류가 발생했습니다."

        except Exception as e:
            print(f'vLLM Error: {str(e)}')
            hint_response = "힌트 생성에 실패했습니다. 문제를 단계별로 나누어 생각해보세요."

    # ... 기존 API, local 모드 코드 ...
```

### 5. Frontend 모델 선택 UI 업데이트

**파일: `frontend/src/pages/AdminPanel/tabs/ModelsTab/index.jsx`**

```jsx
{/* 모드 선택에 vLLM 추가 */}
<label className={`mode-option ${aiMode === 'vllm' ? 'selected' : ''}`}>
  <input
    type="radio"
    name="aiMode"
    value="vllm"
    checked={aiMode === 'vllm'}
    onChange={(e) => setAiMode(e.target.value)}
  />
  <div className="mode-content">
    <div className="mode-title">⚡ vLLM 서버 방식</div>
    <div className="mode-description">
      • 고성능 추론 엔진 (24배 빠른 처리)
      <br/>• PagedAttention으로 메모리 효율 극대화
      <br/>• OpenAI API 호환
      <br/>• 별도 vLLM 서버 필요
    </div>
  </div>
</label>

{/* 모델 선택 드롭다운 */}
<select value={modelName} onChange={(e) => setModelName(e.target.value)}>
  <option value="Qwen/Qwen2.5-Coder-32B-Instruct">Qwen 2.5 Coder 32B</option>
  <option value="Qwen/Qwen2.5-Coder-7B-Instruct">Qwen 2.5 Coder 7B</option>
  <option value="ModelCloud/Brumby-14B-Base-GPTQMODEL-W4A16-v2">
    Brumby 14B (Quantized)
  </option>
</select>
```

---

## 🔧 설치 및 실행

### 1. vLLM 서버 시작

```bash
# GPU가 있는 경우
docker-compose -f docker-compose.yml -f docker-compose.vllm.yml up -d

# 또는 직접 설치
pip install vllm

# vLLM 서버 실행
vllm serve ModelCloud/Brumby-14B-Base-GPTQMODEL-W4A16-v2 \
    --host 0.0.0.0 \
    --port 8001 \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.9
```

### 2. 서버 상태 확인

```bash
# 모델 목록 확인
curl http://localhost:8001/v1/models

# 테스트 요청
curl http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ModelCloud/Brumby-14B-Base-GPTQMODEL-W4A16-v2",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

### 3. Django 설정 업데이트

```bash
# 마이그레이션
python manage.py makemigrations
python manage.py migrate

# 서버 재시작
docker-compose restart backend
```

---

## 💡 모델 특징 비교

### Qwen 2.5 Coder 32B
- **크기**: 32.76 GB
- **특징**: 가장 강력한 코딩 능력
- **단점**: 메모리 요구량 높음, 무료 API 미지원
- **용도**: 복잡한 알고리즘, 최고 품질 힌트

### Qwen 2.5 Coder 7B
- **크기**: 7.6 GB
- **특징**: 균형잡힌 성능/속도
- **추천**: vLLM으로 서빙 시 최적
- **용도**: 일반적인 코딩 힌트

### Brumby 14B (Quantized)
- **크기**: 14.77 GB (양자화)
- **특징**:
  - GPTQ 4bit 양자화 (메모리 절약)
  - 베이스 모델 (Instruction 튜닝 필요 가능)
  - 중간 크기
- **용도**: 리소스 제한 환경

---

## ⚙️ 추천 설정

### 개발/테스트 환경
```yaml
모드: vLLM
모델: Qwen/Qwen2.5-Coder-7B-Instruct
GPU: RTX 3090 (24GB) 이상
```

### 프로덕션 환경
```yaml
모드: vLLM
모델: Qwen/Qwen2.5-Coder-7B-Instruct
GPU: A100 (40GB) 권장
스케일링: 다중 GPU + Tensor Parallelism
```

### 리소스 제한 환경
```yaml
모드: API
모델: 작은 모델 또는 Fallback
대안: Hugging Face Serverless API (유료)
```

---

## 🎯 vLLM 사용 장점

1. ✅ **24배 빠른 처리** - 동시 사용자 처리 능력 극대화
2. ✅ **메모리 효율** - PagedAttention으로 더 많은 요청 처리
3. ✅ **OpenAI API 호환** - 기존 코드 재사용 가능
4. ✅ **쉬운 배포** - Docker 컨테이너로 간단 설치
5. ✅ **실시간 응답** - Continuous Batching으로 지연 최소화

## 🚨 주의사항

1. **GPU 필수**: vLLM은 GPU 필요 (CUDA 지원)
2. **메모리 요구량**: 모델 크기 + 여유 메모리 필요
3. **첫 실행 시간**: 모델 다운로드 및 로딩에 시간 소요
4. **양자화 모델**: Brumby는 GPTQ 양자화로 정확도 약간 하락 가능

---

## 📚 참고 자료

- [vLLM 공식 문서](https://docs.vllm.ai)
- [vLLM GitHub](https://github.com/vllm-project/vllm)
- [PagedAttention 논문](https://arxiv.org/abs/2309.06180)
- [Brumby 모델 카드](https://huggingface.co/ModelCloud/Brumby-14B-Base-GPTQMODEL-W4A16-v2)
