# Docker 실행 가이드

## ⚠️ 중요 안내

현재 환경은 **컨테이너 내부**로, Docker-in-Docker 실행에 필요한 권한이 없습니다.

## ✅ 프로젝트는 준비 완료

- Django 백엔드 (5개 모듈화된 앱)
- React 프론트엔드 (탭별 페이지)
- Docker Compose 설정
- Nginx 프록시
- MySQL 데이터베이스 설정

## 🚀 실행 방법

### 호스트 머신에서 실행하세요

```bash
cd /workspace/proj_hint_system
docker compose up -d --build
```

### 초기 설정

```bash
# 마이그레이션
docker compose exec backend python manage.py migrate

# 슈퍼유저 생성
docker compose exec backend python manage.py createsuperuser

# Static 파일 수집
docker compose exec backend python manage.py collectstatic --noinput
```

### 접속

- 프론트엔드: http://localhost:3000
- 백엔드 API: http://localhost:8000/api/v1
- Django Admin: http://localhost:8000/admin

## 📖 상세 가이드

- **DOCKER_SETUP.md** - Docker 완전 가이드
- **PROJECT_SUMMARY.md** - 프로젝트 전체 요약
- **DEVELOPMENT_GUIDE.md** - 팀 협업 가이드

