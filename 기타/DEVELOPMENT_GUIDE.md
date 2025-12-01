# 개발 가이드

## 팀 협업을 위한 모듈별 작업 가이드

이 프로젝트는 **탭별 모듈화**를 통해 여러 개발자가 동시에 작업할 수 있도록 설계되었습니다.

## 모듈별 작업 영역

### 1. 메인 화면 담당자

**작업 폴더**:
- Backend: `backend/apps/authentication/`
- Frontend: `frontend/src/pages/MainPage/`

**담당 기능**:
- 로그인/회원가입 UI
- 랜딩 페이지 디자인
- JWT 토큰 관리
- 사용자 정보 수정

**주요 파일**:
```
backend/apps/authentication/
├── models.py          # User 모델
├── views.py           # 로그인/회원가입 API
├── serializers.py     # 사용자 시리얼라이저
└── urls.py            # 인증 URL

frontend/src/pages/MainPage/
├── index.jsx          # 메인 페이지
├── Login.jsx          # 로그인 컴포넌트
├── Signup.jsx         # 회원가입 컴포넌트
└── Landing.jsx        # 랜딩 페이지
```

---

### 2. 코딩 테스트 담당자

**작업 폴더**:
- Backend: `backend/apps/coding_test/`
- Frontend: `frontend/src/pages/CodingTest/`

**담당 기능**:
- 문제 목록 및 필터링
- Monaco Editor 통합
- 코드 실행 엔진
- AI 힌트 생성
- 북마크 기능
- 사용자 성향 분석

**주요 파일**:
```
backend/apps/coding_test/
├── models.py          # Problem, Submission, Bookmark 모델
├── views.py           # 문제, 실행, 힌트 API
├── serializers.py
├── services/
│   ├── code_executor.py    # 코드 실행 로직
│   ├── hint_generator.py   # 힌트 생성 (기존 hint-system 연동)
│   └── user_analyzer.py    # 성향 분석
└── urls.py

frontend/src/pages/CodingTest/
├── index.jsx          # 메인 페이지
├── ProblemList.jsx    # 문제 목록
├── ProblemDetail.jsx  # 문제 상세
├── CodeEditor.jsx     # Monaco Editor
├── Terminal.jsx       # 실행 결과
└── HintPanel.jsx      # 힌트 패널
```

**핵심 로직**:
1. 문제 데이터는 `hint-system/data/problems_multi_solution_complete.json`에서 로드
2. 코드 실행은 `services/code_executor.py`에서 처리
3. 힌트 생성은 기존 `hint-system/models/` 활용

---

### 3. 챗봇 담당자

**작업 폴더**:
- Backend: `backend/apps/chatbot/`
- Frontend: `frontend/src/pages/Chatbot/`

**담당 기능**:
- RAG 기반 질의응답
- 채팅 인터페이스
- 북마크 기능
- 답변 평가 (별점)

**주요 파일**:
```
backend/apps/chatbot/
├── models.py          # ChatHistory, Bookmark, Rating 모델
├── views.py           # 채팅 API
├── services/
│   ├── rag_service.py      # RAG 로직 (ChromaDB 활용)
│   └── document_loader.py  # 문서 로드 (Python, Git 공식문서)
└── urls.py

frontend/src/pages/Chatbot/
├── index.jsx          # 메인 페이지
├── ChatInterface.jsx  # 채팅 UI
├── MessageBubble.jsx  # 메시지 말풍선
└── Rating.jsx         # 평가 컴포넌트
```

**핵심 로직**:
1. ChromaDB를 사용한 벡터 검색 (`backend/vectordb/chroma_client.py`)
2. 문서 임베딩은 `vectordb/embeddings.py` 사용

---

### 4. 마이페이지 담당자

**작업 폴더**:
- Backend: `backend/apps/mypage/`
- Frontend: `frontend/src/pages/MyPage/`

**담당 기능**:
- 개인정보 조회/수정
- 북마크 목록 (문제 + 채팅)
- 통계 및 레이팅
- 회원 탈퇴

**주요 파일**:
```
backend/apps/mypage/
├── models.py          # UserStatistics 모델
├── views.py           # 프로필, 북마크, 통계 API
└── urls.py

frontend/src/pages/MyPage/
├── index.jsx          # 메인 페이지
├── Profile.jsx        # 프로필
├── Bookmarks.jsx      # 북마크 목록
└── Statistics.jsx     # 통계
```

---

### 5. 관리자 패널 담당자

**작업 폴더**:
- Backend: `backend/apps/admin_panel/`
- Frontend: `frontend/src/pages/AdminPanel/`

**담당 기능**:
- 힌트 챗봇 관리 (기존 app.py 기능)
- 문답 챗봇 관리
- 모델 설정 변경
- Temperature 조정

