# Docker 실행 문제 해결

## 현재 상황

Docker 데몬은 실행되었지만, MySQL 이미지 pull 시 오류 발생:
```
failed to register layer: unshare: operation not permitted
```

**원인:** 현재 컨테이너 환경에서 네임스페이스 생성 권한이 제한됨

---

## ✅ 해결 방법 1: 호스트 머신에서 직접 실행 (강력 권장)

### 이유
- 완전한 Docker 환경
- 모든 기능 정상 작동
- 성능 최적화
- 프로덕션 환경과 동일

### 방법

#### A. 현재 환경이 볼륨 마운트된 경우
```bash
# 로컬 터미널에서
cd /workspace/proj_hint_system  # 또는 실제 호스트 경로
docker compose up -d --build

# 초기 설정
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser

# 접속
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/api/v1
```

#### B. 프로젝트를 호스트로 복사해야 하는 경우
```bash
# 1. 호스트에 디렉토리 생성
mkdir -p ~/projects/hint_system

# 2. 프로젝트 복사 (컨테이너에서)
# 방법은 환경에 따라 다름 - scp, git, 직접 복사 등

# 3. 호스트에서 실행
cd ~/projects/hint_system
docker compose up -d --build
```

---

## ✅ 해결 방법 2: Privileged 컨테이너 사용

### 방법
현재 컨테이너를 특권(privileged) 모드로 재시작합니다.

### 컨테이너 실행 명령어에 추가
```bash
docker run --privileged \
  --security-opt seccomp=unconfined \
  --security-opt apparmor=unconfined \
  -v /workspace:/workspace \
  your-image
```

### Docker Compose로 실행하는 경우
```yaml
# docker-compose.yml (컨테이너 설정)
services:
  dev-environment:
    privileged: true
    security_opt:
      - seccomp=unconfined
      - apparmor=unconfined
```

**주의:** 보안 위험이 있으므로 개발 환경에서만 사용

---

## ✅ 해결 방법 3: 간단한 테스트 이미지 사용

MySQL 대신 더 가벼운 이미지로 테스트해봅니다.

### docker-compose-test.yml 생성
```yaml
version: '3.8'

services:
  # MySQL 대신 Alpine Linux로 테스트
  test:
    image: alpine:latest
    command: sleep infinity

  # 또는 Python만 테스트
  backend-test:
    image: python:3.11-slim
    command: python --version
```

### 실행
```bash
cd /workspace/proj_hint_system
docker compose -f docker-compose-test.yml up -d
docker compose -f docker-compose-test.yml ps
```

만약 성공하면 → Docker는 작동, MySQL 이미지만 문제
만약 실패하면 → 근본적인 권한 문제

---

## 🔍 현재 환경 진단

### Docker 데몬 상태
```bash
docker info
```
✅ 성공: Storage Driver: vfs, Server Version: 28.5.1

### 이미지 pull 테스트
```bash
# 가벼운 이미지 테스트
docker pull alpine:latest
docker run alpine:latest echo "Hello"
```

만약 alpine도 실패 → **방법 1 또는 2 필수**
만약 alpine 성공 → MySQL 특정 문제

---

## 📊 각 방법 비교

| 방법 | 장점 | 단점 | 추천도 |
|------|------|------|--------|
| **방법 1: 호스트 실행** | ✅ 완전한 기능<br>✅ 안정적<br>✅ 프로덕션과 동일 | ⚠️ 호스트 접근 필요 | ⭐⭐⭐⭐⭐ |
| **방법 2: Privileged** | ✅ 현재 환경 유지<br>✅ 모든 기능 가능 | ⚠️ 보안 위험<br>⚠️ 재시작 필요 | ⭐⭐⭐ |
| **방법 3: 테스트 이미지** | ✅ 빠른 검증 | ⚠️ 제한적 테스트만<br>⚠️ 실제 앱 실행 불가 | ⭐⭐ |

---

## 🎯 권장 순서

### 1단계: 간단한 테스트
```bash
# Alpine 이미지로 Docker 기능 확인
docker pull alpine:latest
docker run alpine:latest echo "Docker works!"
```

### 2단계: 환경 선택

**A. 호스트 접근 가능** → **방법 1 사용**
```bash
# 호스트 터미널에서
cd /workspace/proj_hint_system
docker compose up -d --build
```

**B. 현재 환경만 사용 가능** → **방법 2 시도**
- 컨테이너 관리자에게 privileged 모드 요청
- 또는 다른 개발 환경 고려

**C. 빠른 검증만 필요** → **방법 3**
- docker-compose-test.yml 사용

---

## 💡 최종 권장사항

**가장 좋은 방법: 호스트 머신에서 실행**

이유:
1. ✅ 완전한 Docker 기능
2. ✅ 안정적인 환경
3. ✅ 프로덕션 배포와 동일한 구조
4. ✅ 팀원들도 동일하게 실행 가능
5. ✅ CI/CD와 일관성

### 호스트에서 실행하는 방법

```bash
# 1. 로컬 머신 터미널 열기
# 2. 프로젝트 디렉토리로 이동
cd /workspace/proj_hint_system  # 실제 경로로 변경

# 3. Docker Compose 실행
docker compose up -d --build

# 4. 로그 확인
docker compose logs -f

# 5. 초기 설정
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser

# 6. 브라우저에서 접속
# - http://localhost:3000 (Frontend)
# - http://localhost:8000/api/v1 (Backend API)
# - http://localhost:8000/admin (Django Admin)
```

---

## ❓ 자주 묻는 질문

### Q1: 현재 컨테이너에서 절대 못 쓰나요?
A: Privileged 모드로 재시작하면 가능합니다. 하지만 권장하지 않습니다.

### Q2: 프로젝트 파일은 어떻게 공유하나요?
A:
- 볼륨 마운트되어 있으면 자동 공유
- Git으로 호스트에서 clone
- 파일 복사 (scp, rsync 등)

### Q3: 개발 중에는 어떻게 하나요?
A:
- 코드 수정: 현재 환경 또는 호스트 어디서든 가능
- 실행/테스트: 호스트에서 Docker Compose로

### Q4: 팀원들은 어떻게 하나요?
A: 모두 자신의 로컬 머신에서 Docker Compose로 실행하면 됩니다.

---

## 다음 단계

1. ✅ 호스트 머신 터미널 열기
2. ✅ Docker 설치 확인: `docker --version`
3. ✅ 프로젝트 디렉토리로 이동
4. ✅ `docker compose up -d --build` 실행
5. ✅ 초기 설정 진행
6. ✅ 개발 시작!

---

**결론: 호스트 머신에서 Docker Compose를 실행하세요!** 🚀
