# 🎯 AI 기반 코딩 학습 플랫폼 (Hint System)

> Django + React 기반의 지능형 힌트 제공 시스템으로 초보자부터 중급자까지 단계적 학습 지원

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)

---

## 📋 프로젝트 소개

AI를 활용한 지능형 힌트 제공 시스템을 갖춘 코딩 학습 플랫폼입니다. 학습자의 코드를 실시간으로 분석하고, 소크라틱 질문과 맞춤형 힌트를 제공하여 효과적인 문제 해결을 돕습니다.

### ✨ 주요 기능

#### 1. 지능형 힌트 시스템
- **3단계 힌트**: 소크라틱 질문 → 개념 설명 → 코드 힌트
- **AI 기반 분석**: 코드 유사도, 구문 오류, 로직 오류 자동 감지
- **맞춤형 피드백**: 사용자 수준에 맞는 단계별 힌트 제공
- **12가지 지표 분석**: 정적 6개 + LLM 기반 6개 지표

#### 2. 다중 AI 모델 지원
- **API 방식**: Hugging Face API (Qwen2.5-Coder-7B)
- **로컬 방식**: Ollama 로컬 모델 (오프라인 가능)
- **Runpod vLLM 방식**: 클라우드 GPU에서 대형 모델 (Qwen2.5-Coder-32B) 실행

#### 3. 학습 관리
- **진도 추적**: 문제 해결 상태 관리 (solved/upgrade/upgrading)
- **배지 시스템**: 학습 성취도에 따른 배지 획득
- **로드맵**: AI 기반 맞춤형 학습 경로 생성
- **통계 대시보드**: 학습 기록 및 성취도 시각화

#### 4. 커뮤니티 기능
- **테스트 케이스 제안**: 사용자가 새로운 테스트 케이스 제안 가능
- **솔루션 제안**: 다양한 풀이 방법 공유
- **문제 제안**: 새로운 문제 추가 제안
- **관리자 승인 시스템**: 품질 관리 프로세스

#### 5. 실시간 코드 에디터
- **Monaco Editor**: VS Code와 동일한 에디터
- **실시간 코드 실행**: 예제 입력 자동 테스트
- **커스텀 입력**: 사용자 정의 테스트 케이스
- **제출 시스템**: 숨겨진 테스트 케이스로 채점

---

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                      │
│  - Monaco Editor  - Redux Store  - Material UI           │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/REST API
┌──────────────────────┴──────────────────────────────────┐
│                  Backend (Django REST)                    │
│  - Authentication  - Code Execution  - Hint Generation    │
└──────────────────────┬──────────────────────────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
┌───┴────┐      ┌──────┴──────┐    ┌─────┴─────┐
│ MySQL  │      │  AI Models  │    │  Docker   │
│   DB   │      │  (3 types)  │    │ Container │
└────────┘      └──────┬──────┘    └───────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────┴────┐   ┌─────┴─────┐  ┌────┴────┐
   │Hugging  │   │  Ollama   │  │ Runpod  │
   │Face API │   │  Local    │  │  vLLM   │
   └─────────┘   └───────────┘  └─────────┘
