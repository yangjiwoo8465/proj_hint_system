# 모듈별 상세 가이드

## 📊 모듈별 작업 영역

각 팀원이 **자신의 폴더에서만 작업**하면 해당 탭의 모든 기능을 구현할 수 있습니다.

---

## 1. 메인 화면 (MainPage)

### 담당 영역
- **백엔드**: `backend/apps/authentication/`
- **프론트엔드**: `frontend/src/pages/MainPage/`

### 📁 백엔드 구조
```
apps/authentication/
├── models.py           ✅ 수정 - User 모델 (커스텀 필드 추가 가능)
├── serializers.py      ✅ 수정 - API 응답 형식
├── views.py            ✅ 수정 - 로그인/회원가입 로직
├── urls.py             ✅ 수정 - API 엔드포인트 추가
├── admin.py            ✅ 수정 - Django Admin 설정
└── tests.py            ✅ 수정 - 테스트 코드
```

### 🎨 프론트엔드 구조
```
pages/MainPage/
├── index.jsx           ✅ 수정 - 메인 페이지 (랜딩)
├── Login.jsx           ✅ 추가 - 로그인 폼
├── Signup.jsx          ✅ 추가 - 회원가입 폼
├── Landing.jsx         ✅ 추가 - 프로젝트 소개 페이지
└── mainPage.module.css ✅ 추가 - 스타일
```

### 🔧 수정 가능한 내용

#### 백엔드
- **User 모델** (`models.py`)
  - 추가 필드: 닉네임, 프로필 이미지, 선호 언어 등
  - 예시: `nickname = models.CharField(max_length=50)`

- **회원가입 로직** (`views.py`)
  - 이메일 인증 추가
  - 소셜 로그인 (Google, GitHub 등)
  - 비밀번호 재설정

- **API 엔드포인트** (`urls.py`)
  - 추가 경로: `/auth/verify-email/`, `/auth/reset-password/`

#### 프론트엔드
- **랜딩 페이지** (`Landing.jsx`)
  - 프로젝트 강점 홍보
  - 기능 소개 섹션
  - 애니메이션 효과

- **로그인/회원가입 폼**
  - UI/UX 디자인
  - 폼 유효성 검사
  - 에러 메시지 표시

### 📌 핵심 기능
- ✅ JWT 토큰 기반 인증 (이미 설정됨)
- ⏳ 로그인 UI
- ⏳ 회원가입 UI
- ⏳ 비밀번호 재설정
- ⏳ 랜딩 페이지 디자인

---

## 2. 코딩 테스트 (CodingTest) ⭐

### 담당 영역
- **백엔드**: `backend/apps/coding_test/`
- **프론트엔드**: `frontend/src/pages/CodingTest/`

### 📁 백엔드 구조
```
apps/coding_test/
├── models/                     ✅ 재사용 - LLM 모델 추론
│   ├── model_inference.py     (hint-system에서 이동)
│   ├── model_config.py
│   └── runpod_client.py
│
├── data/                       ✅ 재사용 - 문제 데이터
│   └── problems_multi_solution_complete.json
│
├── services/                   ✅ 수정 - 비즈니스 로직
│   ├── hint_generator.py      (TODO) 힌트 생성
│   ├── code_executor.py       (TODO) 코드 실행
│   └── user_analyzer.py       (TODO) 성향 분석
│
├── models.py                   ✅ 수정 - Django 모델
│   ├── Problem                문제
│   ├── Submission             제출 기록
│   ├── Bookmark               북마크
│   └── HintRequest            힌트 요청 기록
│
├── views.py                    ✅ 수정 - REST API
├── serializers.py              ✅ 수정 - API 직렬화
├── urls.py                     ✅ 수정 - 엔드포인트
└── admin.py                    ✅ 수정 - Admin 설정
```

### 🎨 프론트엔드 구조
```
pages/CodingTest/
├── index.jsx                   ✅ 수정 - 메인 레이아웃
├── ProblemList.jsx             ✅ 추가 - 문제 목록 (필터링)
├── ProblemDetail.jsx           ✅ 추가 - 문제 상세 정보
├── CodeEditor.jsx              ✅ 추가 - Monaco Editor 통합
├── Terminal.jsx                ✅ 추가 - 실행 결과 표시
├── HintPanel.jsx               ✅ 추가 - 힌트 요청/표시
└── codingTest.module.css       ✅ 추가 - 스타일
```

### 🔧 수정 가능한 내용

