# Runpod 연동 가이드

## Runpod이란?

Runpod는 GPU 클라우드 서비스로, 로컬 PC에서 돌리기 어려운 무거운 모델(7B, 14B 등)을 원격으로 실행할 수 있게 해줍니다.

## 왜 Runpod를 사용하나요?

### 로컬 모델의 한계
- **Qwen2.5-3B-Instruct** (3B) - 로컬에서 가능하지만 성능 제한적
- **Qwen2.5-7B-Instruct** (7B) - 로컬에서 느리거나 불가능
- **Qwen2.5-14B-Instruct** (14B) - 로컬에서 불가능 (VRAM 부족)

### Runpod 사용 시
- ✅ 무거운 모델(7B~14B) 빠르게 실행
- ✅ GPU 비용 효율적 (사용한 만큼만 과금)
- ✅ 로컬 PC 부담 없음

---

## 1. Runpod 계정 생성 및 설정

### 1-1. Runpod 회원가입
1. https://www.runpod.io 접속
2. Sign Up 클릭
3. 이메일/비밀번호 설정 또는 Google 로그인

### 1-2. 크레딧 충전
1. 대시보드 → Billing
2. 최소 $10 충전 (약 13,000원)
3. 사용량 기준: GPU 시간당 $0.3~$0.5 (약 400~650원)

---

## 2. Runpod Serverless Endpoint 생성

### 2-1. Serverless 선택
1. Runpod 대시보드 → **Serverless** 탭 클릭
2. **+ New Endpoint** 클릭

### 2-2. 모델 선택
**추천 템플릿:** `vLLM`

```
Template: vLLM (Hugging Face)
Model: Qwen/Qwen2.5-7B-Instruct
GPU: RTX 4090 또는 A5000
```

### 2-3. 설정
```
Max Workers: 1 (비용 절약)
Idle Timeout: 5 minutes
GPU Memory: 24GB
```

### 2-4. Endpoint 생성
- **Create Endpoint** 클릭
- 생성 완료까지 1~2분 대기

---

## 3. API 키 및 엔드포인트 URL 복사

### 3-1. API 키 발급
1. Runpod 대시보드 → **Settings** → **API Keys**
2. **Create API Key** 클릭
3. 이름 입력 (예: `hint-system`)
4. **생성된 API 키 복사** (예: `ABCDEF1234567890...`)

### 3-2. Endpoint URL 복사
1. Serverless 탭 → 생성한 Endpoint 클릭
2. **Endpoint URL 복사**

예시:
```
https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync
```

---

## 4. 프로젝트에 Runpod 설정

### 4-1. .env 파일 수정

프로젝트 루트에 `.env` 파일이 없으면 생성:
```bash
cp .env.example .env
```

`.env` 파일 열어서 아래 내용 수정:

```bash
# Runpod 사용 활성화
USE_RUNPOD=true

# Runpod API 엔드포인트 (위에서 복사한 URL)
RUNPOD_API_ENDPOINT=https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync

# Runpod API 키 (위에서 복사한 키)
RUNPOD_API_KEY=ABCDEF1234567890...
```

**⚠️ 주의:**
- `YOUR_ENDPOINT_ID`는 실제 Endpoint ID로 교체
- `ABCDEF1234567890...`는 실제 API 키로 교체

---

## 5. 사용 방법

### 5-1. 앱 실행
```bash
python hint-system/app.py
```

### 5-2. 모델 선택
- `USE_RUNPOD=true`로 설정하면 자동으로 Runpod 모델이 추가됩니다:
  - Qwen2.5-7B-Instruct (Runpod)
  - Qwen2.5-14B-Instruct (Runpod)
  - Llama-3.1-8B-Instruct (Runpod)

### 5-3. 힌트 생성
1. UI에서 Runpod 모델 선택 (예: `Qwen2.5-7B-Instruct`)
2. 문제 선택 및 사용자 코드 입력
3. 힌트 요청
4. **Runpod 서버에서 실행되어 결과 반환** (30초~1분)

---

## 6. VSCode + Runpod SSH 연결 (선택사항)