```

---

## 🛠️ 기술 스택

### Frontend
- **React 18**: UI 프레임워크
- **Vite**: 빌드 도구 (HMR 지원)
- **Redux Toolkit**: 상태 관리
- **Axios**: HTTP 클라이언트
- **Monaco Editor**: VS Code 기반 코드 에디터

### Backend
- **Django 5.1**: 웹 프레임워크
- **Django REST Framework**: RESTful API 서버
- **MySQL 8.0**: 관계형 데이터베이스
- **Gunicorn**: WSGI HTTP 서버
- **Docker**: 컨테이너화

### AI/ML
- **vLLM 0.6.4+**: 고성능 LLM 추론 엔진
- **Transformers**: Hugging Face 라이브러리
- **OpenAI SDK**: vLLM API 클라이언트
- **Qwen2.5-Coder**: Alibaba의 코드 특화 LLM

### Infrastructure
- **Docker & Docker Compose**: 컨테이너 오케스트레이션
- **Nginx**: Reverse Proxy (프로덕션)
- **Runpod**: 클라우드 GPU 플랫폼

---

## 🚀 빠른 시작

### 사전 요구사항

**필수**:
- **Docker**: 20.10+ ([설치 가이드](https://docs.docker.com/get-docker/))
- **Docker Compose**: 2.0+
- **Node.js**: 18+ ([다운로드](https://nodejs.org/))
- **npm**: 9+
- **Git**: 최신 버전

**선택사항** (AI 모델):
- Hugging Face API 키 (API 방식)
- Ollama 설치 (로컬 방식)
- Runpod 계정 (vLLM 방식)

---

### 설치 및 실행

#### 1단계: 프로젝트 클론

```bash
git clone https://github.com/yangjiwoo8465/proj_hint_system.git
cd proj_hint_system/5th-project_mvp
```

#### 2단계: 환경 변수 설정

`.env.example`을 복사하여 `.env` 생성:

```bash
cp .env.example .env
```

`.env` 파일 수정:

```env
# Django 설정
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 데이터베이스
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=hint_system_db
MYSQL_USER=hint_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=db
MYSQL_PORT=3306

# Hugging Face API (선택사항)
HUGGINGFACE_API_KEY=hf_your_api_key_here
```

#### 3단계: Backend 실행

Docker Compose로 백엔드 및 데이터베이스 실행:

```bash
docker-compose up -d
```

초기 설정:

```bash
# 데이터베이스 마이그레이션
docker exec -it hint_system_backend python manage.py migrate

# 관리자 계정 생성
docker exec -it hint_system_backend python manage.py createsuperuser

# 정적 파일 수집
docker exec -it hint_system_backend python manage.py collectstatic --noinput
```

#### 4단계: Frontend 실행

```bash
cd frontend
npm install
npm run dev
```

#### 5단계: 서비스 접속

- **메인 페이지**: http://localhost:3000
- **관리자 패널**: http://localhost:3000/app/admin
- **Backend API**: http://localhost:8000/api/v1/
- **Django Admin**: http://localhost:8000/admin

---

## 🤖 AI 모델 설정

프로젝트는 3가지 AI 모델 연동 방식을 지원합니다. 관리자 패널(http://localhost:3000/app/admin)의 **Models** 탭에서 설정할 수 있습니다.

### 방식 1: Hugging Face API (추천 - 초보자)

**장점**:
- ✅ 설치 불필요
- ✅ 빠른 시작
- ✅ 안정적인 성능

**단점**:
- ❌ API 호출 비용
- ❌ 인터넷 연결 필수

**설정 방법**:

1. [Hugging Face](https://huggingface.co/) 계정 생성
2. API 토큰 발급: https://huggingface.co/settings/tokens
3. `.env`에 토큰 추가:
   ```env
   HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx
   ```
4. 관리자 패널에서 설정:
   - AI 모델 방식: **API 방식 (Hugging Face)**
   - API Key 입력
   - 모델명: `Qwen/Qwen2.5-Coder-7B-Instruct`
   - **설정 저장** 클릭

---

### 방식 2: Ollama Local (오프라인)

**장점**:
- ✅ 완전 무료
- ✅ 오프라인 사용 가능
- ✅ 데이터 프라이버시

**단점**:
- ❌ 로컬 GPU/CPU 리소스 사용
- ❌ 설치 및 설정 필요
- ❌ 모델 크기에 따른 디스크 공간 필요

**설정 방법**:

1. **Ollama 설치**: https://ollama.ai/download

2. **모델 다운로드**:
   ```bash
   ollama pull qwen2.5-coder:7b
   ```

3. **Ollama 서버 실행**:
   ```bash
   ollama serve
   ```
   기본적으로 `http://localhost:11434`에서 실행됩니다.

4. **관리자 패널에서 설정**:
   - AI 모델 방식: **로컬 로드 방식**
   - 모델명: `qwen2.5-coder:7b`
   - **모델 로드** 버튼 클릭
   - **설정 저장** 클릭

**문제 해결**:
- Ollama가 실행 중인지 확인: `ollama list`
- 포트 확인: `curl http://localhost:11434/api/tags`

---

