# 프로젝트 현재 상태

**마지막 업데이트**: 2025-11-04
**상태**: ✅ 구조 완성 / 구현 대기

---

## ✅ 완료된 작업

### 1. 프로젝트 구조 설계 및 생성
- [x] 모듈식 폴더 구조 (각 탭이 독립적인 앱/페이지)
- [x] Backend: Django 5.0 + Django REST Framework
- [x] Frontend: React 18 + Vite + Redux Toolkit
- [x] Database: MySQL 8.0 설정
- [x] Docker Compose 구성 (Nginx, Backend, Frontend, MySQL)

### 2. 백엔드 앱 구성
```
backend/apps/
├── authentication/    ✅ 모델, 뷰, 시리얼라이저, URL 구성 완료
├── coding_test/       ✅ 모델 정의 완료, hint-system 통합 완료
├── chatbot/           ✅ 기본 구조 완료
├── mypage/            ✅ 기본 구조 완료
└── admin_panel/       ✅ 기본 구조 완료
```

### 3. 프론트엔드 페이지 구성
```
frontend/src/pages/
├── MainPage/          ✅ 로그인/회원가입 UI 골격
├── CodingTest/        ✅ 기본 컴포넌트 구조
├── Chatbot/           ✅ 기본 컴포넌트 구조
├── MyPage/            ✅ 기본 컴포넌트 구조
└── AdminPanel/        ✅ 기본 컴포넌트 구조
```

### 4. 공통 유틸리티
- [x] JWT 인증 시스템 (로그인/회원가입 로직)
- [x] 권한 관리 (IsAdminUser, IsOwnerOrAdmin)
- [x] API 응답 포맷 (success_response, error_response)
- [x] 레이팅 계산 로직
- [x] 성향 분석 로직
- [x] ChromaDB 클라이언트 (RAG용)
- [x] Axios 인터셉터 (JWT 자동 갱신)
- [x] Redux 스토어 구성

### 5. hint-system 통합
- [x] `hint-system/models/` → `backend/apps/coding_test/models/`
- [x] `hint-system/data/` → `backend/apps/coding_test/data/`
- [x] 기존 hint-system을 `기타/` 폴더로 백업

### 6. 문서화
- [x] **PROJECT_SUMMARY.md** - 전체 프로젝트 요약
- [x] **DEVELOPMENT_GUIDE.md** - 팀 개발 가이드
- [x] **DOCKER_SETUP.md** - Docker 설치 및 실행
- [x] **MIGRATION_GUIDE.md** - app.py → AdminPanel 마이그레이션
- [x] **MODULE_GUIDE.md** - 각 모듈 상세 설명
- [x] **FINAL_STRUCTURE.md** - 최종 프로젝트 구조
- [x] **NEW_PROJECT_README.md** - 프로젝트 README

---

## ⏳ 구현 대기 중 (각 모듈별 개발자가 담당)

### MainPage (authentication 앱)
- [ ] 로그인 UI 완성
- [ ] 회원가입 폼 유효성 검사
- [ ] 소셜 로그인 추가 (선택)

### CodingTest (coding_test 앱)
- [ ] Monaco Editor 통합
- [ ] 코드 실행 엔진 (`services/code_executor.py`)
- [ ] 힌트 생성 서비스 (`services/hint_generator.py`) - models/ 사용
- [ ] 사용자 성향 분석 (`services/user_analyzer.py`)
- [ ] 문제 데이터 DB 임포트
- [ ] 북마크 기능
- [ ] 제출 이력 표시

### Chatbot (chatbot 앱)
- [ ] ChromaDB에 문서 임베딩 (Python/Git 문서)
- [ ] RAG 기반 답변 생성 (`services/rag_service.py`)
- [ ] 대화 이력 관리
- [ ] 코드 블록 하이라이팅

### MyPage (mypage 앱)
- [ ] 사용자 통계 대시보드
- [ ] 레이팅 그래프
- [ ] 풀이한 문제 목록
- [ ] 북마크한 문제 목록
- [ ] 성향 분석 결과 시각화
- [ ] 프로필 수정

### AdminPanel (admin_panel 앱)
- [ ] 힌트 관리 UI (app.py 기능 이전)
- [ ] 문제별 답안 코드 조회
- [ ] 모델 선택 및 Temperature 설정
- [ ] 여러 모델 힌트 비교
- [ ] 평가 저장 및 통계
- [ ] 모델 설정 관리
- [ ] 사용자 관리

---

## 🚀 실행 방법

### 사전 요구사항
- Docker 및 Docker Compose 설치 필요
- 현재 환경은 컨테이너 내부라서 Docker 실행 불가
- **호스트 머신에서 실행해야 함**

### 호스트 머신에서 실행
```bash
# 1. 프로젝트 디렉토리로 이동
cd /workspace/proj_hint_system

# 2. Docker 확인
docker --version
docker compose version

# 3. 서비스 시작
docker compose up -d --build

# 4. 초기 설정 (최초 1회)
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py collectstatic --noinput

# 5. 접속
# - 프론트엔드: http://localhost:3000
# - 백엔드 API: http://localhost:8000/api/v1
# - Django Admin: http://localhost:8000/admin
```

