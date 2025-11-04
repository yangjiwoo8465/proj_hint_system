# 로컬 개발 환경 설정 가이드 (Docker 없이)

## 목차
1. [빠른 시작 (SQLite 사용)](#빠른-시작-sqlite-사용)
2. [MySQL 사용 설정](#mysql-사용-설정)
3. [백엔드 실행](#백엔드-실행)
4. [프론트엔드 실행](#프론트엔드-실행)

---

## 빠른 시작 (SQLite 사용)

Docker 없이 가장 빠르게 시작하는 방법입니다.

### 1. 백엔드 설정 (SQLite)

```bash
cd /workspace/proj_hint_system/backend

# Python 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# SQLite 사용을 위한 설정 변경 (임시)
# settings.py를 수정하거나 아래 명령어로 SQLite DB 생성
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser

# 개발 서버 실행
python manage.py runserver 0.0.0.0:8000
```

**백엔드 접속**: http://localhost:8000

---

### 2. 프론트엔드 설정

새 터미널을 열고:

```bash
cd /workspace/proj_hint_system/frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

**프론트엔드 접속**: http://localhost:3000

---

## 상세 설정

### A. 백엔드 - SQLite 설정 (권장 - 간단)

SQLite는 별도 DB 서버 없이 파일 기반으로 동작합니다.

#### 1) settings.py 수정

```bash
cd /workspace/proj_hint_system/backend
```

`config/settings.py`의 DATABASES 부분을 임시로 수정:

```python
# SQLite로 변경 (개발용)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### 2) 마이그레이션

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 3) 문제 데이터 로드

```bash
# 커스텀 관리 명령어 생성 필요 (아래 참고)
# 또는 Django Admin에서 수동 추가
```

---

### B. 백엔드 - MySQL 설정 (프로덕션)

MySQL을 사용하려면 MySQL 서버가 설치되어 있어야 합니다.

#### 1) MySQL 설치 확인

```bash
mysql --version
```

없으면 설치:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# 설치 후 MySQL 시작
sudo systemctl start mysql
sudo systemctl enable mysql
```

#### 2) 데이터베이스 생성

```bash
sudo mysql -u root -p
```

MySQL 프롬프트에서:

```sql
CREATE DATABASE hint_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'hint_user'@'localhost' IDENTIFIED BY 'your-password';
GRANT ALL PRIVILEGES ON hint_system.* TO 'hint_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 3) .env 파일 수정

```bash
DB_NAME=hint_system
DB_USER=hint_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

#### 4) MySQL 클라이언트 설치

```bash
pip install mysqlclient
```

오류 발생 시:

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

# 다시 설치
pip install mysqlclient
```

#### 5) 마이그레이션

```bash
python manage.py migrate
```

---

## 프론트엔드 설정

### 1) Node.js 확인

```bash
node --version
npm --version
```

없으면 설치:

```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 2) 의존성 설치

```bash
cd /workspace/proj_hint_system/frontend
npm install
```

### 3) 환경 변수 (선택)

```bash
# frontend/.env.local 생성
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > .env.local
```

### 4) 개발 서버 실행

```bash
npm run dev
```

---

## 문제 데이터 로드

### 방법 1: Django Admin 사용

1. http://localhost:8000/admin 접속
2. 슈퍼유저로 로그인
3. Problems 섹션에서 수동 추가

### 방법 2: 관리 명령어 작성

```bash
# 폴더 생성
mkdir -p /workspace/proj_hint_system/backend/apps/coding_test/management/commands
touch /workspace/proj_hint_system/backend/apps/coding_test/management/__init__.py
touch /workspace/proj_hint_system/backend/apps/coding_test/management/commands/__init__.py
```

`apps/coding_test/management/commands/import_problems.py` 파일 생성 (코드는 아래 참고)

실행:

```bash
cd /workspace/proj_hint_system/backend
python manage.py import_problems
```

---

## 실행 요약

### 터미널 1: 백엔드

```bash
cd /workspace/proj_hint_system/backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### 터미널 2: 프론트엔드

```bash
cd /workspace/proj_hint_system/frontend
npm run dev
```

### 접속

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000/api/v1
- **Django Admin**: http://localhost:8000/admin

---

## 문제 해결

### 1. mysqlclient 설치 오류

```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
pip install mysqlclient
```

### 2. 포트 충돌

```bash
# 8000 포트 확인
lsof -ti:8000

# 프로세스 종료
kill -9 <PID>
```

### 3. npm 오류

```bash
# 캐시 삭제
rm -rf node_modules package-lock.json
npm install
```

### 4. ChromaDB 오류

ChromaDB는 선택사항입니다. 챗봇 기능 구현 전까지는 불필요합니다.

임시로 비활성화:

```python
# settings.py에서 주석 처리
# CHROMA_DB_PATH = ...
```

---

## 다음 단계

1. ✅ 백엔드 실행
2. ✅ 프론트엔드 실행
3. ⏳ 각 탭별 기능 구현 시작
4. ⏳ 문제 데이터 로드
5. ⏳ 기존 hint-system 통합

상세한 개발 가이드는 [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)를 참고하세요.
