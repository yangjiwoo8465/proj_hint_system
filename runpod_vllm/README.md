# Runpod vLLM Server Setup

Runpod Workspace에서 Qwen 2.5 Coder 32B 모델을 vLLM으로 실행하기 위한 가이드입니다.

## 1. Runpod Pod 생성

1. [Runpod](https://www.runpod.io/)에 로그인
2. **GPU Pods** 선택
3. **Deploy** 클릭
4. GPU 선택 (권장: RTX 4090 또는 A6000 이상)
5. **Pytorch 2.1** 템플릿 선택
6. Pod 시작

## 2. 환경 설정

Runpod Workspace 터미널에서 다음 명령어 실행:

```bash
# vLLM 설치
pip install vllm transformers accelerate

# 또는 requirements.txt 사용
pip install -r requirements.txt
```

## 3. vLLM 서버 실행

### 방법 1: 스크립트 사용 (권장)

```bash
chmod +x start_vllm.sh
./start_vllm.sh
```

### 방법 2: 직접 실행

```bash
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-Coder-32B-Instruct \
    --port 8000 \
    --max-model-len 8192 \
    --gpu-memory-utilization 0.95 \
    --tensor-parallel-size 1 \
    --dtype auto \
    --trust-remote-code
```

## 4. 엔드포인트 확인

vLLM 서버가 시작되면 다음과 같은 URL이 생성됩니다:

```
https://your-pod-id-8000.proxy.runpod.net
```

예시:
```
https://abc123def456-8000.proxy.runpod.net
```

## 5. 로컬 Django와 연결

1. **관리자 패널** 접속
2. **Models 탭** 선택
3. **AI 모드: Runpod** 선택
4. **Runpod Endpoint URL** 입력:
   ```
   https://your-pod-id-8000.proxy.runpod.net
   ```
5. **모델명** 입력:
   ```
   Qwen/Qwen2.5-Coder-32B-Instruct
   ```
6. **설정 저장** 클릭

## 6. 테스트

### API 테스트 (curl)

```bash
curl https://your-pod-id-8000.proxy.runpod.net/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "messages": [
      {"role": "user", "content": "Python으로 피보나치 수열을 구현하는 방법을 알려줘"}
    ],
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

### Python 테스트

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://your-pod-id-8000.proxy.runpod.net/v1",
    api_key="EMPTY"  # vLLM은 API 키 불필요
)

response = client.chat.completions.create(
    model="Qwen/Qwen2.5-Coder-32B-Instruct",
    messages=[
        {"role": "user", "content": "Python으로 피보나치 수열을 구현하는 방법을 알려줘"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

## 7. 주의사항

- **GPU 메모리**: Qwen 2.5 Coder 32B는 약 24GB VRAM 필요
- **모델 다운로드**: 첫 실행 시 모델 다운로드에 시간이 걸림 (약 10-20분)
- **콜드 스타트**: Runpod Serverless가 아닌 Pod 사용 시 콜드 스타트 없음
- **URL 변경**: Pod 재시작 시 URL이 변경될 수 있음
- **비용**: 사용 시간에 따라 과금됨

## 8. 문제 해결

### vLLM 서버가 시작되지 않음
- GPU 메모리 부족: `--gpu-memory-utilization` 값을 0.9로 낮춤
- CUDA 버전 확인: `nvidia-smi`로 CUDA 버전 확인

### 로컬에서 연결 안됨
- Runpod URL 확인: Runpod 대시보드에서 URL 복사
- 포트 확인: 8000 포트가 열려있는지 확인
- 방화벽: Runpod Proxy가 활성화되어 있는지 확인

## 9. 모델 정보

- **모델명**: Qwen/Qwen2.5-Coder-32B-Instruct
- **파라미터**: 32B
- **특화**: 코드 생성, 디버깅, 알고리즘 설명
- **컨텍스트 길이**: 최대 32K 토큰 (설정: 8192)
- **제작사**: Alibaba Cloud

## 10. 성능 최적화

### GPU 메모리 최적화
```bash
--gpu-memory-utilization 0.95  # GPU 메모리 95% 사용
--max-model-len 8192            # 컨텍스트 길이 제한
```

### 병렬 처리 (Multi-GPU)
```bash
--tensor-parallel-size 2  # 2개 GPU 사용
```

### 배치 처리
```bash
--max-num-seqs 256  # 동시 처리 가능한 시퀀스 수
```
