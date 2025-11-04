# 프로젝트 구조 설계 문서

## 기술 스택
- **프론트엔드**: React, Monaco Editor
- **백엔드**: Django, Django REST Framework, JWT
- **웹서버**: Nginx
- **데이터베이스**: MySQL (메인 DB), ChromaDB (벡터 DB)
- **AI/ML**: 기존 LLM 모델 시스템 활용

## 전체 폴더 구조

```
proj_hint_system/
├── backend/                          # Django 백엔드
│   ├── config/                       # Django 프로젝트 설정
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── apps/                         # Django 앱들 (탭별 모듈화)
│   │   ├── authentication/           # 인증/회원가입
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── tests.py
│   │   ├── coding_test/              # 코딩 테스트
│   │   │   ├── models.py             # 문제, 북마크, 사용자 제출 기록
│   │   │   ├── serializers.py
│   │   │   ├── views.py              # 문제 목록, 실행, 힌트 API
│   │   │   ├── urls.py
│   │   │   ├── services/
│   │   │   │   ├── code_executor.py  # 코드 실행 서비스
│   │   │   │   ├── hint_generator.py # 힌트 생성 서비스
│   │   │   │   └── user_analyzer.py  # 사용자 성향 분석
│   │   │   └── tests.py
│   │   ├── chatbot/                  # 문답 챗봇
│   │   │   ├── models.py             # 채팅 기록, 북마크, 평가
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── services/
│   │   │   │   ├── rag_service.py    # RAG 기반 답변 생성
│   │   │   │   └── document_loader.py
│   │   │   └── tests.py
│   │   ├── mypage/                   # 마이페이지
│   │   │   ├── models.py             # 사용자 프로필, 통계
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── tests.py
│   │   └── admin_panel/              # 관리자
│   │       ├── models.py
│   │       ├── serializers.py
│   │       ├── views.py
│   │       ├── urls.py
│   │       └── tests.py
│   ├── common/                       # 공통 유틸리티
│   │   ├── permissions.py            # 권한 관리
│   │   ├── pagination.py
│   │   ├── exceptions.py
│   │   └── utils.py
│   ├── vectordb/                     # ChromaDB 연동
│   │   ├── chroma_client.py
│   │   └── embeddings.py
│   ├── requirements.txt
│   └── manage.py
│
├── frontend/                         # React 프론트엔드
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/               # 공통 컴포넌트
│   │   │   ├── Layout/
│   │   │   │   ├── Header.jsx
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   └── Footer.jsx
│   │   │   ├── Common/
│   │   │   │   ├── Button.jsx
│   │   │   │   ├── Input.jsx
│   │   │   │   ├── Modal.jsx
│   │   │   │   └── Loading.jsx
│   │   │   └── Editor/
│   │   │       └── MonacoEditor.jsx  # Monaco Editor 래퍼
│   │   ├── pages/                    # 탭별 페이지 (모듈화)
│   │   │   ├── MainPage/             # 메인 화면
│   │   │   │   ├── index.jsx
│   │   │   │   ├── Login.jsx
│   │   │   │   ├── Signup.jsx
│   │   │   │   ├── Landing.jsx
│   │   │   │   └── mainPage.module.css
│   │   │   ├── CodingTest/           # 코딩 테스트
│   │   │   │   ├── index.jsx
│   │   │   │   ├── ProblemList.jsx
│   │   │   │   ├── ProblemDetail.jsx
│   │   │   │   ├── CodeEditor.jsx
│   │   │   │   ├── Terminal.jsx
│   │   │   │   ├── HintPanel.jsx
│   │   │   │   └── codingTest.module.css
│   │   │   ├── Chatbot/              # 문답 챗봇
│   │   │   │   ├── index.jsx
│   │   │   │   ├── ChatInterface.jsx
│   │   │   │   ├── MessageBubble.jsx
│   │   │   │   ├── Rating.jsx
│   │   │   │   └── chatbot.module.css
│   │   │   ├── MyPage/               # 마이페이지
│   │   │   │   ├── index.jsx
│   │   │   │   ├── Profile.jsx
│   │   │   │   ├── Bookmarks.jsx
│   │   │   │   ├── Statistics.jsx
│   │   │   │   └── myPage.module.css
│   │   │   └── AdminPanel/           # 관리자
│   │   │       ├── index.jsx
│   │   │       ├── HintAdmin.jsx
│   │   │       ├── ChatbotAdmin.jsx
│   │   │       └── adminPanel.module.css
│   │   ├── services/                 # API 서비스
│   │   │   ├── api.js                # Axios 설정
│   │   │   ├── authService.js
│   │   │   ├── codingTestService.js
│   │   │   ├── chatbotService.js
│   │   │   ├── mypageService.js
│   │   │   └── adminService.js
│   │   ├── store/                    # 상태 관리 (Redux or Context)
│   │   │   ├── index.js
│   │   │   ├── authSlice.js
│   │   │   ├── codingTestSlice.js
│   │   │   └── chatbotSlice.js
│   │   ├── hooks/                    # 커스텀 훅
│   │   │   ├── useAuth.js
│   │   │   ├── useCodingTest.js
│   │   │   └── useChatbot.js
│   │   ├── utils/                    # 유틸리티
│   │   │   ├── constants.js
│   │   │   └── helpers.js
│   │   ├── App.jsx
│   │   ├── index.jsx
│   │   └── routes.jsx
│   ├── package.json
│   └── vite.config.js (or webpack.config.js)
│
├── hint-system/                      # 기존 힌트 시스템 (재사용)
│   ├── models/
│   │   ├── model_inference.py
│   │   ├── model_config.py
│   │   └── runpod_client.py
│   ├── data/
│   │   └── problems_multi_solution_complete.json
│   └── ...
│
├── nginx/                            # Nginx 설정
│   ├── nginx.conf
│   └── Dockerfile
│
├── docker-compose.yml                # 전체 서비스 오케스트레이션
├── .env.example
├── README.md
└── SETUP_GUIDE.md
```