**주요 파일**:
```
backend/apps/admin_panel/
├── models.py
├── views.py           # 관리자 전용 API
└── urls.py

frontend/src/pages/AdminPanel/
├── index.jsx
├── HintAdmin.jsx      # 힌트 챗봇 관리 (기존 app.py 이전)
└── ChatbotAdmin.jsx   # 문답 챗봇 관리
```

**기존 코드 이전**:
- `hint-system/app.py`의 관리자 기능을 AdminPanel로 이전
- 답안코드 조회, 모델 변경, Temperature 설정 등 유지

---

## 공통 작업 영역

### API 서비스 (모든 담당자)

각 담당자는 자신의 기능에 대한 API 서비스를 `frontend/src/services/`에 작성합니다.

```javascript
// frontend/src/services/codingTestService.js
import api from './api'

export const getProblems = async (params) => {
  const response = await api.get('/coding-test/problems/', { params })
  return response.data
}

export const executeCode = async (code, problemId) => {
  const response = await api.post('/coding-test/execute/', { code, problem_id: problemId })
  return response.data
}
```

### Redux 상태 관리

각 담당자는 자신의 Slice를 관리합니다:
- `frontend/src/store/authSlice.js` - 인증 담당자
- `frontend/src/store/codingTestSlice.js` - 코딩 테스트 담당자
- `frontend/src/store/chatbotSlice.js` - 챗봇 담당자

---

## 개발 워크플로우

### 1. 브랜치 전략

```bash
# 기능별 브랜치 생성
git checkout -b feature/coding-test
git checkout -b feature/chatbot
git checkout -b feature/mypage
git checkout -b feature/admin
```

### 2. 커밋 컨벤션

```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 추가
chore: 빌드 업무 수정

예시:
feat(coding-test): Add code execution feature
fix(chatbot): Fix RAG search bug
```

### 3. Pull Request 작성

1. 자신의 모듈 폴더에서만 작업
2. 공통 파일 수정 시 팀원과 협의
3. PR 템플릿 사용:

```markdown
## 변경 사항
- [ ] 기능 A 추가
- [ ] 버그 B 수정

## 테스트
- [ ] 로컬 테스트 완료
- [ ] API 테스트 완료

## 스크린샷
(필요시 추가)
```

---

## 로컬 개발 환경 설정

### 백엔드 개발자

```bash
# 1. 가상환경 생성
cd backend
python -m venv venv
source venv/bin/activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 데이터베이스 마이그레이션
python manage.py migrate

# 4. 개발 서버 실행
python manage.py runserver

# 5. 자신의 앱만 마이그레이션
python manage.py makemigrations coding_test
python manage.py migrate coding_test
```

### 프론트엔드 개발자

```bash
# 1. 의존성 설치
cd frontend
npm install

# 2. 개발 서버 실행
npm run dev

# 3. 자신의 페이지 작업
# pages/CodingTest/ 폴더에서만 작업
```

---

## API 테스트

### Postman/Thunder Client 사용

```bash
# 1. 로그인으로 토큰 획득
POST http://localhost:8000/api/v1/auth/login/
Body: {
  "username": "testuser",
  "password": "testpass"
}

# 2. 토큰을 Header에 추가
Authorization: Bearer <access_token>

# 3. API 테스트
GET http://localhost:8000/api/v1/coding-test/problems/
```

---

## 문제 해결

### 백엔드

**마이그레이션 충돌**:
```bash
# 충돌 발생 시
python manage.py migrate --fake
python manage.py migrate
```

**포트 충돌**:
```bash
# 8000 포트 사용 중인 프로세스 종료
lsof -ti:8000 | xargs kill -9
```

### 프론트엔드

**의존성 오류**:
```bash
# node_modules 삭제 후 재설치
rm -rf node_modules package-lock.json
npm install
```

**빌드 오류**:
```bash
# 캐시 삭제
npm run clean
npm run dev
```

---

## 코드 리뷰 체크리스트

### 백엔드
- [ ] 모델 필드에 `verbose_name` 추가
- [ ] API 응답은 `common/utils.py`의 `success_response`, `error_response` 사용
- [ ] 권한 체크 (`@permission_classes` 데코레이터)
- [ ] 에러 핸들링
- [ ] 테스트 코드 작성

### 프론트엔드
- [ ] 컴포넌트 재사용성
- [ ] Redux 액션 사용
- [ ] API 에러 처리
- [ ] 로딩 상태 표시
- [ ] CSS 모듈 사용

---

## 추가 자료

- [Django REST Framework 공식 문서](https://www.django-rest-framework.org/)
- [React 공식 문서](https://react.dev/)
- [Redux Toolkit 공식 문서](https://redux-toolkit.js.org/)
- [Monaco Editor 문서](https://microsoft.github.io/monaco-editor/)

---

## 질문 및 지원

팀 슬랙 채널 또는 GitHub Issues를 통해 문의해주세요.