### 방식 3: Runpod vLLM (최고 성능)

**장점**:
- ✅ 최고 성능 (32B 모델)
- ✅ GPU 리소스 걱정 없음
- ✅ 확장 가능

**단점**:
- ❌ 비용 발생 (시간당 과금)
- ❌ 복잡한 설정
- ❌ 인터넷 연결 필수

**상세 가이드**: [Runpod vLLM 설정 가이드](./runpod_vllm/README.md) 참조

**요약**:

1. **Runpod Pod 생성**:
   - GPU: A100 80GB 이상
   - Template: `madiator2011/better-pytorch:cuda12.4-torch2.6.0`
   - Expose Port: 8000

2. **vLLM 서버 설치**:
   ```bash
   cd /workspace
   # runpod_vllm/ 폴더의 파일들을 Runpod으로 복사
   chmod +x start_vllm.sh
   pip install -r requirements.txt
   nohup ./start_vllm.sh > vllm_server.log 2>&1 &
   ```

3. **관리자 패널에서 설정**:
   - AI 모델 방식: **Runpod vLLM 방식**
   - Runpod Endpoint URL: `https://[your-pod-id]-8000.proxy.runpod.net`
   - Runpod API Key: 비워두기 (vLLM은 인증 불필요)
   - 모델명: `Qwen/Qwen2.5-Coder-32B-Instruct`
   - **설정 저장** 클릭

4. **연결 테스트**:
   ```bash
   curl https://[your-pod-id]-8000.proxy.runpod.net/v1/models
   ```

**자세한 내용은 [runpod_vllm/README.md](./runpod_vllm/README.md)를 참조하세요.**

---

## 📁 프로젝트 구조

```
5th-project_mvp/
├── backend/                    # Django 백엔드
│   ├── apps/
│   │   ├── accounts/           # 사용자 인증 (JWT)
│   │   ├── admin_panel/        # 관리자 패널
│   │   ├── coding_test/        # 코딩 테스트 핵심 로직
│   │   │   ├── models.py       # DB 모델 (Problem, HintMetrics 등)
│   │   │   ├── views.py        # API 뷰
│   │   │   ├── hint_api.py     # AI 힌트 생성 로직
│   │   │   ├── code_analyzer.py # 코드 분석 (12가지 지표)
│   │   │   ├── badge_logic.py  # 배지 시스템
│   │   │   └── roadmap_api.py  # 로드맵 생성
│   │   └── chatbot/            # RAG 챗봇
│   ├── config/                 # Django 설정
│   │   ├── settings.py
│   │   └── urls.py
│   ├── requirements.txt        # Python 의존성
│   └── manage.py
│
├── frontend/                   # React 프론트엔드
│   ├── src/
│   │   ├── components/         # 공통 컴포넌트
│   │   ├── pages/              # 페이지 컴포넌트
│   │   │   ├── MainPage/       # 메인 페이지
│   │   │   ├── Login/          # 로그인
│   │   │   ├── Signup/         # 회원가입
│   │   │   ├── Problems/       # 문제 목록
│   │   │   ├── CodingTest/     # 코딩 테스트
│   │   │   ├── MyPage/         # 마이페이지
│   │   │   ├── AdminPanel/     # 관리자 패널
│   │   │   │   └── tabs/       # 탭 컴포넌트들
│   │   │   ├── Chatbot/        # 챗봇
│   │   │   ├── Roadmap/        # 로드맵
│   │   │   └── Survey/         # 설문조사
│   │   ├── services/           # API 서비스
│   │   │   └── api.js          # Axios 인스턴스
│   │   ├── store/              # Redux 스토어
│   │   │   └── authSlice.js    # 인증 상태 관리
│   │   ├── App.jsx             # 메인 앱 컴포넌트
│   │   └── main.jsx            # 진입점
│   ├── package.json            # npm 의존성
│   ├── vite.config.js          # Vite 설정
│   └── index.html
│
├── runpod_vllm/                # Runpod vLLM 설정 파일
│   ├── start_vllm.sh           # vLLM 서버 시작 스크립트
│   ├── test_connection.py      # 연결 테스트 스크립트
│   ├── requirements.txt        # Python 의존성 (vLLM)
│   └── README.md               # Runpod 설정 가이드
│
├── nginx/                      # Nginx 설정 (프로덕션)
│   └── nginx.conf
│
├── 기타/                       # 문서 및 스크립트
│   ├── docs/                   # 개발 문서
│   ├── scripts/                # 유틸리티 스크립트
│   └── hint-system/            # 구버전 파일
│
├── docker-compose.yml          # Docker 컨테이너 구성
├── .env.example                # 환경 변수 예시
├── .gitignore                  # Git 무시 파일
└── README.md                   # 이 파일
```