#### 백엔드
- **힌트 생성 서비스** (`services/hint_generator.py`)
  ```python
  class HintGenerator:
      def __init__(self):
          # models/model_inference.py 사용
          self.model_manager = ModelManager()

      def generate_hint(self, problem, user_code, level):
          # 대/중/소 힌트 생성 로직
          # 사용자 성향에 따른 맞춤형 힌트
          pass
  ```

- **코드 실행 서비스** (`services/code_executor.py`)
  ```python
  class CodeExecutor:
      def execute(self, code, test_cases):
          # 코드 실행 (subprocess 사용)
          # 타임아웃 처리
          # 결과 반환
          pass
  ```

- **사용자 성향 분석** (`services/user_analyzer.py`)
  ```python
  class UserAnalyzer:
      def analyze_tendency(self, submissions):
          # 실행 횟수, 풀이 시간 분석
          # 'perfectionist' or 'iterative' 판별
          pass
  ```

- **API 엔드포인트** (`views.py`)
  - `GET /problems/` - 문제 목록 (tags, level 필터)
  - `GET /problems/<id>/` - 문제 상세
  - `POST /execute/` - 코드 실행
  - `POST /hints/` - 힌트 요청
  - `POST /bookmarks/toggle/` - 북마크 토글

#### 프론트엔드
- **문제 목록** (`ProblemList.jsx`)
  - tags, level 필터링
  - 검색 기능
  - 페이지네이션

- **Monaco Editor** (`CodeEditor.jsx`)
  - Python 문법 하이라이팅
  - 자동완성
  - 테마 설정

- **힌트 패널** (`HintPanel.jsx`)
  - 대/중/소 힌트 버튼
  - 힌트 표시
  - 북마크 기능

- **터미널** (`Terminal.jsx`)
  - 실행 결과 출력
  - 에러 메시지 표시
  - 실행 시간 표시

### 📌 핵심 기능
- ✅ 문제 데이터 준비 (problems_multi_solution_complete.json)
- ✅ LLM 모델 로직 준비 (models/)
- ⏳ 문제 목록 UI (필터링)
- ⏳ Monaco Editor 통합
- ⏳ 코드 실행 엔진
- ⏳ 힌트 생성 (LLM 연동)
- ⏳ 북마크 기능
- ⏳ 사용자 성향 분석

---

## 3. 챗봇 (Chatbot)

### 담당 영역
- **백엔드**: `backend/apps/chatbot/`
- **프론트엔드**: `frontend/src/pages/Chatbot/`

### 📁 백엔드 구조
```
apps/chatbot/
├── models.py                   ✅ 수정 - Django 모델
│   ├── ChatHistory            채팅 기록
│   ├── Bookmark               북마크
│   └── Rating                 평가
│
├── serializers.py              ✅ 수정 - API 직렬화
├── views.py                    ✅ 수정 - REST API
├── urls.py                     ✅ 수정 - 엔드포인트
│
└── services/                   ✅ 수정 - 비즈니스 로직
    ├── rag_service.py         (TODO) RAG 기반 답변 생성
    └── document_loader.py     (TODO) 문서 로드 및 임베딩
```

### 🎨 프론트엔드 구조
```
pages/Chatbot/
├── index.jsx                   ✅ 수정 - 메인 레이아웃
├── ChatInterface.jsx           ✅ 추가 - 채팅 UI
├── MessageBubble.jsx           ✅ 추가 - 메시지 말풍선 (북마크/복사)
├── Rating.jsx                  ✅ 추가 - 별점 평가
└── chatbot.module.css          ✅ 추가 - 스타일
```

### 🔧 수정 가능한 내용

#### 백엔드
- **RAG 서비스** (`services/rag_service.py`)
  ```python
  class RAGService:
      def __init__(self):
          # ChromaDB 클라이언트 사용
          from vectordb.chroma_client import get_chroma_client
          self.chroma = get_chroma_client()

      def answer_question(self, question):
          # 1. 벡터 검색으로 관련 문서 찾기
          docs = self.chroma.query([question], n_results=5)
          # 2. LLM으로 답변 생성
          # 3. 답변 반환
          pass
  ```

- **문서 로더** (`services/document_loader.py`)
  ```python
  class DocumentLoader:
      def load_python_docs(self):
          # Python 공식 문서 로드
          # 청크 단위로 분할
          # ChromaDB에 임베딩 저장
          pass

      def load_git_docs(self):
          # Git 공식 문서 로드
          pass
  ```

- **API 엔드포인트** (`views.py`)
  - `POST /chat/` - 질문 및 답변
  - `GET /history/` - 채팅 기록
  - `POST /bookmarks/toggle/` - 북마크
  - `POST /ratings/` - 평가

