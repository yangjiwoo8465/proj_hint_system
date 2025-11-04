#!/bin/bash
# =================================================================
# Runpod 환경에서 힌트 시스템 실행 스크립트
# Ubuntu 22.04, Python 3.10, CUDA 11.8
# =================================================================

echo "================================================"
echo "백준 힌트 생성 시스템 - Runpod 실행"
echo "================================================"

# 1. 시스템 정보 출력
echo ""
echo "[INFO] 시스템 정보:"
echo "  - OS: $(lsb_release -d | cut -f2-)"
echo "  - Python: $(python3 --version)"
echo "  - CUDA: $(nvcc --version | grep release | awk '{print $5,$6}')"
echo "  - GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader)"
echo "  - VRAM: $(nvidia-smi --query-gpu=memory.total --format=csv,noheader)"
echo ""

# 2. 작업 디렉토리 확인
PROJECT_DIR="/workspace/5th-project_mvp/hint-system"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "[ERROR] 프로젝트 디렉토리가 없습니다: $PROJECT_DIR"
    echo "[TIP] 먼저 프로젝트를 복사하세요:"
    echo "  git clone <repository> /workspace/5th-project_mvp"
    exit 1
fi

cd "$PROJECT_DIR"
echo "[INFO] 작업 디렉토리: $(pwd)"
echo ""

# 3. Python 패키지 설치 확인
echo "[INFO] Python 패키지 확인 중..."
if [ ! -f "requirements.txt" ]; then
    echo "[ERROR] requirements.txt 파일이 없습니다"
    exit 1
fi

# 패키지 설치 (없으면)
pip list | grep -q gradio
if [ $? -ne 0 ]; then
    echo "[INSTALL] 패키지 설치 중... (최초 1회, 2~3분 소요)"
    pip install -r requirements.txt
else
    echo "[OK] 패키지 이미 설치됨"
fi
echo ""

# 4. 환경 변수 설정
echo "[INFO] 환경 변수 설정 중..."

# .env 파일이 있으면 로드
if [ -f "../.env" ]; then
    echo "[OK] .env 파일 발견, 로드 중..."
    export $(grep -v '^#' ../.env | xargs)
else
    echo "[WARN] .env 파일이 없습니다. 기본값 사용"
    export PROJECT_ROOT="/workspace/5th-project_mvp"
fi

# CUDA 메모리 최적화
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

echo ""

# 5. Gradio 공개 링크 설정
echo "[INFO] Gradio 설정 중..."
echo "  - 포트: 7860"
echo "  - 공개 링크: 활성화"
echo ""

# 6. 앱 실행
echo "================================================"
echo "앱 시작 중... (모델 로딩 1~2분 소요)"
echo "================================================"
echo ""

python3 app.py

# 종료 시
echo ""
echo "================================================"
echo "앱 종료됨"
echo "================================================"