---

## 🔑 주요 API 엔드포인트

### 인증 (`/api/v1/accounts/`)
- `POST /register/` - 회원가입
- `POST /login/` - 로그인
- `POST /logout/` - 로그아웃
- `POST /verify-email/` - 이메일 인증
- `GET /profile/` - 프로필 조회

### 문제 (`/api/v1/coding-test/problems/`)
- `GET /` - 문제 목록
- `GET /{id}/` - 문제 상세
- `POST /propose/` - 문제 제안

### 코드 실행 (`/api/v1/coding-test/`)
- `POST /execute/` - 코드 실행 (예제 테스트)
- `POST /submit/` - 코드 제출 (채점)

### 힌트 (`/api/v1/coding-test/`)
- `POST /hints/` - 힌트 요청

### 테스트 케이스 (`/api/v1/coding-test/test-cases/`)
- `POST /propose/` - 테스트 케이스 제안
- `GET /` - 제안 목록
- `GET /{problem_id}/approved/` - 승인된 테스트 케이스
- `POST /{id}/approve/` - 승인 (관리자)
- `POST /{id}/reject/` - 거부 (관리자)

### 솔루션 (`/api/v1/coding-test/solutions/`)
- `POST /propose/` - 솔루션 제안
- `GET /` - 제안 목록
- `POST /{id}/approve/` - 승인 (관리자)
- `POST /{id}/reject/` - 거부 (관리자)

### AI 설정 (`/api/v1/coding-test/ai-config/`) - 관리자만
- `GET /` - AI 설정 조회
- `POST /update/` - AI 설정 업데이트
- `POST /load-model/` - 로컬 모델 로드
- `POST /unload-model/` - 로컬 모델 언로드

### 로드맵 (`/api/v1/coding-test/`)
- `POST /survey/` - 설문조사 제출
- `GET /roadmap/` - 로드맵 조회
- `GET /roadmaps/` - 로드맵 목록
- `POST /roadmaps/{id}/activate/` - 로드맵 활성화

### 배지 (`/api/v1/coding-test/`)
- `GET /badges/` - 모든 배지 목록
- `GET /user-badges/` - 사용자 획득 배지

---

## 🎓 학습 시스템

### 힌트 레벨

프로젝트는 3단계 힌트 시스템을 제공합니다:

1. **소크라틱 질문** (Level 1):
   - 스스로 생각하도록 유도하는 질문
   - 예: "이 문제에서 무엇을 입력받아야 할까요?"

2. **개념 설명** (Level 2):
   - 문제 해결에 필요한 개념 설명
   - 예: "등차수열의 합 공식: n * (n+1) / 2"

3. **코드 힌트** (Level 3):
   - 구체적인 코드 패턴 제시
   - 예: `n = int(input())`

### 코드 분석 지표 (12가지)

#### 정적 분석 (6개)
1. **syntax_errors**: 구문 오류 개수
2. **test_pass_rate**: 테스트 통과율 (%)
3. **code_complexity**: 순환 복잡도 (McCabe)
4. **code_quality_score**: 코드 품질 점수 (0-100)
5. **algorithm_pattern_match**: 알고리즘 패턴 일치도 (%)
6. **pep8_violations**: PEP8 위반 개수

#### LLM 기반 분석 (6개)
7. **algorithm_efficiency**: 알고리즘 효율성 (1-5)
8. **code_readability**: 코드 가독성 (1-5)
9. **design_pattern_fit**: 설계 패턴 적합도 (1-5)
10. **edge_case_handling**: 엣지 케이스 처리 (1-5)
11. **code_conciseness**: 코드 간결성 (1-5)
12. **function_separation**: 함수 분리도 (1-5)

