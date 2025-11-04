# Docker 실행 방법 (현재 환경 기준)

## 현재 상황

현재 컨테이너 내부 환경에서는 Docker-in-Docker 실행 시 권한 문제가 발생합니다:
- ❌ iptables 권한 없음
- ❌ 네트워크 브리지 생성 권한 없음
- ❌ Docker 데몬 네트워크 초기화 실패

---

## ✅ 해결 방법 1: 로컬 머신에서 실행 (권장)

### 방법
이 프로젝트를 로컬 머신(호스트)으로 복사해서 실행합니다.

### 단계
```bash
# 1. 로컬 머신에서 프로젝트 복사
# (이 컨테이너가 호스트와 볼륨이 마운트되어 있다면 이미 공유됨)
cd /workspace/proj_hint_system

# 2. Docker 확인
docker --version
docker compose version

# 3. 서비스 실행
docker compose up -d --build

# 4. 초기 설정
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser

# 5. 접속
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000/api/v1
```

**장점:**
- ✅ 정상적인 Docker 환경
- ✅ 모든 기능 사용 가능
- ✅ 성능 최적

---

## ✅ 해결 방법 2: Docker-in-Docker with Privileged Mode

### 방법
현재 컨테이너를 privileged 모드로 재시작합니다.

### 필요한 옵션
```bash
docker run --privileged \
  -v /workspace:/workspace \
  -v /var/run/docker.sock:/var/run/docker.sock \
  your-container-image
```

또는 docker-compose.yml에:
```yaml
services:
  dev:
    privileged: true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

**주의:** 이 방법은 보안 위험이 있으므로 개발 환경에서만 사용하세요.

---

## ✅ 해결 방법 3: 호스트의 Docker 소켓 사용

### 방법
호스트의 Docker 데몬을 직접 사용합니다.

### 단계
```bash
# 1. 호스트의 Docker 소켓을 마운트 (컨테이너 실행 시)
docker run -v /var/run/docker.sock:/var/run/docker.sock ...

# 2. 컨테이너 내부에서 호스트의 Docker 사용
docker ps  # 호스트의 컨테이너 목록이 보임
cd /workspace/proj_hint_system
docker compose up -d --build
```

**장점:**
- ✅ Privileged 모드 불필요
- ✅ 호스트의 Docker를 직접 사용
- ✅ 간단한 설정

**단점:**
- ⚠️ 컨테이너가 호스트의 Docker에 접근 가능 (보안 고려 필요)

---

## 🔍 현재 환경 확인

### Docker 설치 여부
```bash
docker --version
# Docker version 28.5.1, build e180ab8 ✅ 설치됨
```

### Docker Compose 설치 여부
```bash
docker compose version
# Docker Compose version v2.40.3 ✅ 설치됨
```

### Docker 소켓 확인
```bash
ls -la /var/run/docker.sock
```

만약 존재한다면 → **방법 3 사용 가능**
만약 없다면 → **방법 1 또는 2 필요**

---

## 🚀 빠른 테스트

### 현재 Docker 접근 가능한지 확인
```bash
docker ps
```

**성공하면:**
```
CONTAINER ID   IMAGE     COMMAND   ...
```
→ 이미 호스트 Docker에 연결되어 있음! 바로 사용 가능

**실패하면:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```
→ 위의 방법 1, 2, 3 중 하나 선택

---

## 📝 권장 방법

### 개발 중이라면
- **방법 1 (로컬 실행)** - 가장 안전하고 일반적

### CI/CD 환경이라면
- **방법 3 (Docker 소켓 마운트)** - 효율적

### 특수한 경우
- **방법 2 (Privileged)** - 마지막 수단

---

## ❓ 어떤 방법을 선택해야 할까요?

다음 명령어로 확인해보세요:
```bash
ls -la /var/run/docker.sock
```

### 결과에 따른 선택:

**1. 파일이 존재하고 접근 가능하면:**
```bash
cd /workspace/proj_hint_system
docker compose up -d --build
```
→ 바로 실행하세요!

**2. Permission denied 에러가 나면:**
```bash
chmod 666 /var/run/docker.sock  # 임시 권한 부여
# 또는
docker compose up -d --build
```

**3. 파일이 없으면:**
→ **방법 1 (로컬 머신에서 실행)** 사용

---

## 다음 단계

1. 위 방법 중 하나를 선택해서 Docker를 실행 가능한 상태로 만듭니다
2. `docker compose up -d --build` 실행
3. 초기 설정 진행
4. 개발 시작!
