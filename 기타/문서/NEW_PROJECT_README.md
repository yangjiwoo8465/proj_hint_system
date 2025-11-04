# Hint System - AI 기반 코딩 학습 플랫폼

Django + React 기반의 모듈화된 코딩 학습 플랫폼

## 프로젝트 개요

이 프로젝트는 AI를 활용한 코딩 학습 플랫폼으로, 다음과 같은 주요 기능을 제공합니다:

- **코딩 테스트**: 문제 풀이, 코드 실행, AI 힌트 제공
- **문답 챗봇**: RAG 기반 질의응답 시스템
- **마이페이지**: 개인 통계, 북마크, 레이팅 관리
- **관리자 패널**: 힌트 및 챗봇 관리 (기존 app.py 기능 이전)

## 기술 스택

### 프론트엔드
- React 18
- Vite
- Redux Toolkit
- Monaco Editor
- Axios

### 백엔드
- Django 5.0
- Django REST Framework
- JWT 인증
- MySQL
- ChromaDB (벡터 DB)

### 인프라
- Nginx
- Docker & Docker Compose
- Gunicorn

## 프로젝트 구조

```
proj_hint_system/
├── backend/                 # Django 백엔드
│   ├── config/             # Django 설정
│   ├── apps/               # 탭별 모듈화된 앱
│   │   ├── authentication/ # 인증 (로그인/회원가입)
│   │   ├── coding_test/    # 코딩 테스트
│   │   ├── chatbot/        # 문답 챗봇
│   │   ├── mypage/         # 마이페이지
│   │   └── admin_panel/    # 관리자
│   ├── common/             # 공통 유틸리티
│   ├── vectordb/           # ChromaDB 연동
│   └── manage.py
│
├── frontend/               # React 프론트엔드
│   ├── src/
│   │   ├── components/     # 공통 컴포넌트
│   │   ├── pages/          # 탭별 페이지
│   │   │   ├── MainPage/
│   │   │   ├── CodingTest/
│   │   │   ├── Chatbot/
│   │   │   ├── MyPage/
│   │   │   └── AdminPanel/
│   │   ├── services/       # API 서비스
│   │   ├── store/          # Redux 상태 관리
│   │   └── utils/          # 유틸리티
│   └── package.json
│
├── hint-system/            # 기존 힌트 시스템 (재사용)
├── nginx/                  # Nginx 설정
├── docker-compose.yml
├── .env.example
└── PROJECT_STRUCTURE.md    # 상세 구조 설명
```

## 빠른 시작

### 1. 환경 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 수정 (DB 비밀번호 등)
vi .env
```

### 2. Docker로 실행

```bash
# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

서비스 접속:
- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000/api/v1
- **Django Admin**: http://localhost:8000/admin

### 3. 로컬 개발 환경

#### 백엔드

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser

