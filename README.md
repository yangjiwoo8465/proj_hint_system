# 🎯 Hint System - AI 기반 코딩 테스트 학습 플랫폼

> Django + React 기반의 모듈식 힌트 제공 시스템

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)

---

## 📋 프로젝트 소개

코딩 테스트 학습을 위한 AI 기반 힌트 시스템입니다. 학습자의 성향을 분석하고, 적절한 수준의 힌트를 제공하여 효과적인 학습을 돕습니다.

### 주요 기능

- 🧩 **코딩 테스트**: Monaco Editor 기반 코드 작성 및 실행
- 💡 **AI 힌트 시스템**: 3단계 힌트 (대/중/소) 제공
- 🤖 **RAG 챗봇**: Python/Git 문서 기반 질의응답
- 📊 **성향 분석**: 완벽주의형 vs 반복형 학습자 분류
- 🏆 **레이팅 시스템**: 문제 난이도, 풀이 시간, 실행 횟수 기반 점수
- 🔐 **관리자 패널**: 모델 관리, 힌트 평가, 통계

---

## 🏗️ 프로젝트 구조

```
proj_hint_system/
├── backend/              # Django REST API
│   ├── apps/
│   │   ├── authentication/     # 인증 (JWT)
│   │   ├── coding_test/        # 코딩 테스트 + 힌트 시스템
│   │   ├── chatbot/            # RAG 챗봇
│   │   ├── mypage/             # 사용자 프로필
│   │   └── admin_panel/        # 관리자 기능
│   ├── common/           # 공통 유틸리티
│   └── vectordb/         # ChromaDB 연동
│
├── frontend/             # React + Vite
│   ├── src/
│   │   ├── pages/        # 5개 메인 페이지
│   │   ├── components/   # 공통 컴포넌트
│   │   ├── store/        # Redux Toolkit
│   │   └── services/     # API 호출
│   └── public/
│
├── nginx/                # Reverse Proxy
├── docker-compose.yml
└── .env
```

---

## 🚀 빠른 시작

### 사전 요구사항

- Docker 20.10+
- Docker Compose 2.0+

### 설치 및 실행

```bash
# 1. 저장소 클론
git clone https://github.com/yangjiwoo8465/proj_hint_system.git
cd proj_hint_system

# 2. 환경 변수 설정
cp .env.example .env
# .env 파일 수정 (필요시)

# 3. Docker Compose로 실행
docker compose up -d --build

# 4. 초기 설정
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py collectstatic --noinput

# 5. 접속
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000/api/v1
# - Admin Panel: http://localhost:8000/admin
```

### 개발 모드 실행

```bash
# 로그 확인
docker compose logs -f

# 특정 서비스만 재시작
docker compose restart backend
docker compose restart frontend

# 컨테이너 접속
docker compose exec backend bash
```

---

## 📚 문서

- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 프로젝트 전체 요약
- [MODULE_GUIDE.md](MODULE_GUIDE.md) - 각 모듈 상세 가이드
- [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) - 개발 가이드
- [DOCKER_SETUP.md](DOCKER_SETUP.md) - Docker 설치 및 실행
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - 기존 app.py 마이그레이션

---

## 🛠️ 기술 스택

### Backend
- **Framework**: Django 5.0, Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: MySQL 8.0
- **Vector DB**: ChromaDB (RAG)
- **LLM**: Qwen2.5-Coder (로컬 추론)

### Frontend
- **Framework**: React 18, Vite
- **State Management**: Redux Toolkit
- **Code Editor**: Monaco Editor
- **Styling**: CSS Modules
- **HTTP Client**: Axios

### Infrastructure
- **Containerization**: Docker, Docker Compose
- **Web Server**: Nginx (Reverse Proxy)
- **CI/CD**: GitHub Actions (예정)

---

## 👥 모듈별 개발

각 모듈은 독립적으로 개발 가능합니다:

| 모듈 | Backend 앱 | Frontend 페이지 | 담당 기능 |
|------|-----------|----------------|----------|
| **인증** | `authentication` | `MainPage` | 로그인/회원가입 |
| **코딩 테스트** | `coding_test` | `CodingTest` | 문제 풀이, 힌트 |
| **챗봇** | `chatbot` | `Chatbot` | RAG 기반 질의응답 |
| **마이페이지** | `mypage` | `MyPage` | 통계, 프로필 |
| **관리자** | `admin_panel` | `AdminPanel` | 모델 관리, 평가 |

자세한 내용은 [MODULE_GUIDE.md](MODULE_GUIDE.md)를 참고하세요.

---

## 🔑 주요 API 엔드포인트

### 인증
- `POST /api/v1/auth/signup/` - 회원가입
- `POST /api/v1/auth/login/` - 로그인
- `POST /api/v1/auth/logout/` - 로그아웃

### 코딩 테스트
- `GET /api/v1/coding-test/problems/` - 문제 목록
- `POST /api/v1/coding-test/problems/{id}/execute/` - 코드 실행
- `POST /api/v1/coding-test/problems/{id}/hint/` - 힌트 요청
- `POST /api/v1/coding-test/problems/{id}/submit/` - 제출

### 챗봇
- `POST /api/v1/chatbot/ask/` - 질문하기
- `GET /api/v1/chatbot/history/` - 대화 이력

### 관리자
- `GET /api/v1/admin/problems/{id}/solution/` - 답안 코드 (관리자만)
- `POST /api/v1/admin/hint/generate/` - 힌트 생성 (모델 선택)
- `POST /api/v1/admin/evaluation/` - 힌트 평가 저장

---

## 🎓 학습 시스템

### 레이팅 계산
```python
기본 점수 (난이도별):
- Level 1: 10점
- Level 2: 20점
- Level 3: 30점
- Level 4: 50점
- Level 5: 100점

보너스/페널티:
+ 빠른 풀이: 시간 보너스
- 많은 실행: 실행 횟수 페널티
+ 연속 풀이: 스트릭 보너스
```

### 성향 분석
- **완벽주의형**: 실행 1~2회로 정답, 신중한 접근
- **반복형**: 여러 번 실행하며 시행착오를 통한 학습

---

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다.

---

## 📧 문의

- **프로젝트 링크**: [https://github.com/yangjiwoo8465/proj_hint_system](https://github.com/yangjiwoo8465/proj_hint_system)
- **이슈 등록**: [Issues](https://github.com/yangjiwoo8465/proj_hint_system/issues)

---

**Happy Coding! 🚀**
