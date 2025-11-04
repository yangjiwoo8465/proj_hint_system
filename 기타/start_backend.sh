#!/bin/bash

echo "======================================"
echo "  백엔드 서버 시작 (SQLite)"
echo "======================================"

cd /workspace/proj_hint_system/backend

# 가상환경이 없으면 생성
if [ ! -d "venv" ]; then
    echo "가상환경 생성 중..."
    python3 -m venv venv
fi

# 가상환경 활성화
echo "가상환경 활성화..."
source venv/bin/activate

# 의존성 설치 (requirements.txt가 변경되었을 수 있으므로)
echo "의존성 확인 중..."
pip install -q -r requirements.txt 2>/dev/null || echo "의존성 설치 건너뛰기 (이미 설치됨)"

# 마이그레이션
echo "데이터베이스 마이그레이션..."
python manage.py makemigrations 2>/dev/null
python manage.py migrate

# 슈퍼유저 존재 확인
echo ""
echo "슈퍼유저가 없으면 생성하세요:"
echo "  python manage.py createsuperuser"
echo ""

# 서버 실행
echo "======================================"
echo "  서버 시작: http://localhost:8000"
echo "  Admin: http://localhost:8000/admin"
echo "======================================"
echo ""

python manage.py runserver 0.0.0.0:8000