### 배지 시스템

사용자의 학습 성취도에 따라 자동으로 배지를 획득합니다:

- 🥉 **첫 걸음**: 첫 문제 해결
- 🥈 **10제 돌파**: 10개 문제 해결
- 🥇 **50제 마스터**: 50개 문제 해결
- 🏆 **완벽주의자**: 10개 문제를 1-2회 실행으로 해결
- 🔥 **열정**: 7일 연속 문제 풀이
- ⚡ **스피드**: 5개 문제를 평균 시간 이하로 해결

---

## 🔧 개발 가이드

### Backend 개발

#### 로컬 개발 환경 (가상환경)

```bash
cd backend
python -m venv venv

# 가상환경 활성화
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

#### 마이그레이션

```bash
# 마이그레이션 파일 생성
docker exec -it hint_system_backend python manage.py makemigrations

# 마이그레이션 적용
docker exec -it hint_system_backend python manage.py migrate

# 특정 앱만 마이그레이션
docker exec -it hint_system_backend python manage.py makemigrations coding_test
```

#### 테스트

```bash
# 전체 테스트
docker exec -it hint_system_backend python manage.py test

# 특정 앱 테스트
docker exec -it hint_system_backend python manage.py test apps.coding_test

# 커버리지 포함
docker exec -it hint_system_backend coverage run --source='.' manage.py test
docker exec -it hint_system_backend coverage report
```

---

### Frontend 개발

#### 개발 서버

```bash
cd frontend
npm run dev
```

Hot Module Replacement (HMR)가 활성화되어 코드 변경 시 자동으로 반영됩니다.

#### 빌드

```bash
# 프로덕션 빌드
npm run build

# 빌드 결과 미리보기
npm run preview
```

#### 린트 및 포맷

```bash
# ESLint 실행
npm run lint

# 자동 수정
npm run lint:fix
```

---

## 🐛 문제 해결

### Docker 관련

**컨테이너가 시작되지 않음**:
```bash
docker-compose down
docker-compose up -d --force-recreate
```

**포트 충돌**:
```bash
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Mac/Linux
lsof -i :8000
lsof -i :3000

# docker-compose.yml에서 포트 변경
```

**볼륨 초기화**:
```bash
docker-compose down -v
docker volume prune
docker-compose up -d
```

---

### Database 관련

**마이그레이션 오류**:
```bash
# Fake 마이그레이션 (주의: 데이터 손실 가능)
docker exec -it hint_system_backend python manage.py migrate --fake

# 특정 앱 초기화
docker exec -it hint_system_backend python manage.py migrate coding_test zero
docker exec -it hint_system_backend python manage.py migrate coding_test
```

**데이터베이스 접속**:
```bash
docker exec -it hint_system_db mysql -u hint_user -p
# password: .env의 MYSQL_PASSWORD
```

**데이터베이스 백업**:
```bash
docker exec hint_system_db mysqldump -u hint_user -p hint_system_db > backup.sql
```

---

### Frontend 관련

**모듈을 찾을 수 없음**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**프록시 오류**:
- `vite.config.js`에서 프록시 설정 확인
- Backend 서버가 `http://localhost:8000`에서 실행 중인지 확인

**빌드 오류**:
```bash
# 캐시 삭제
rm -rf .vite node_modules/.vite
npm run build
```

---

### AI 모델 관련

**Hugging Face API 오류**:
- API 키 확인: `.env`의 `HUGGINGFACE_API_KEY`
- API 할당량 확인: https://huggingface.co/settings/tokens
- 네트워크 연결 확인

**Ollama 연결 실패**:
```bash
# Ollama 서비스 상태 확인
ollama list

# 재시작
ollama serve

# 포트 확인
curl http://localhost:11434/api/tags
```

**Runpod vLLM 오류**:
- Endpoint URL 확인
- Pod가 실행 중인지 Runpod 대시보드에서 확인
- 로그 확인: `cat vllm_server.log`

---

## 📊 모니터링 및 로그

