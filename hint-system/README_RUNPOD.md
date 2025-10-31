# Runpod에서 힌트 시스템 실행하기

## 🚀 빠른 시작 (5분 완료)

```bash
# 1. 프로젝트 복사
git clone <your-repository> /workspace/5th-project_mvp

# 2. 실행 스크립트 권한 부여
chmod +x /workspace/5th-project_mvp/hint-system/run_runpod.sh

# 3. 실행
cd /workspace/5th-project_mvp/hint-system
./run_runpod.sh
```

**완료!** Gradio 공개 링크가 출력됩니다.

---

## 📋 목차

1. [Runpod Pod 생성](#1-runpod-pod-생성)
2. [프로젝트 설치](#2-프로젝트-설치)
3. [실행](#3-실행)
4. [VSCode Remote SSH 연결 (선택)](#4-vscode-remote-ssh-연결-선택)
5. [모델 정보](#5-모델-정보)
6. [트러블슈팅](#6-트러블슈팅)

---

## 1. Runpod Pod 생성

### 1-1. Runpod 로그인
- https://www.runpod.io 접속
- 로그인 (계정 없으면 생성)

### 1-2. Pod 생성
1. **Pods** 탭 클릭
2. **+ Deploy** 클릭
3. GPU 선택:
   ```
   추천: H100 PCIe (80GB VRAM)
   비용: $2.39/hr
   이유: 14B~32B 모델 동시 실행 가능
   ```

4. Template 선택:
   ```
   RunPod PyTorch (권장)
   또는
   RunPod Tensorflow
   ```

5. 설정:
   ```
   Container Disk: 50GB
   Volume: 필요 없음 (체크 해제)
   ```

6. **Deploy On-Demand** 클릭

### 1-3. Pod 시작 대기
- Pod 상태가 `Running`이 될 때까지 1~2분 대기
- `Connect` 버튼이 활성화되면 완료

---

## 2. 프로젝트 설치

### 2-1. Jupyter Notebook 또는 Terminal 열기

**방법 1: Jupyter Notebook (추천)**
1. Pod 카드에서 **Connect** → **Start Jupyter Notebook** 클릭
2. Jupyter가 열리면 **Terminal** 클릭

**방법 2: SSH**
1. Pod 카드에서 **Connect** → **SSH** 탭
2. SSH 명령어 복사해서 로컬 터미널에서 실행

### 2-2. 프로젝트 복사

```bash
# Git 설치 확인
git --version

# 프로젝트 클론
cd /workspace
git clone https://github.com/your-username/5th-project_mvp.git

# 또는 로컬에서 업로드 (scp 사용)
# scp -r 5th-project_mvp root@ssh.runpod.io:/workspace/
```

### 2-3. 패키지 설치

```bash
cd /workspace/5th-project_mvp/hint-system

# Python 패키지 설치 (2~3분 소요)
pip install -r requirements.txt
```

---

## 3. 실행

### 방법 1: 실행 스크립트 사용 (추천)

```bash
# 실행 권한 부여
chmod +x run_runpod.sh

# 실행
./run_runpod.sh
```

### 방법 2: 직접 실행

```bash
python3 app.py
```

### 3-1. 공개 링크 복사

실행되면 다음과 같은 메시지가 출력됩니다:

```
[RUNPOD] Runpod 환경 감지 - 공개 링크 생성 중...

* Running on local URL:  http://0.0.0.0:7860
* Running on public URL: https://abcd1234.gradio.live

This share link expires in 72 hours.
```

**`https://abcd1234.gradio.live` 링크를 복사**해서 브라우저에서 접속하세요!

---

## 4. VSCode Remote SSH 연결 (선택)

Claude Code Extension을 Runpod에서 사용하려면 VSCode Remote SSH로 연결하세요.

### 4-1. SSH 정보 확인

1. Runpod Pod 카드 → **Connect** → **TCP Port Mappings**
2. SSH 포트 확인:
   ```
   SSH: 22 -> 12345 (예시)
   ```

3. SSH 명령어 복사:
   ```bash
   ssh root@ssh.runpod.io -p 12345
   ```

### 4-2. VSCode 연결

1. VSCode에서 **Remote-SSH** Extension 설치
2. `Ctrl+Shift+P` → `Remote-SSH: Add New SSH Host`
3. SSH 명령어 입력: `ssh root@ssh.runpod.io -p 12345`
4. `Ctrl+Shift+P` → `Remote-SSH: Connect to Host`
5. `ssh.runpod.io` 선택

### 4-3. Claude Code 사용

- VSCode가 Runpod에 연결되면 **Claude Code Extension 자동 작동**
- 로컬과 동일하게 사용 가능!

---

## 5. 모델 정보

### 탑재된 모델 (80GB VRAM 기준)

| 모델 | 크기 | VRAM 사용량 | 성능 | 추천도 |
|------|------|-------------|------|--------|
| **Qwen2.5-14B-Instruct** | 14B | ~28GB | 최고 | ⭐⭐⭐⭐⭐ |
| Qwen2.5-7B-Instruct | 7B | ~14GB | 우수 | ⭐⭐⭐⭐ |
| Llama-3.1-8B-Instruct | 8B | ~16GB | 우수 | ⭐⭐⭐⭐ |
| Qwen2.5-32B-Instruct (4-bit) | 32B (4-bit) | ~20GB | 최상 | ⭐⭐⭐⭐⭐ |
| Qwen2.5-3B-Instruct | 3B | ~6GB | 보통 | ⭐⭐⭐ |

### 추천 사용 순서

1. **Qwen2.5-14B-Instruct** - 균형잡힌 성능/속도
2. **Qwen2.5-32B-Instruct (4-bit)** - 최고 성능 (양자화로 빠름)
3. Llama-3.1-8B-Instruct - 비교용

---

## 6. 트러블슈팅

### 문제: "CUDA out of memory"

**원인:** 모델이 너무 커서 VRAM 부족

**해결:**
1. 더 작은 모델 사용 (14B → 7B)
2. 4-bit 양자화 모델 사용 (32B 4-bit)
3. Pod GPU 업그레이드 (40GB → 80GB)

---

### 문제: "ModuleNotFoundError: No module named 'torch'"

**원인:** 패키지 미설치

**해결:**
```bash
pip install -r requirements.txt
```

---

### 문제: "Port 7860 already in use"

**원인:** 이미 앱이 실행 중

**해결:**
```bash
# 실행 중인 프로세스 찾기
ps aux | grep app.py

# 프로세스 종료 (PID는 위에서 확인)
kill -9 <PID>

# 다시 실행
./run_runpod.sh
```

---

### 문제: "Gradio 공개 링크가 생성되지 않음"

**원인:** Runpod 환경 감지 실패

**해결:**
```bash
# 환경 변수 수동 설정
export RUNPOD_POD_ID="manual"

# 다시 실행
python3 app.py
```

---

### 문제: "모델 로딩이 너무 느림 (10분+)"

**원인:** 첫 실행 시 모델 다운로드 중

**해결:**
- 첫 실행 시 정상 (모델 다운로드: 5~10분)
- 이후 실행은 빠름 (캐시 사용: 1~2분)
- Hugging Face 토큰 설정으로 속도 향상 가능:
  ```bash
  huggingface-cli login
  ```

---

## 7. 비용 정보

### Pod 비용

| GPU | VRAM | 시간당 비용 | 하루 (24시간) | 권장 사용 |
|-----|------|-------------|--------------|-----------|
| H100 PCIe | 80GB | $2.39 | $57.36 | 14B~32B 모델 |
| A100 80GB | 80GB | $1.89 | $45.36 | 14B~32B 모델 |
| RTX 4090 | 24GB | $0.34 | $8.16 | 7B 모델 |

### 비용 절약 팁

1. **사용 후 즉시 종료** - Pod 카드에서 `Stop` 클릭
2. **Spot 인스턴스 사용** - On-Demand 대신 Spot (50% 저렴, 중단 가능성)
3. **필요한 GPU만 선택** - 7B 모델이면 RTX 4090으로 충분

---

## 8. 다음 단계

### ✅ 완료 체크리스트

- [ ] Runpod Pod 생성
- [ ] 프로젝트 복사
- [ ] 패키지 설치
- [ ] 앱 실행
- [ ] 공개 링크 접속
- [ ] 힌트 생성 테스트
- [ ] (선택) VSCode Remote SSH 연결

### 🎯 힌트 생성 테스트

1. 공개 링크 접속
2. 문제 선택 (예: #1000)
3. 사용자 코드 입력
4. **Qwen2.5-14B-Instruct** 선택
5. 힌트 요청
6. 결과 확인:
   ```
   Q: "같은 코드 10번 복사하면 나중에 10군데 다 고쳐?"
   ```

---

## 9. 지원

문제 발생 시:
1. 이 README 트러블슈팅 섹션 확인
2. GitHub Issues 등록
3. Runpod 공식 문서: https://docs.runpod.io

---

**Happy Hinting! 🎯**