#### 프론트엔드
- **채팅 인터페이스** (`ChatInterface.jsx`)
  - 실시간 채팅 UI
  - 스크롤 자동 하단 이동
  - 로딩 인디케이터

- **메시지 말풍선** (`MessageBubble.jsx`)
  - 북마크 버튼
  - 복사 버튼
  - Markdown 렌더링

- **별점 평가** (`Rating.jsx`)
  - 5점 만점 별점
  - 평가 저장

### 📌 핵심 기능
- ✅ ChromaDB 클라이언트 준비 (vectordb/)
- ⏳ Python/Git 문서 임베딩
- ⏳ RAG 기반 답변 생성
- ⏳ 채팅 UI
- ⏳ 북마크 기능
- ⏳ 별점 평가

---

## 4. 마이페이지 (MyPage)

### 담당 영역
- **백엔드**: `backend/apps/mypage/`
- **프론트엔드**: `frontend/src/pages/MyPage/`

### 📁 백엔드 구조
```
apps/mypage/
├── models.py                   ✅ 수정 - Django 모델
│   └── UserStatistics         사용자 통계
│
├── serializers.py              ✅ 수정 - API 직렬화
├── views.py                    ✅ 수정 - REST API
└── urls.py                     ✅ 수정 - 엔드포인트
```

### 🎨 프론트엔드 구조
```
pages/MyPage/
├── index.jsx                   ✅ 수정 - 메인 레이아웃
├── Profile.jsx                 ✅ 추가 - 프로필 정보
├── Bookmarks.jsx               ✅ 추가 - 북마크 목록
├── Statistics.jsx              ✅ 추가 - 통계 대시보드
└── myPage.module.css           ✅ 추가 - 스타일
```

### 🔧 수정 가능한 내용

#### 백엔드
- **사용자 통계 모델** (`models.py`)
  ```python
  class UserStatistics(models.Model):
      user = models.OneToOneField(User)
      total_solved = models.IntegerField(default=0)
      total_hints_used = models.IntegerField(default=0)
      average_execution_count = models.FloatField(default=0)
      # 추가 통계 필드 자유롭게 추가 가능
  ```

- **API 엔드포인트** (`views.py`)
  - `GET /profile/` - 프로필 조회
  - `PUT /profile/` - 프로필 수정
  - `GET /bookmarks/` - 북마크 목록 (문제 + 채팅)
  - `GET /statistics/` - 통계 데이터
  - `GET /rating/` - 레이팅 점수

#### 프론트엔드
- **프로필** (`Profile.jsx`)
  - 아이디, 이메일, 권한 표시
  - 비밀번호 변경
  - 회원 탈퇴
  - 로그아웃

- **북마크 목록** (`Bookmarks.jsx`)
  - 문제 북마크 (CodingTest)
  - 채팅 북마크 (Chatbot)
  - 탭으로 구분

- **통계** (`Statistics.jsx`)
  - 해결한 문제 수
  - 레이팅 점수
  - 성향 (완벽주의형/반복형)
  - 차트/그래프

### 📌 핵심 기능
- ✅ User 모델 (authentication 앱)
- ⏳ 프로필 조회/수정 UI
- ⏳ 북마크 통합 목록
- ⏳ 통계 대시보드
- ⏳ 레이팅 시각화

---

## 5. 관리자 (AdminPanel) 🔐

### 담당 영역
- **백엔드**: `backend/apps/admin_panel/`
- **프론트엔드**: `frontend/src/pages/AdminPanel/`

### 📁 백엔드 구조
```
apps/admin_panel/
├── models.py                   ✅ 수정 - Django 모델
│   ├── ModelConfiguration     모델 설정
│   └── HintEvaluation         힌트 평가 기록
│
├── serializers.py              ✅ 수정 - API 직렬화
├── views.py                    ✅ 수정 - REST API (관리자 전용)
└── urls.py                     ✅ 수정 - 엔드포인트
```

### 🎨 프론트엔드 구조
```
pages/AdminPanel/
├── index.jsx                   ✅ 수정 - 메인 레이아웃
├── HintAdmin.jsx               ✅ 추가 - 힌트 챗봇 관리 (기존 app.py)
├── ChatbotAdmin.jsx            ✅ 추가 - 문답 챗봇 관리
├── ModelConfig.jsx             ✅ 추가 - 모델 설정
└── adminPanel.module.css       ✅ 추가 - 스타일
```

### 🔧 수정 가능한 내용

#### 백엔드
- **모델 설정** (`models.py`)
  ```python
  class ModelConfiguration(models.Model):
      name = models.CharField(max_length=200)
      path = models.CharField(max_length=500)
      quantize = models.BooleanField(default=False)
      model_type = models.CharField(max_length=50)
      temperature = models.FloatField(default=0.7)
      # 모델별 설정 추가 가능
  ```

