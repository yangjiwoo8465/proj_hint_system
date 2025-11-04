#!/bin/bash

echo "======================================"
echo "  프론트엔드 서버 시작 (React + Vite)"
echo "======================================"

cd /workspace/proj_hint_system/frontend

# node_modules가 없으면 설치
if [ ! -d "node_modules" ]; then
    echo "의존성 설치 중..."
    npm install
fi

echo ""
echo "======================================"
echo "  서버 시작: http://localhost:3000"
echo "======================================"
echo ""

npm run dev