# 개발 서버 실행
python manage.py runserver
```

#### 프론트엔드

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

## 주요 기능

### 1. 메인 화면 (MainPage)
- 로그인 / 회원가입
- 랜딩 페이지

**담당 파일**:
- Backend: `backend/apps/authentication/`
- Frontend: `frontend/src/pages/MainPage/`

### 2. 코딩 테스트 (CodingTest)
- 문제 목록 (tags, level 필터링)
- Monaco Editor 기반 코드 작성
- 코드 실행 및 결과 확인
- AI 힌트 제공 (대/중/소)
- 북마크 기능
- 사용자 성향 분석

**담당 파일**:
- Backend: `backend/apps/coding_test/`
- Frontend: `frontend/src/pages/CodingTest/`

### 3. 문답 챗봇 (Chatbot)
- RAG 기반 질의응답
- 채팅 북마크
- 답변 평가 (별점)

**담당 파일**:
- Backend: `backend/apps/chatbot/`
- Frontend: `frontend/src/pages/Chatbot/`

### 4. 마이페이지 (MyPage)
- 개인정보 관리
- 북마크 목록
- 레이팅 점수

**담당 파일**:
- Backend: `backend/apps/mypage/`
- Frontend: `frontend/src/pages/MyPage/`

### 5. 관리자 (AdminPanel)
- 힌트 챗봇 관리
- 문답 챗봇 관리
- 모델 설정

**담당 파일**:
- Backend: `backend/apps/admin_panel/`
- Frontend: `frontend/src/pages/AdminPanel/`

## API 엔드포인트

### 인증
- `POST /api/v1/auth/signup/` - 회원가입
- `POST /api/v1/auth/login/` - 로그인
- `POST /api/v1/auth/logout/` - 로그아웃
- `GET /api/v1/auth/user/` - 사용자 정보

### 코딩 테스트
- `GET /api/v1/coding-test/problems/` - 문제 목록
- `GET /api/v1/coding-test/problems/<id>/` - 문제 상세
- `POST /api/v1/coding-test/execute/` - 코드 실행
- `POST /api/v1/coding-test/hints/` - 힌트 요청
- `GET /api/v1/coding-test/bookmarks/` - 북마크 목록

### 챗봇
- `POST /api/v1/chatbot/chat/` - 채팅
- `GET /api/v1/chatbot/history/` - 채팅 기록
- `GET /api/v1/chatbot/bookmarks/` - 북마크 목록

### 마이페이지
- `GET /api/v1/mypage/profile/` - 프로필
- `GET /api/v1/mypage/statistics/` - 통계
- `GET /api/v1/mypage/rating/` - 레이팅

## 개발 가이드

### 새로운 탭 추가하기

1. **백엔드**: `backend/apps/` 폴더에 새 Django 앱 생성
2. **프론트엔드**: `frontend/src/pages/` 폴더에 새 페이지 생성
3. URL 라우팅 추가
4. 네비게이션 메뉴 업데이트

### 모듈 구조

각 탭은 독립된 모듈로 구성되어 있습니다:

**백엔드 모듈** (`apps/<탭명>/`):
- `models.py` - 데이터베이스 모델
- `serializers.py` - API 시리얼라이저
- `views.py` - API 뷰
- `urls.py` - URL 라우팅
- `services/` - 비즈니스 로직

**프론트엔드 모듈** (`pages/<탭명>/`):
- `index.jsx` - 메인 컴포넌트
- 하위 컴포넌트들
- `*.module.css` - 스타일

### 기존 hint-system 통합

기존 `hint-system/` 폴더의 모델 및 힌트 생성 로직은 재사용됩니다:
- `hint-system/models/` - LLM 모델 관리
- `hint-system/data/` - 문제 데이터

## 데이터베이스

### 초기 데이터 로드

```bash
# 문제 데이터 로드 (problems_multi_solution_complete.json)
python manage.py loaddata problems

# 또는 커스텀 관리 명령어 작성
python manage.py import_problems
```

### 마이그레이션

```bash
# 마이그레이션 파일 생성
python manage.py makemigrations

# 마이그레이션 실행
python manage.py migrate
```

## 테스트

```bash
# 백엔드 테스트
cd backend
python manage.py test

# 프론트엔드 테스트
cd frontend
npm run test
```

## 배포

### 프로덕션 설정

1. `.env` 파일에서 `DEBUG=False` 설정
2. `DJANGO_SECRET_KEY` 변경
3. `ALLOWED_HOSTS` 설정
4. Static 파일 수집:
   ```bash
   python manage.py collectstatic
   ```

### Docker 배포

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 문제 해결

### 일반적인 문제

1. **DB 연결 오류**: `.env` 파일의 DB 설정 확인
2. **CORS 오류**: `settings.py`의 CORS 설정 확인
3. **Static 파일 404**: `collectstatic` 실행 확인

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다.

## 기여

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 문의

프로젝트 관련 문의사항이 있으시면 Issue를 등록해주세요.
