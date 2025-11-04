# 🚀 빠른 시작 가이드 (Docker 없이)

## 1분 안에 시작하기

### Step 1: 백엔드 실행

터미널에서:

```bash
cd /workspace/proj_hint_system
./start_backend.sh
```

또는 수동으로:

```bash
cd /workspace/proj_hint_system/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### Step 2: 프론트엔드 실행

**새 터미널**을 열고:

```bash
cd /workspace/proj_hint_system
./start_frontend.sh
```

또는 수동으로:

```bash
cd /workspace/proj_hint_system/frontend
npm install
npm run dev
```

### Step 3: 접속

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000/api/v1
- **Django Admin**: http://localhost:8000/admin

---

## 슈퍼유저 생성 (최초 1회)

백엔드 터미널에서 Ctrl+C로 서버를 멈추고:

```bash
cd /workspace/proj_hint_system/backend
source venv/bin/activate
python manage.py createsuperuser

# 다시 서버 시작
python manage.py runserver 0.0.0.0:8000
```

---

## 현재 사용 중인 설정

✅ **데이터베이스**: SQLite (파일: `backend/db.sqlite3`)
- MySQL 설치 불필요
- 별도 설정 불필요
- 개발에 최적

✅ **인증**: JWT 토큰 (설정 완료)

✅ **CORS**: localhost:3000 허용 (설정 완료)

---

## 프로젝트 구조 (핵심)

```
proj_hint_system/
├── backend/                    # Django 백엔드
│   ├── apps/                   # 탭별 앱
│   │   ├── authentication/     # 로그인/회원가입
│   │   ├── coding_test/        # 코딩 테스트
│   │   ├── chatbot/            # 챗봇
│   │   ├── mypage/             # 마이페이지
│   │   └── admin_panel/        # 관리자
│   ├── config/settings.py      # 설정
│   └── manage.py
│
├── frontend/                   # React 프론트엔드
│   ├── src/
│   │   ├── pages/              # 탭별 페이지
│   │   ├── components/         # 공통 컴포넌트
│   │   ├── store/              # Redux
│   │   └── services/           # API
│   └── package.json
│
└── hint-system/                # 기존 시스템 (재사용)
```

---

## 다음 단계

### 1. API 테스트

```bash
# 회원가입
curl -X POST http://localhost:8000/api/v1/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"testpass123!","password_confirm":"testpass123!"}'

# 로그인
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"testpass123!"}'
```

### 2. 각 탭 기능 구현

각 담당자는 자신의 폴더에서 작업:

- **메인 화면**: `frontend/src/pages/MainPage/`
- **코딩 테스트**: `frontend/src/pages/CodingTest/`
- **챗봇**: `frontend/src/pages/Chatbot/`
- **마이페이지**: `frontend/src/pages/MyPage/`
- **관리자**: `frontend/src/pages/AdminPanel/`

### 3. 문제 데이터 로드

Django Admin에서 수동으로 추가하거나, 관리 명령어 작성 (TODO)

---

## 문제 해결

### 포트 충돌

```bash
# 8000 포트 사용 중
lsof -ti:8000 | xargs kill -9

# 3000 포트 사용 중
lsof -ti:3000 | xargs kill -9
```

### 마이그레이션 오류

```bash
cd /workspace/proj_hint_system/backend
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### npm 오류

```bash
cd /workspace/proj_hint_system/frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 참고 문서

- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 전체 개요
- [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) - 개발 가이드
- [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md) - 로컬 개발 상세 가이드

---

**이제 http://localhost:3000 에 접속하여 개발을 시작하세요!** 🎉