- **관리자 전용 API** (`views.py`)
  - `GET /hints/solutions/<problem_id>/` - 답안 코드 조회 ⭐
  - `POST /hints/generate/` - 힌트 생성 (모델/Temperature 선택)
  - `GET /models/` - 모델 목록
  - `POST /models/` - 모델 추가
  - `DELETE /models/<id>/` - 모델 제거
  - `GET /evaluations/` - 평가 기록

#### 프론트엔드
- **힌트 관리** (`HintAdmin.jsx`)
  - 문제 선택
  - **답안 코드 보기 버튼** ⭐ (관리자만)
  - 모델 선택 드롭다운
  - Temperature 슬라이더
  - 힌트 레벨 (대/중/소)
  - 힌트 생성 및 비교
  - 평가 저장

- **모델 설정** (`ModelConfig.jsx`)
  - 모델 목록
  - 모델 추가/제거
  - 우선순위 설정

- **챗봇 관리** (`ChatbotAdmin.jsx`)
  - 챗봇 모델 설정
  - 답변 품질 모니터링

### 📌 핵심 기능
- ✅ 권한 체크 (IsAdminUser)
- ⏳ 답안 코드 조회 API
- ⏳ 힌트 관리 UI (기존 app.py 기능)
- ⏳ 모델 관리
- ⏳ 평가 통계

---

## 🔗 모듈 간 연동

### API 서비스 (`frontend/src/services/`)

각 모듈은 자신의 API 서비스 파일을 가집니다:

```
services/
├── api.js                      공통 Axios 설정 (JWT 자동 추가)
├── authService.js              인증 API
├── codingTestService.js        코딩 테스트 API
├── chatbotService.js           챗봇 API
├── mypageService.js            마이페이지 API
└── adminService.js             관리자 API
```

**예시** (`codingTestService.js`):
```javascript
import api from './api'

export const getProblems = async (filters) => {
  const response = await api.get('/coding-test/problems/', { params: filters })
  return response.data
}

export const executeCode = async (code, problemId) => {
  const response = await api.post('/coding-test/execute/', { code, problem_id: problemId })
  return response.data
}

export const requestHint = async (problemId, userCode, level) => {
  const response = await api.post('/coding-test/hints/', {
    problem_id: problemId,
    user_code: userCode,
    hint_level: level
  })
  return response.data
}
```

### Redux Store (`frontend/src/store/`)

각 모듈의 상태 관리:
```
store/
├── index.js                    Redux Store 설정
├── authSlice.js                인증 상태
├── codingTestSlice.js          코딩 테스트 상태
└── chatbotSlice.js             챗봇 상태
```

---

## 📋 체크리스트

각 담당자가 확인할 사항:

### 백엔드
- [ ] Django 모델 정의 (`models.py`)
- [ ] API 엔드포인트 구현 (`views.py`)
- [ ] 시리얼라이저 작성 (`serializers.py`)
- [ ] URL 라우팅 (`urls.py`)
- [ ] 비즈니스 로직 (`services/`)
- [ ] 테스트 코드 (`tests.py`)

### 프론트엔드
- [ ] 페이지 레이아웃 (`index.jsx`)
- [ ] 하위 컴포넌트
- [ ] API 서비스 (`services/<모듈>Service.js`)
- [ ] Redux 상태 관리 (`store/<모듈>Slice.js`)
- [ ] 스타일 (`*.module.css`)

---

## 💡 개발 팁

1. **백엔드 먼저 → 프론트엔드**
   - API를 먼저 완성한 후 UI 작업

2. **Mock 데이터 활용**
   - 백엔드 개발 중에는 프론트에서 Mock 데이터 사용

3. **공통 컴포넌트 재사용**
   - `frontend/src/components/` 폴더 활용

4. **권한 체크**
   - 백엔드: `@permission_classes([IsAuthenticated])`
   - 프론트: Redux state의 `user.role` 확인

5. **에러 처리**
   - 백엔드: `common/utils.py`의 `error_response` 사용
   - 프론트: try-catch로 에러 처리

---

## 📚 참고 문서

- **PROJECT_SUMMARY.md** - 프로젝트 전체 요약
- **DEVELOPMENT_GUIDE.md** - 개발 가이드
- **MIGRATION_GUIDE.md** - app.py 마이그레이션
- **DOCKER_SETUP.md** - Docker 실행

각 담당자는 자신의 모듈 폴더에서만 작업하면 됩니다! 🎯
