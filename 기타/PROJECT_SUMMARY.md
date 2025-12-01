# 프로젝트 구조 요약

## 프로젝트 완료 ✅

Django + React 기반의 **탭별 모듈화된** AI 코딩 학습 플랫폼이 성공적으로 구성되었습니다.

---

## 생성된 구조

### 📁 백엔드 (Django)

```
backend/
├── config/                     # Django 프로젝트 설정
│   ├── settings.py            # ✅ JWT, CORS, DB 설정 완료
│   ├── urls.py                # ✅ 모든 앱 URL 라우팅
│   └── wsgi.py / asgi.py      # ✅ WSGI/ASGI 설정
│
├── apps/                       # 탭별 모듈화된 Django 앱
│   ├── authentication/         # ✅ 로그인/회원가입
│   │   ├── models.py          # User 모델 (role, rating, tendency)
│   │   ├── views.py           # 로그인, 회원가입, 로그아웃 API
│   │   ├── serializers.py     # JWT 토큰 포함
│   │   └── urls.py
│   │
│   ├── coding_test/            # ✅ 코딩 테스트
│   │   ├── models.py          # Problem, Submission, Bookmark, HintRequest
│   │   ├── views.py           # 문제 조회, 코드 실행, 힌트 API
│   │   ├── urls.py
│   │   └── services/          # (생성 필요) code_executor, hint_generator
│   │
│   ├── chatbot/                # ✅ 문답 챗봇
│   │   ├── models.py          # (생성 필요) ChatHistory, Bookmark, Rating
│   │   ├── views.py           # (생성 필요) RAG 기반 챗봇 API
│   │   └── services/          # (생성 필요) rag_service, document_loader
│   │
│   ├── mypage/                 # ✅ 마이페이지
│   │   ├── models.py          # (생성 필요) UserStatistics
│   │   └── views.py           # (생성 필요) 프로필, 북마크, 통계 API
│   │
│   └── admin_panel/            # ✅ 관리자 패널
│       └── views.py           # (생성 필요) 기존 app.py 기능 이전
│
├── common/                     # ✅ 공통 유틸리티
│   ├── permissions.py         # IsAdminUser, IsOwnerOrAdmin
│   ├── pagination.py          # 페이지네이션 클래스
│   ├── exceptions.py          # 커스텀 예외
│   └── utils.py               # success_response, calculate_rating_points
│
└── vectordb/                   # ✅ ChromaDB 연동
    ├── chroma_client.py       # ChromaDB 싱글톤 클라이언트
    └── embeddings.py          # 임베딩 생성기
```

### 📁 프론트엔드 (React)

```
frontend/
├── src/
│   ├── components/             # ✅ 공통 컴포넌트
│   │   ├── Layout/
│   │   │   └── Layout.jsx     # 사이드바, 네비게이션 (완성)
│   │   ├── Common/            # (생성 필요) Button, Input, Modal
│   │   └── Editor/            # (생성 필요) Monaco Editor 래퍼
│   │
│   ├── pages/                  # ✅ 탭별 페이지
│   │   ├── MainPage/          # 기본 구조 생성 (TODO: 로그인/회원가입 UI)
│   │   ├── CodingTest/        # 기본 구조 생성 (TODO: 문제 목록, 에디터)
│   │   ├── Chatbot/           # 기본 구조 생성 (TODO: 채팅 인터페이스)
│   │   ├── MyPage/            # 기본 구조 생성 (TODO: 프로필, 북마크)
│   │   └── AdminPanel/        # 기본 구조 생성 (TODO: 관리자 기능)
│   │
│   ├── services/               # ✅ API 서비스
│   │   └── api.js             # Axios 인터셉터, JWT 자동 갱신
│   │
│   ├── store/                  # ✅ Redux 상태 관리
│   │   ├── authSlice.js       # 인증 상태
│   │   ├── codingTestSlice.js # 코딩 테스트 상태
│   │   └── chatbotSlice.js    # 챗봇 상태
│   │
│   ├── utils/                  # ✅ 유틸리티
│   │   ├── constants.js       # 상수 정의
│   │   └── helpers.js         # 헬퍼 함수
│   │
│   ├── App.jsx                 # ✅ 라우팅 설정 (권한별 분기)
│   └── index.jsx               # ✅ Redux Provider, Router 설정
│
└── package.json                # ✅ 의존성 (React, Monaco Editor, Axios 등)
```

### 📁 인프라

```
프로젝트 루트/
├── nginx/
│   ├── nginx.conf              # ✅ 프록시 설정 (프론트/백엔드 분리)
│   └── Dockerfile              # ✅ Nginx 컨테이너
│
├── docker-compose.yml          # ✅ 전체 서비스 오케스트레이션
│   ├── db (MySQL)
│   ├── backend (Django)
│   ├── frontend (React)
│   └── nginx
│
└── .env.example                # ✅ 환경 변수 템플릿
```

---

## 주요 기능 현황

### ✅ 완료된 항목

1. **프로젝트 구조**
   - 탭별 모듈화 완료
   - 백엔드/프론트엔드 분리
   - Docker 환경 구성

2. **인증 시스템**
   - JWT 기반 인증
   - 로그인/회원가입 API
   - 토큰 자동 갱신

3. **데이터베이스**
   - MySQL 모델 정의 (User, Problem, Submission, Bookmark 등)
   - ChromaDB 연동 준비