## 모듈화 설계 원칙

### 1. 탭별 독립성
- 각 탭은 백엔드의 독립된 Django 앱과 프론트엔드의 독립된 페이지 폴더로 구성
- 각 모듈은 자체 models, views, serializers, 그리고 React 컴포넌트를 가짐
- 팀원은 각 탭의 폴더만 수정하면 해당 기능 완성 가능

### 2. 확장성
- 새로운 탭 추가 시:
  - 백엔드: `apps/` 폴더에 새 Django 앱 추가
  - 프론트엔드: `pages/` 폴더에 새 페이지 폴더 추가
  - URL 라우팅만 추가하면 즉시 사용 가능

### 3. 공통 컴포넌트 재사용
- Layout, Button 등 공통 컴포넌트는 `components/` 폴더에서 관리
- API 통신은 `services/` 폴더에서 중앙 관리
- 권한, 인증 등 공통 로직은 `common/` 폴더에서 관리

## 주요 기능별 모듈 매핑

### 메인 화면 (MainPage)
- **백엔드**: `apps/authentication/`
- **프론트엔드**: `pages/MainPage/`
- **기능**: 로그인, 회원가입, 랜딩 페이지

### 코딩 테스트 (CodingTest)
- **백엔드**: `apps/coding_test/`
- **프론트엔드**: `pages/CodingTest/`
- **기능**: 문제 선택, 코드 작성, 실행, 힌트, 북마크, 성향 분석

### 문답 챗봇 (Chatbot)
- **백엔드**: `apps/chatbot/`
- **프론트엔드**: `pages/Chatbot/`
- **기능**: RAG 기반 챗봇, 북마크, 평가

### 마이페이지 (MyPage)
- **백엔드**: `apps/mypage/`
- **프론트엔드**: `pages/MyPage/`
- **기능**: 프로필, 북마크 목록, 통계, 레이팅

### 관리자 (AdminPanel)
- **백엔드**: `apps/admin_panel/`
- **프론트엔드**: `pages/AdminPanel/`
- **기능**: 힌트 챗봇 관리, 문답 챗봇 관리 (기존 app.py 기능 이전)

## API 엔드포인트 구조

```
/api/v1/
├── auth/
│   ├── signup/
│   ├── login/
│   ├── logout/
│   ├── refresh/
│   └── user/
├── coding-test/
│   ├── problems/
│   ├── problems/<id>/
│   ├── execute/
│   ├── hints/
│   ├── bookmarks/
│   └── submissions/
├── chatbot/
│   ├── chat/
│   ├── history/
│   ├── bookmarks/
│   └── ratings/
├── mypage/
│   ├── profile/
│   ├── bookmarks/
│   ├── statistics/
│   └── rating/
└── admin/
    ├── hints/
    ├── chatbot/
    └── models/
```

## 데이터베이스 스키마 (주요 테이블)

### Users (인증)
- id, username, email, password, role (user/admin), created_at

### Problems (코딩 테스트)
- id, problem_id, title, level, tags, description, examples

### Submissions (제출 기록)
- id, user_id, problem_id, code, result, execution_count, time_spent

### Bookmarks (북마크)
- id, user_id, content_type (problem/chat), content_id, created_at

### ChatHistory (채팅 기록)
- id, user_id, question, answer, rating, created_at

### UserStatistics (사용자 통계)
- id, user_id, total_solved, rating, tendency_type

## 개발 워크플로우

1. **백엔드 개발자**: `backend/apps/<탭명>/` 폴더에서 작업
2. **프론트엔드 개발자**: `frontend/src/pages/<탭명>/` 폴더에서 작업
3. **API 연동**: `frontend/src/services/<탭명>Service.js`에서 API 호출 정의
4. **공통 기능**: `common/` 또는 `components/` 폴더에서 재사용 가능한 코드 작성

## 다음 단계
1. Django 프로젝트 초기화
2. React 프로젝트 초기화
3. Docker 환경 구성
4. 각 탭별 기본 구조 생성
5. 기존 hint-system의 모델 통합