### Backend 로그

```bash
# 실시간 로그
docker logs -f hint_system_backend

# 최근 100줄
docker logs --tail 100 hint_system_backend

# 특정 시간대 로그
docker logs --since 2024-01-01T00:00:00 hint_system_backend
```

### Frontend 로그

Vite 개발 서버가 자동으로 콘솔에 로그를 출력합니다.

### Database 로그

```bash
docker logs -f hint_system_db
```

### Performance Monitoring

```bash
# 컨테이너 리소스 사용량
docker stats

# 특정 컨테이너
docker stats hint_system_backend hint_system_db
```

---

## 🚢 배포

### 프로덕션 환경 설정

#### 1. 환경 변수 업데이트

`.env` 파일:
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=production-secret-key-here

# HTTPS 설정
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

#### 2. Frontend 빌드

```bash
cd frontend
npm run build
```

빌드 결과는 `frontend/dist/` 폴더에 생성됩니다.

#### 3. Nginx 설정

`docker-compose.yml`에서 nginx 서비스 주석 해제:

```yaml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    - ./frontend/dist:/usr/share/nginx/html
    - ./certbot/conf:/etc/letsencrypt
```

#### 4. SSL 인증서 (Let's Encrypt)

```bash
# Certbot 설치
sudo apt-get install certbot python3-certbot-nginx

# 인증서 발급
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

#### 5. 실행

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🤝 기여 가이드

프로젝트에 기여해주셔서 감사합니다!

### 기여 절차

1. **Fork** the Project
2. **Create** your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your Changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the Branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### 코드 스타일

- **Python**: PEP 8
- **JavaScript**: ESLint + Prettier
- **커밋 메시지**: Conventional Commits

```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 추가
chore: 빌드 작업, 패키지 매니저 설정
```

### Pull Request 가이드

- 명확한 제목과 설명 작성
- 관련 Issue 번호 포함
- 스크린샷 추가 (UI 변경 시)
- 테스트 통과 확인

---

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

## 👥 팀

- **프로젝트 리더**: 양지우
- **GitHub**: [@yangjiwoo8465](https://github.com/yangjiwoo8465)

---

## 📧 연락처

- **Email**: yangjiwoo8465@gmail.com
- **GitHub Repository**: https://github.com/yangjiwoo8465/proj_hint_system
- **Issues**: https://github.com/yangjiwoo8465/proj_hint_system/issues

---

## 🔗 참고 자료

### 공식 문서
- [Django 공식 문서](https://docs.djangoproject.com/)
- [React 공식 문서](https://react.dev/)
- [vLLM 문서](https://docs.vllm.ai/)
- [Docker 문서](https://docs.docker.com/)

### AI 모델
- [Qwen2.5-Coder 모델 카드](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct)
- [Ollama 공식 사이트](https://ollama.ai/)
- [Runpod 문서](https://docs.runpod.io/)

### 추가 가이드
- [Runpod vLLM 설정 가이드](./runpod_vllm/README.md)
- [기타 문서](./기타/docs/)

---

## 📈 버전 히스토리

### v1.0.0 (2025-01-XX) - 현재
- ✅ 3단계 힌트 시스템
- ✅ 다중 AI 모델 지원 (API/Local/Runpod)
- ✅ 12가지 코드 분석 지표
- ✅ 배지 및 로드맵 시스템
- ✅ 커뮤니티 기능 (테스트 케이스/솔루션/문제 제안)
- ✅ 관리자 패널 (모델 관리, 메트릭 검증)

### v0.9.0 (2024-12-XX)
- Beta 릴리스
- 코어 기능 구현
- Docker 컨테이너화

---

## 🙏 감사의 글

이 프로젝트는 다음 오픈소스 프로젝트들을 사용합니다:

- [Django](https://www.djangoproject.com/)
- [React](https://react.dev/)
- [vLLM](https://github.com/vllm-project/vllm)
- [Monaco Editor](https://microsoft.github.io/monaco-editor/)
- [Qwen2.5-Coder by Alibaba](https://github.com/QwenLM/Qwen2.5-Coder)

---

**Happy Coding! 🚀**