---

## 📁 프로젝트 구조

```
proj_hint_system/
├── backend/
│   ├── config/                 # Django 설정
│   ├── apps/
│   │   ├── authentication/     # 인증 (MainPage)
│   │   ├── coding_test/        # 코딩 테스트 (hint-system 통합)
│   │   │   ├── models/         # ← hint-system LLM 모델
│   │   │   ├── data/           # ← 문제 데이터
│   │   │   └── services/       # 힌트 생성, 코드 실행
│   │   ├── chatbot/            # 문답 챗봇
│   │   ├── mypage/             # 마이페이지
│   │   └── admin_panel/        # 관리자 (app.py 기능)
│   ├── common/                 # 공통 유틸리티
│   └── vectordb/               # ChromaDB 연동
│
├── frontend/
│   ├── src/
│   │   ├── pages/              # 각 탭별 페이지
│   │   ├── components/         # 공통 컴포넌트
│   │   ├── store/              # Redux
│   │   └── services/           # API 호출
│   └── public/
│
├── nginx/                      # Reverse Proxy
├── docker-compose.yml
├── .env
│
├── 기타/                       # 불필요한 파일들
│   ├── 기존문서/
│   └── hint-system/            # 원본 백업
│
└── 문서/
    ├── PROJECT_SUMMARY.md
    ├── DEVELOPMENT_GUIDE.md
    ├── DOCKER_SETUP.md
    ├── MIGRATION_GUIDE.md
    ├── MODULE_GUIDE.md
    └── FINAL_STRUCTURE.md
```

---

## 👥 팀 개발 가이드

### 병렬 개발 가능
각 개발자는 자신의 모듈 폴더에서 독립적으로 작업 가능:

| 개발자 | Backend 폴더 | Frontend 폴더 |
|--------|-------------|---------------|
| A | `apps/authentication/` | `pages/MainPage/` |
| B | `apps/coding_test/` | `pages/CodingTest/` |
| C | `apps/chatbot/` | `pages/Chatbot/` |
| D | `apps/mypage/` | `pages/MyPage/` |
| E | `apps/admin_panel/` | `pages/AdminPanel/` |

### Git 브랜치 전략
```bash
main                    # 메인 브랜치
├── feature/auth        # 인증 모듈
├── feature/coding      # 코딩 테스트
├── feature/chatbot     # 챗봇
├── feature/mypage      # 마이페이지
└── feature/admin       # 관리자
```

### 공통 유틸리티 사용
- Backend: `backend/common/` 파일들 import
- Frontend: `src/components/`, `src/services/` 사용

---

## 🔐 권한 구분

### 일반 사용자 (role='user')
- ✅ 문제 풀이
- ✅ 힌트 요청 (대/중/소)
- ✅ 챗봇 사용
- ✅ 마이페이지
- ❌ 답안 코드 조회
- ❌ 모델 변경
- ❌ 관리자 패널

### 관리자 (role='admin')
- ✅ 모든 사용자 기능
- ✅ 답안 코드 조회
- ✅ 모델 선택 및 Temperature 설정
- ✅ 힌트 평가 및 비교
- ✅ 사용자 관리
- ✅ 모델 설정

---

## 📊 핵심 기능

### 1. 레이팅 시스템
- 문제 난이도별 기본 점수 (1~5 레벨)
- 풀이 시간 보너스
- 실행 횟수 페널티
- 연속 풀이 보너스

### 2. 성향 분석
- **완벽주의형**: 실행 1회로 정답, 높은 정답률
- **반복형**: 여러 번 실행, 시행착오 학습

### 3. 힌트 시스템
- **대 힌트**: 소크라테스 질문만
- **중 힌트**: 개념 설명 + 질문
- **소 힌트**: 구체적인 코드 힌트
- 성향별 맞춤 힌트

### 4. RAG 챗봇
- Python/Git 문서 기반
- ChromaDB 벡터 검색
- 코드 예제 포함 답변

---

## 🎯 다음 단계

1. **호스트 머신에 Docker 설치** (DOCKER_SETUP.md 참고)
2. **Docker Compose로 전체 서비스 실행**
3. **각 팀원이 자신의 모듈 구현** (MODULE_GUIDE.md 참고)
4. **문제 데이터 DB 로드**
5. **통합 테스트**
6. **프로덕션 배포**

---

## 📚 참고 문서

1. **PROJECT_SUMMARY.md** - 프로젝트 전체 개요 및 기술 스택
2. **DEVELOPMENT_GUIDE.md** - 개발 워크플로우 및 Git 전략
3. **DOCKER_SETUP.md** - Docker 설치 및 실행 가이드
4. **MIGRATION_GUIDE.md** - app.py → AdminPanel 마이그레이션
5. **MODULE_GUIDE.md** - 각 모듈 상세 설명 및 수정 가능 파일
6. **FINAL_STRUCTURE.md** - 최종 폴더 구조

---

**프로젝트 구조는 완성되었습니다! 이제 각 모듈을 구현하면 됩니다.** 🚀