### Claude Code 계속 사용 가능?
**네, 가능합니다!**

VSCode를 Runpod Pod에 SSH로 연결하면:
- ✅ Claude Code Extension 그대로 작동
- ✅ Runpod GPU로 무거운 모델 실행
- ✅ 로컬 파일 편집 가능

### SSH 연결 방법

#### 6-1. Runpod Pod 생성 (Serverless 대신 Pod 사용)
1. Runpod 대시보드 → **Pods** 탭
2. **+ Deploy** 클릭
3. GPU 선택 (RTX 4090 추천)
4. Template: **RunPod Pytorch** 선택
5. **Deploy On-Demand** 클릭

#### 6-2. SSH 설정
1. Pod 생성 완료 후 **Connect** 클릭
2. **TCP Port Mappings** 확인:
   ```
   SSH: 22 -> XXXXX (외부 포트)
   ```
3. SSH 명령어 복사:
   ```bash
   ssh root@ssh.runpod.io -p XXXXX
   ```

#### 6-3. VSCode Remote SSH 연결
1. VSCode에서 **Remote-SSH** Extension 설치
2. `Ctrl+Shift+P` → "Remote-SSH: Add New SSH Host"
3. 위에서 복사한 SSH 명령어 입력
4. 연결!

#### 6-4. Claude Code 사용
- VSCode가 Runpod에 연결되면 **Claude Code Extension 자동 작동**
- 로컬과 동일하게 사용 가능

---

## 7. 비용 관리

### Serverless 비용 (추천)
```
GPU 실행 시간: $0.0002/초 (약 0.26원/초)
힌트 1개 생성 (30초): 약 $0.006 (약 8원)
```

### Pod 비용
```
RTX 4090: $0.34/시간 (약 450원/시간)
1시간 사용: 약 450원
```

### 비용 절약 팁
1. **Serverless 사용** (사용할 때만 과금)
2. **Idle Timeout 5분** 설정 (미사용 시 자동 종료)
3. **필요할 때만 켜기**

---

## 8. 트러블슈팅

### 문제: "Runpod API 에러: 401"
**원인:** API 키가 잘못되었거나 만료됨

**해결:**
1. Runpod 대시보드 → Settings → API Keys 확인
2. `.env` 파일의 `RUNPOD_API_KEY` 재확인

---

### 문제: "Runpod API 타임아웃 (60초 초과)"
**원인:** Endpoint가 Cold Start 중이거나 모델 로딩 중

**해결:**
1. 첫 실행 시 2~3분 대기 (모델 로딩)
2. 이후 요청은 30초 내로 완료

---

### 문제: "Job 큐에 등록됨, 대기 중"
**원인:** 비동기 Endpoint 사용 중 (/run 대신 /runsync 사용 필요)

**해결:**
`.env` 파일의 `RUNPOD_API_ENDPOINT` 확인:
```bash
# ❌ 잘못된 URL
https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/run

# ✅ 올바른 URL
https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync
```

---

## 9. 요약

### 로컬 모델 (현재)
- Qwen2.5-3B-Instruct (3B) - 작동하지만 성능 제한적
- 비용: 무료
- 속도: 30초~1분

### Runpod 원격 모델 (추가)
- Qwen2.5-7B-Instruct (7B) - **2배 더 큰 모델, 성능 향상**
- Qwen2.5-14B-Instruct (14B) - **4배 더 큰 모델, 최고 성능**
- 비용: 힌트 1개당 약 8원 (Serverless)
- 속도: 30초~1분

### VSCode + Runpod SSH
- Claude Code 그대로 사용 가능
- GPU 서버에서 직접 작업
- 비용: 시간당 약 450원 (RTX 4090)

---

## 10. 다음 단계

1. ✅ `.env` 파일에 Runpod 설정 추가
2. ✅ `USE_RUNPOD=true` 설정
3. ✅ 앱 실행 후 Runpod 모델 선택
4. ✅ 힌트 생성 테스트
5. (선택) VSCode를 Runpod SSH 연결

**성공하면:** V16 프롬프트 + 7B/14B 모델로 고품질 소크라테스 힌트 생성 가능!
