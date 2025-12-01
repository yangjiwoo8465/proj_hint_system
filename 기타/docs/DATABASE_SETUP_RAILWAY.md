# Railway MySQL 설정 가이드

## 1. Railway에서 MySQL 프로젝트 생성

### 1.1 회원가입 및 로그인
1. https://railway.app 접속
2. GitHub 계정으로 로그인
3. 무료 플랜: $5 크레딧 제공 (월 500시간 사용 가능)

### 1.2 MySQL 서비스 생성
```bash
# Railway CLI 설치 (선택사항)
npm install -g @railway/cli

# 로그인
railway login

# 새 프로젝트 생성
railway init

# MySQL 추가
railway add --plugin mysql
```

**또는 웹 UI에서:**
1. "New Project" 클릭
2. "Deploy MySQL" 선택
3. 자동 생성 완료

### 1.3 연결 정보 확인

Railway 대시보드에서 MySQL 서비스 클릭 → Variables 탭:

```
MYSQL_URL=mysql://root:PASSWORD@containers-us-west-XXX.railway.app:6379/railway
MYSQL_HOST=containers-us-west-XXX.railway.app
MYSQL_PORT=6379
MYSQL_USER=root
MYSQL_PASSWORD=XXXXXXXXXXXXX
MYSQL_DATABASE=railway
```

---

## 2. Django 설정 수정

### 2.1 backend/config/settings.py 수정

```python
import os
from urllib.parse import urlparse

# Railway MySQL 연결 정보
RAILWAY_MYSQL_URL = os.getenv('MYSQL_URL', '')

if RAILWAY_MYSQL_URL:
    # Railway MySQL URL 파싱
    parsed = urlparse(RAILWAY_MYSQL_URL)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': parsed.path[1:],  # '/railway' -> 'railway'
            'USER': parsed.username,
            'PASSWORD': parsed.password,
            'HOST': parsed.hostname,
            'PORT': parsed.port or 3306,
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    # 로컬 개발 환경 (기존 설정)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'mydb'),
            'USER': os.getenv('DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'yourpassword'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3307'),
            'OPTIONS': {'charset': 'utf8mb4'},
        }
    }
```

---

## 3. RunPod 환경변수 설정

RunPod Pod 생성 시 Environment Variables에 추가:

```bash
MYSQL_URL=mysql://root:YOUR_PASSWORD@containers-us-west-XXX.railway.app:6379/railway
DJANGO_SETTINGS_MODULE=config.settings
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*.runpod.io,your-domain.com
```

---

## 4. 마이그레이션 실행

### 로컬에서 테스트

```bash
cd backend

# Railway MySQL URL 설정
export MYSQL_URL="mysql://root:PASSWORD@containers-us-west-XXX.railway.app:6379/railway"

# 마이그레이션
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser
```

### RunPod에서 자동 실행

`start_runpod.sh` 스크립트에 이미 포함됨:
```bash
python3 manage.py migrate --noinput
```

---

## 5. 비용 및 성능

### Railway MySQL 요금

| 플랜 | CPU | RAM | Storage | 비용 |
|------|-----|-----|---------|------|
| Free | Shared | 512MB | 1GB | $0 (월 $5 크레딧) |
| Developer | 2 vCPU | 8GB | 10GB | $10/월 |
| Team | 4 vCPU | 16GB | 20GB | $20/월 |

**추천**: Developer 플랜 ($10/월) - 충분한 성능

### 예상 총 비용

| 항목 | 비용 |
|------|------|
| RunPod A6000 GPU | ~$570/월 |
| Railway MySQL (Developer) | $10/월 |
| **총 비용** | **~$580/월** |

---

## 6. 백업 및 복원

### 데이터베이스 백업

```bash
# Railway CLI로 백업
railway run mysqldump railway > backup.sql

# 또는 직접 mysqldump
mysqldump -h containers-us-west-XXX.railway.app \
  -P 6379 \
  -u root \
  -p railway > backup.sql
```

### 복원

```bash
mysql -h containers-us-west-XXX.railway.app \
  -P 6379 \
  -u root \
  -p railway < backup.sql
```

---

## 7. 문제 해결

### Q1: "Access denied for user" 에러

**원인**: 비밀번호 또는 호스트 오류

**해결**:
1. Railway 대시보드에서 MYSQL_PASSWORD 재확인
2. 환경변수 정확히 복사 (공백 주의)

### Q2: "Too many connections" 에러

**원인**: Django connection pool 설정

**해결**:
```python
# settings.py
DATABASES['default']['OPTIONS']['max_connections'] = 20
```

### Q3: 마이그레이션 실패

**원인**: 네트워크 또는 권한 문제

**해결**:
```bash
# Railway MySQL 접속 테스트
mysql -h HOST -P PORT -u root -p

# 연결 확인 후 Django 테스트
python manage.py dbshell
```

---

**작성일**: 2025-01-30
**테스트 완료**: Railway MySQL + Django 연동 확인
