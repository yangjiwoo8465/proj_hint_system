# 설치 및 실행 가이드

## 빠른 시작 (Docker 사용)

### 1. 사전 요구사항

- Docker 및 Docker Compose 설치
- Git

### 2. 프로젝트 클론 및 설정

```bash
# 프로젝트 디렉토리로 이동
cd /workspace/proj_hint_system

# 환경 변수 파일 생성
cp .env.example .env

# .env 파일 편집 (DB 비밀번호 등)
nano .env
```

### 3. Docker로 실행

```bash
# 모든 서비스 빌드 및 시작
docker-compose up -d --build

# 로그 확인
docker-compose logs -f

# 백엔드 마이그레이션 (최초 1회)
docker-compose exec backend python manage.py migrate

# 슈퍼유저 생성 (최초 1회)
docker-compose exec backend python manage.py createsuperuser

# 문제 데이터 로드
docker-compose exec backend python manage.py loaddata problems
```

### 4. 접속

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000/api/v1
- **Django Admin**: http://localhost:8000/admin

### 5. 종료

```bash
# 서비스 중지
docker-compose down

# 볼륨까지 삭제 (데이터 초기화)
docker-compose down -v
```

---

## 로컬 개발 환경 (Docker 없이)

### 1. 백엔드 설정

#### 사전 요구사항
- Python 3.10+
- MySQL 8.0+

#### 설치

```bash
cd backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp ../.env.example .env
# .env 파일 수정 (DB_HOST=localhost 등)

# MySQL 데이터베이스 생성
mysql -u root -p
CREATE DATABASE hint_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'hint_user'@'localhost' IDENTIFIED BY 'your-password';
GRANT ALL PRIVILEGES ON hint_system.* TO 'hint_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# 마이그레이션
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser

# 개발 서버 실행
python manage.py runserver
```

### 2. 프론트엔드 설정

#### 사전 요구사항
- Node.js 18+
- npm

#### 설치

```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정 (선택사항)
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > .env.local

# 개발 서버 실행
npm run dev
```

프론트엔드: http://localhost:3000

---

## 문제 데이터 로드

### 방법 1: Django Admin 사용

1. http://localhost:8000/admin 접속
2. Problems 메뉴에서 수동으로 추가

### 방법 2: 커스텀 관리 명령어 작성

```python
# backend/apps/coding_test/management/commands/import_problems.py
from django.core.management.base import BaseCommand
import json
from apps.coding_test.models import Problem

class Command(BaseCommand):
    help = 'Import problems from JSON file'

    def handle(self, *args, **options):
        json_path = 'hint-system/data/problems_multi_solution_complete.json'

        with open(json_path, 'r', encoding='utf-8') as f:
            problems = json.load(f)

        for problem_data in problems:
            Problem.objects.update_or_create(
                problem_id=problem_data['problem_id'],
                defaults={
                    'title': problem_data['title'],
                    'level': problem_data['level'],
                    'tags': problem_data['tags'],
                    'description': problem_data['description'],
                    'input_description': problem_data['input_description'],
                    'output_description': problem_data['output_description'],
                    'examples': problem_data['examples'],
                    'solutions': problem_data['solutions'],
                    'url': problem_data.get('url', ''),
                    'step_title': problem_data.get('step_title', ''),
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(problems)} problems'))
```

```bash
# 실행
python manage.py import_problems
```

---

## ChromaDB 설정

### 문서 임베딩 추가

```python
# backend/scripts/load_documents.py
from vectordb.chroma_client import get_chroma_client
import os

def load_python_docs():
    """Python 공식 문서 로드"""
    client = get_chroma_client()

    # 여기에 문서 로드 로직 추가
    documents = [
        "Python is a high-level programming language...",
        "List comprehension in Python...",
        # ... more documents
    ]

    ids = [f"doc_{i}" for i in range(len(documents))]
    metadatas = [{"source": "python_docs"} for _ in documents]

    client.add_documents(documents, metadatas, ids)
    client.persist()

    print(f"Loaded {len(documents)} documents")

if __name__ == "__main__":
    load_python_docs()
```

---

## 테스트

### 백엔드 테스트

```bash
cd backend

# 모든 테스트 실행
python manage.py test

# 특정 앱 테스트
python manage.py test apps.coding_test

# 커버리지 확인
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### 프론트엔드 테스트

```bash
cd frontend

# 테스트 실행
npm run test

# 커버리지 확인
npm run test:coverage
```

---

## 프로덕션 배포

### 1. 환경 변수 설정

```bash
# .env 파일 수정
DEBUG=False
DJANGO_SECRET_KEY=<강력한-시크릿-키>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 2. Static 파일 수집

```bash
docker-compose exec backend python manage.py collectstatic --noinput
```

### 3. HTTPS 설정 (Let's Encrypt)

```nginx
# nginx/nginx.conf 수정
server {
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # ... rest of config
}
```

---

## 문제 해결

### 일반적인 문제

#### 1. DB 연결 오류

```bash
# MySQL 서비스 확인
sudo systemctl status mysql

# Docker에서
docker-compose logs db
```

#### 2. 포트 충돌

```bash
# 8000 포트 사용 중인 프로세스 확인
lsof -ti:8000

# 프로세스 종료
kill -9 <PID>
```

#### 3. 마이그레이션 오류

```bash
# 마이그레이션 리셋 (주의: 데이터 손실)
python manage.py migrate --fake <app_name> zero
python manage.py migrate <app_name>
```

#### 4. CORS 오류

`backend/config/settings.py`에서 CORS 설정 확인:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    # 프로덕션 도메인 추가
]
```

---

## 유용한 명령어

### Docker

```bash
# 전체 재빌드
docker-compose up -d --build --force-recreate

# 특정 서비스만 재시작
docker-compose restart backend

# 컨테이너 내부 접속
docker-compose exec backend bash
docker-compose exec frontend sh

# 로그 실시간 확인
docker-compose logs -f backend
```

### Django

```bash
# 셸 실행
python manage.py shell

# 데이터베이스 리셋
python manage.py flush

# 새 앱 생성
python manage.py startapp app_name
```

### npm

```bash
# 빌드 (프로덕션)
npm run build

# 프리뷰
npm run preview

# 린트
npm run lint
```

---

## 모니터링

### 로그 위치

- Backend: `backend/logs/django.log`
- Nginx: Docker 로그 (`docker-compose logs nginx`)

### 성능 모니터링

```bash
# Django Debug Toolbar 설치 (개발 환경)
pip install django-debug-toolbar

# settings.py에 추가
INSTALLED_APPS = [
    ...
    'debug_toolbar',
]
```

---

## 다음 단계

1. ✅ 프로젝트 구조 생성 완료
2. TODO: 각 탭별 상세 기능 구현
3. TODO: 기존 `hint-system/app.py` 기능을 AdminPanel로 이전
4. TODO: 문제 데이터 로드
5. TODO: ChromaDB 문서 임베딩
6. TODO: 프론트엔드 UI/UX 개선

자세한 개발 가이드는 [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md)를 참고하세요.
