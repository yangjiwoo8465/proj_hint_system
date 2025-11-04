# Docker 설치 및 실행 가이드

## Docker 설치

### Ubuntu/Debian

```bash
# 기존 Docker 제거 (있을 경우)
sudo apt-get remove docker docker-engine docker.io containerd runc

# 필수 패키지 설치
sudo apt-get update
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Docker GPG 키 추가
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Docker 저장소 추가
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Docker 설치
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Docker 서비스 시작
sudo systemctl start docker
sudo systemctl enable docker

# 현재 사용자를 docker 그룹에 추가 (sudo 없이 사용하기 위해)
sudo usermod -aG docker $USER

# 재로그인 또는 다음 명령어 실행
newgrp docker

# Docker 설치 확인
docker --version
docker compose version
```

### 빠른 설치 스크립트

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

---

## 프로젝트 실행

### 1. 환경 확인

```bash
# Docker 확인
docker --version
docker compose version

# 프로젝트 디렉토리로 이동
cd /workspace/proj_hint_system
```

### 2. 전체 서비스 시작

```bash
# 빌드 및 시작
docker compose up -d --build

# 로그 확인
docker compose logs -f
```

### 3. 초기 설정 (최초 1회)

```bash
# 마이그레이션
docker compose exec backend python manage.py migrate

# 슈퍼유저 생성
docker compose exec backend python manage.py createsuperuser

# Static 파일 수집
docker compose exec backend python manage.py collectstatic --noinput
```

### 4. 접속

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000/api/v1
- **Django Admin**: http://localhost:8000/admin

---

## 주요 명령어

### 서비스 관리

```bash
# 시작
docker compose up -d

# 중지
docker compose down

# 재시작
docker compose restart

# 전체 재빌드
docker compose up -d --build --force-recreate

# 특정 서비스만 재시작
docker compose restart backend
docker compose restart frontend
```

### 로그 확인

```bash
# 전체 로그
docker compose logs -f

# 특정 서비스 로그
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db
```

### 컨테이너 접속

```bash
# 백엔드 컨테이너 접속
docker compose exec backend bash

# 프론트엔드 컨테이너 접속
docker compose exec frontend sh

# MySQL 접속
docker compose exec db mysql -u hint_user -p
# 비밀번호: hint_password_2024
```

### Django 관리 명령어

```bash
# 마이그레이션 생성
docker compose exec backend python manage.py makemigrations

# 마이그레이션 실행
docker compose exec backend python manage.py migrate

# 슈퍼유저 생성
docker compose exec backend python manage.py createsuperuser

# Django 셸
docker compose exec backend python manage.py shell
```

---

## 문제 해결

### 포트 충돌

```bash
# 사용 중인 포트 확인
sudo lsof -i :3000
sudo lsof -i :8000
sudo lsof -i :3306
sudo lsof -i :80

# 프로세스 종료
sudo kill -9 <PID>
```

### 컨테이너 초기화

```bash
# 모든 컨테이너 및 볼륨 삭제 (데이터 손실 주의!)
docker compose down -v

# 다시 시작
docker compose up -d --build
```

### 데이터베이스 초기화

```bash
# DB 컨테이너만 삭제
docker compose down
docker volume rm proj_hint_system_mysql_data

# 다시 시작
docker compose up -d
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

### 빌드 캐시 삭제

```bash
# Docker 캐시 전체 삭제
docker system prune -a

# 다시 빌드
docker compose up -d --build
```

---

## 개발 워크플로우

### 코드 수정 시

1. **백엔드 코드 수정**: 자동 reload (Gunicorn은 수동 재시작 필요)
   ```bash
   docker compose restart backend
   ```

2. **프론트엔드 코드 수정**: 자동 reload (Hot Module Replacement)

3. **의존성 추가**:
   ```bash
   # requirements.txt 수정 후
   docker compose up -d --build backend

   # package.json 수정 후
   docker compose up -d --build frontend
   ```

4. **모델 변경**:
   ```bash
   docker compose exec backend python manage.py makemigrations
   docker compose exec backend python manage.py migrate
   ```

---

## 서비스 구성

### docker-compose.yml 구조

```yaml
services:
  db:           # MySQL 8.0
  backend:      # Django + Gunicorn
  frontend:     # React + Vite
  nginx:        # Reverse Proxy
```

### 네트워크

- `hint_network`: 모든 서비스가 연결된 내부 네트워크

### 볼륨

- `mysql_data`: MySQL 데이터 영구 저장
- `static_volume`: Django static 파일
- `media_volume`: 업로드 파일

---

## 프로덕션 배포

### 환경 변수 수정

```bash
# .env 파일 수정
DEBUG=False
DJANGO_SECRET_KEY=<강력한-랜덤-키>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_PASSWORD=<강력한-비밀번호>
```

### HTTPS 설정

Nginx에 SSL 인증서 추가 (Let's Encrypt 권장)

```bash
# Certbot 사용
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## 다음 단계

1. ✅ Docker 설치
2. ✅ 서비스 시작: `docker compose up -d --build`
3. ✅ 초기 설정: 마이그레이션, 슈퍼유저
4. ⏳ 각 탭별 기능 구현
5. ⏳ 문제 데이터 로드
6. ⏳ 프로덕션 배포

---

## 참고 문서

- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 프로젝트 전체 요약
- [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) - 개발 가이드
- [NEW_PROJECT_README.md](NEW_PROJECT_README.md) - 프로젝트 README

---

**Docker로 깔끔하게 실행하세요!** 🐳