4. **공통 기능**
   - 권한 관리 (IsAdminUser, IsOwnerOrAdmin)
   - API 응답 포맷 통일
   - 레이팅 점수 계산 로직

5. **프론트엔드 기반**
   - Redux 상태 관리 설정
   - API 서비스 레이어
   - 레이아웃 컴포넌트

### 🚧 구현 필요 항목

각 담당자가 자신의 모듈에서 구현해야 할 사항:

#### 1. 메인 화면 (MainPage)
- [ ] 로그인 UI
- [ ] 회원가입 UI
- [ ] 랜딩 페이지 디자인

#### 2. 코딩 테스트 (CodingTest)
- [ ] 문제 목록 UI (필터링)
- [ ] Monaco Editor 통합
- [ ] 코드 실행 서비스 (`services/code_executor.py`)
- [ ] 힌트 생성 서비스 (`services/hint_generator.py` - 기존 hint-system 연동)
- [ ] 터미널 UI
- [ ] 사용자 성향 분석 로직

#### 3. 챗봇 (Chatbot)
- [ ] 채팅 인터페이스 UI
- [ ] RAG 서비스 (`services/rag_service.py`)
- [ ] 문서 로더 (`services/document_loader.py`)
- [ ] 북마크 기능
- [ ] 별점 평가 UI

#### 4. 마이페이지 (MyPage)
- [ ] 프로필 UI
- [ ] 북마크 목록 (문제 + 채팅)
- [ ] 통계 대시보드
- [ ] 레이팅 시각화

#### 5. 관리자 (AdminPanel)
- [ ] 기존 `hint-system/app.py`의 관리자 기능 이전
- [ ] 답안코드 조회
- [ ] 모델 변경 UI
- [ ] Temperature 설정

---

## 다음 단계 (우선순위)

### Phase 1: 기본 기능 구현 (1-2주)

1. **문제 데이터 로드**
   ```bash
   # backend/apps/coding_test/management/commands/import_problems.py 작성
   python manage.py import_problems
   ```

2. **각 탭의 기본 UI 구현**
   - 로그인/회원가입 폼
   - 문제 목록 + Monaco Editor
   - 채팅 인터페이스
   - 프로필 페이지

3. **핵심 API 구현**
   - 코드 실행 API
   - 힌트 생성 API
   - 챗봇 API

### Phase 2: 고급 기능 (2-3주)

4. **기존 hint-system 통합**
   - `hint-system/models/` 연동
   - AdminPanel에서 모델 관리

5. **ChromaDB 문서 임베딩**
   - Python 공식문서 처리
   - Git 공식문서 처리

6. **사용자 성향 분석**
   - 문제 풀이 패턴 분석
   - 맞춤형 힌트 제공

### Phase 3: 최적화 및 배포 (1-2주)

7. **UI/UX 개선**
   - 반응형 디자인
   - 로딩 상태 표시

8. **테스트 작성**
   - 백엔드 유닛 테스트
   - 프론트엔드 컴포넌트 테스트

9. **프로덕션 배포**
   - HTTPS 설정
   - 성능 최적화

---

## 팀 협업 가이드

### 브랜치 전략

```bash
main                    # 프로덕션
├── develop            # 개발 통합
│   ├── feature/auth           # 인증 담당자
│   ├── feature/coding-test    # 코딩 테스트 담당자
│   ├── feature/chatbot        # 챗봇 담당자
│   ├── feature/mypage         # 마이페이지 담당자
│   └── feature/admin          # 관리자 담당자
```

### 작업 영역 분리

| 담당자 | 백엔드 폴더 | 프론트엔드 폴더 |
|--------|------------|----------------|
| 인증 | `apps/authentication/` | `pages/MainPage/` |
| 코딩 테스트 | `apps/coding_test/` | `pages/CodingTest/` |
| 챗봇 | `apps/chatbot/` | `pages/Chatbot/` |
| 마이페이지 | `apps/mypage/` | `pages/MyPage/` |
| 관리자 | `apps/admin_panel/` | `pages/AdminPanel/` |

### 중요 참고 문서

1. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 상세 구조 설명
2. [NEW_PROJECT_README.md](NEW_PROJECT_README.md) - 전체 프로젝트 개요
3. [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) - 개발 가이드
4. [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) - 설치 및 실행 가이드

---

## 기존 프로젝트와의 관계

### 재사용되는 부분
- `hint-system/models/` - LLM 모델 관리
- `hint-system/data/` - 문제 데이터
- 힌트 생성 로직

### 새롭게 구현된 부분
- Django REST API
- React 프론트엔드
- JWT 인증
- 모듈화된 구조
- 챗봇 기능
- 사용자 관리

---

## 실행 방법

### Docker로 실행 (권장)

```bash
# 환경 설정
cp .env.example .env
nano .env  # DB 비밀번호 등 수정

# 실행
docker-compose up -d --build

# 마이그레이션
docker-compose exec backend python manage.py migrate

# 슈퍼유저 생성
docker-compose exec backend python manage.py createsuperuser

# 접속
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Admin: http://localhost:8000/admin
```

### 로컬 개발

상세한 내용은 [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) 참고

---

## 문의 및 지원

- 구조 관련 질문: `PROJECT_STRUCTURE.md` 참고
- 개발 가이드: `DEVELOPMENT_GUIDE.md` 참고
- 설치 문제: `SETUP_INSTRUCTIONS.md` 참고

---

**프로젝트 생성 완료!** 🎉

이제 각 담당자가 자신의 모듈 폴더에서 작업을 시작하면 됩니다.
