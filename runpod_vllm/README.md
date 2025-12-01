# Runpod vLLM 설정 가이드

이 문서는 Runpod에서 vLLM을 이용하여 Qwen 2.5 Coder 32B 모델을 배포하고, 프로젝트와 연동하는 방법을 상세히 설명합니다.

## 목차
1. [사전 요구사항](#사전-요구사항)
2. [Runpod Pod 생성](#runpod-pod-생성)
3. [vLLM 서버 설치 및 실행](#vllm-서버-설치-및-실행)
4. [연결 테스트](#연결-테스트)
5. [프로젝트 연동](#프로젝트-연동)
6. [문제 해결](#문제-해결)

---

## 사전 요구사항

### 1. Runpod 계정
- [Runpod](https://www.runpod.io/) 계정 생성 및 로그인
- GPU 크레딧 충전 (A100 80GB GPU 권장)

### 2. 필요한 GPU 사양
- **최소 요구사항**: A100 80GB GPU
- **이유**: Qwen 2.5 Coder 32B 모델은 약 60-70GB VRAM 필요
- **추천 GPU**: A100 80GB, H100 80GB

---

## Runpod Pod 생성

### 1단계: Template 선택

1. Runpod 대시보드에서 **"Deploy"** 클릭
2. **GPU Type** 선택: `A100 80GB` 이상
3. **Template** 선택: `madiator2011/better-pytorch:cuda12.4-torch2.6.0`
   - PyTorch와 CUDA가 사전 설치된 이미지
   - Python 3.10+ 포함

### 2단계: Pod 설정

```
Container Disk: 50GB 이상 (모델 다운로드 공간)
Volume Disk: 선택사항 (데이터 영속성 필요시)
Expose HTTP Ports: 8000 (vLLM 서버 포트)
Expose TCP Ports: 22 (SSH 접속용)
```

### 3단계: Pod 시작

- **Deploy** 버튼 클릭
- Pod가 `Running` 상태가 될 때까지 대기 (1-2분 소요)
- Pod URL 확인: `https://[pod-id]-8000.proxy.runpod.net`

---

## vLLM 서버 설치 및 실행

### 1단계: Pod에 SSH 접속

Runpod 대시보드에서 **"Connect"** > **"Start Web Terminal"** 클릭

또는 SSH 클라이언트 사용:
```bash
ssh root@[pod-ssh-address] -p [port]
```

### 2단계: 작업 디렉토리 생성

```bash
cd /workspace
mkdir -p vllm_server
cd vllm_server
```

### 3단계: 필요한 파일 생성

#### `requirements.txt` 생성
```bash
cat > requirements.txt << 'EOF'
vllm==0.6.4.post1
torch>=2.4.0
transformers>=4.45.0
accelerate>=0.34.0
EOF
```

#### `start_vllm.sh` 생성
```bash
cat > start_vllm.sh << 'EOF'
#!/bin/bash

echo "========================================="
echo "Starting vLLM Server with Qwen 2.5 Coder 32B"
echo "========================================="

export CUDA_VISIBLE_DEVICES=0
export MODEL_NAME="Qwen/Qwen2.5-Coder-32B-Instruct"
export PORT=8000
export MAX_MODEL_LEN=8192
export GPU_MEMORY_UTILIZATION=0.95

python -m vllm.entrypoints.openai.api_server \
    --model $MODEL_NAME \
    --port $PORT \
    --max-model-len $MAX_MODEL_LEN \
    --gpu-memory-utilization $GPU_MEMORY_UTILIZATION \
    --tensor-parallel-size 1 \
    --dtype auto \
    --trust-remote-code \
    --served-model-name "Qwen/Qwen2.5-Coder-32B-Instruct"

echo "vLLM server has stopped"
EOF
```

#### `test_connection.py` 생성
```bash
cat > test_connection.py << 'EOF'
"""
Runpod vLLM 서버 연결 테스트 스크립트
"""
from openai import OpenAI
import sys

def test_vllm_connection(endpoint_url):
    """vLLM 서버 연결 테스트"""

    print("=" * 50)
    print("Runpod vLLM Connection Test")
    print("=" * 50)
    print(f"Endpoint: {endpoint_url}")

    try:
        # OpenAI 클라이언트 생성
        client = OpenAI(
            base_url=f"{endpoint_url}/v1",
            api_key="EMPTY"  # vLLM은 API 키 불필요
        )

        print("\n테스트 요청 전송 중...")

        # 테스트 요청
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful coding assistant."
                },
                {
                    "role": "user",
                    "content": "Python으로 1부터 10까지의 합을 구하는 함수를 작성해줘."
                }
            ],
            temperature=0.7,
            max_tokens=500
        )

        print("\n✅ 연결 성공!")
        print("\n응답:")
        print("-" * 50)
        print(response.choices[0].message.content)
        print("-" * 50)

        print(f"\n사용 토큰:")
        print(f"  - Prompt: {response.usage.prompt_tokens}")
        print(f"  - Completion: {response.usage.completion_tokens}")
        print(f"  - Total: {response.usage.total_tokens}")

        return True

    except Exception as e:
        print(f"\n❌ 연결 실패!")
        print(f"에러: {str(e)}")
        print("\n문제 해결 방법:")
        print("1. Runpod vLLM 서버가 실행 중인지 확인")
        print("2. 엔드포인트 URL이 올바른지 확인")
        print("3. 네트워크 연결 확인")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python test_connection.py <endpoint_url>")
        print("예시: python test_connection.py https://abc123-8000.proxy.runpod.net")
        sys.exit(1)

    endpoint = sys.argv[1]

    # URL에서 /v1 제거 (자동으로 추가됨)
    if endpoint.endswith('/v1'):
        endpoint = endpoint[:-3]

    success = test_vllm_connection(endpoint)
    sys.exit(0 if success else 1)
EOF
```

### 4단계: 실행 권한 부여

```bash
chmod +x start_vllm.sh
```

### 5단계: vLLM 설치

```bash
pip install -r requirements.txt
```

설치 시간: 약 5-10분 소요

### 6단계: vLLM 서버 시작

#### 백그라운드 실행 (권장)
```bash
nohup ./start_vllm.sh > vllm_server.log 2>&1 &
```

#### 로그 확인
```bash
tail -f vllm_server.log
```

#### 실행 확인
다음 메시지가 나오면 성공:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**주의**: 모델 다운로드 및 로딩에 5-15분 소요

---

## 연결 테스트

### 1. Runpod 내부에서 테스트

```bash
# OpenAI 라이브러리 설치
pip install openai

# 테스트 실행
python test_connection.py http://localhost:8000
```

### 2. 외부에서 테스트

로컬 PC에서:

```bash
curl https://[pod-id]-8000.proxy.runpod.net/v1/models
```

성공 응답 예시:
```json
{
  "object": "list",
  "data": [
    {
      "id": "Qwen/Qwen2.5-Coder-32B-Instruct",
      "object": "model",
      "created": 1234567890,
      "owned_by": "vllm"
    }
  ]
}
```

---

## 프로젝트 연동

### 1단계: Endpoint URL 확인

Runpod Pod 페이지에서 확인:
```
https://[your-pod-id]-8000.proxy.runpod.net
```

### 2단계: 로컬 서버 실행

프로젝트 루트에서:

```bash
# Backend 실행
docker-compose up -d

# Frontend 실행
cd frontend
npm run dev
```

### 3단계: Admin Panel 설정

1. 브라우저에서 `http://localhost:3000` 접속
2. 관리자 계정으로 로그인
3. `http://localhost:3000/app/admin` 접속
4. **Models** 탭 선택
5. **AI 모델 방식** 섹션에서:
   - ☑ **Runpod vLLM 방식** 선택
   - **Runpod Endpoint URL**: `https://[your-pod-id]-8000.proxy.runpod.net` 입력
   - **Runpod API Key**: 비워두기 (vLLM은 인증 불필요)
   - **모델명**: `Qwen/Qwen2.5-Coder-32B-Instruct` (자동 입력됨)
6. **설정 저장** 버튼 클릭

### 4단계: 힌트 기능 테스트

1. 문제 페이지 접속
2. 코드 작성
3. 힌트 요청 버튼 클릭
4. Runpod vLLM에서 생성된 힌트 확인

---

## 문제 해결

### 1. GPU 메모리 부족 (OOM)

**증상**:
```
torch.cuda.OutOfMemoryError: CUDA out of memory
```

**해결 방법**:
- A100 80GB 이상 GPU 사용
- `GPU_MEMORY_UTILIZATION` 값 조정 (0.95 → 0.90)
- 더 작은 모델 사용 (예: Qwen2.5-Coder-7B)

### 2. 모델 다운로드 실패

**증상**:
```
Failed to download model from Hugging Face
```

**해결 방법**:
```bash
# Hugging Face 토큰 설정 (선택사항)
export HF_TOKEN="your_huggingface_token"

# 또는 수동 다운로드
huggingface-cli download Qwen/Qwen2.5-Coder-32B-Instruct
```

### 3. 포트 8000 접근 불가

**증상**:
- 외부에서 연결 안됨

**확인 사항**:
1. Runpod Pod 설정에서 Port 8000이 Expose되어 있는지 확인
2. vLLM 서버가 실행 중인지 확인:
   ```bash
   ps aux | grep vllm
   ```
3. 방화벽 설정 확인

### 4. 응답 속도가 느림

**원인**:
- 모델 크기 (32B 파라미터)
- 네트워크 지연

**해결 방법**:
- `MAX_MODEL_LEN` 값 줄이기 (8192 → 4096)
- `temperature` 값 조정
- 더 작은 모델 사용

### 5. Pod가 자동 종료됨

**원인**:
- Runpod 크레딧 부족
- Idle 타임아웃

**해결 방법**:
- 크레딧 충전
- Pod 설정에서 Auto-stop 비활성화

---

## 비용 최적화 팁

### 1. Pod 사용 시간 관리
- 사용하지 않을 때는 Pod 중지
- Spot Instance 활용 (비용 50-80% 절감)

### 2. 모델 선택
- 개발/테스트: Qwen2.5-Coder-7B (비용 절감)
- 프로덕션: Qwen2.5-Coder-32B (성능 최적)

### 3. 배치 처리
- 여러 요청을 모아서 처리
- `MAX_MODEL_LEN` 최적화

---

## 추가 리소스

- [vLLM 공식 문서](https://docs.vllm.ai/)
- [Runpod 문서](https://docs.runpod.io/)
- [Qwen2.5-Coder 모델 페이지](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct)

---

## 지원

문제가 발생하면:
1. 로그 파일 확인: `cat vllm_server.log`
2. Runpod 커뮤니티 포럼 검색
3. 프로젝트 Issue 등록
