#!/bin/bash
set -e

echo "🚀 Starting application on RunPod..."

# 1. 모델 다운로드 (처음 실행 시)
echo "📥 Checking model..."
python3 /app/scripts/download_model.py

# 2. DB 마이그레이션
echo "🗄️  Running database migrations..."
cd /app/backend
python3 manage.py migrate --noinput

# 3. vLLM 서버 시작 (백그라운드)
echo "🤖 Starting vLLM model server..."
python3 -m vllm.entrypoints.openai.api_server \
    --model $MODEL_PATH \
    --host 127.0.0.1 \
    --port 8001 \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.9 \
    --max-model-len 8192 \
    --quantization awq \
    > /var/log/vllm.log 2>&1 &

VLLM_PID=$!
echo "✅ vLLM server started (PID: $VLLM_PID)"

# vLLM 서버 준비 대기 (최대 5분)
echo "⏳ Waiting for vLLM server to be ready..."
for i in {1..60}; do
    if curl -s http://127.0.0.1:8001/health > /dev/null 2>&1; then
        echo "✅ vLLM server is ready!"
        break
    fi
    echo "  Attempt $i/60..."
    sleep 5
done

# 4. Django 서버 시작 (백그라운드)
echo "🌐 Starting Django backend..."
cd /app/backend
gunicorn config.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 4 \
    --timeout 300 \
    --access-logfile /var/log/gunicorn-access.log \
    --error-logfile /var/log/gunicorn-error.log \
    > /var/log/django.log 2>&1 &

DJANGO_PID=$!
echo "✅ Django server started (PID: $DJANGO_PID)"

# 5. Nginx 시작 (foreground)
echo "🔀 Starting Nginx..."
nginx -g "daemon off;" &
NGINX_PID=$!

echo ""
echo "=========================================="
echo "✅ All services started successfully!"
echo "=========================================="
echo "  🤖 vLLM:   PID $VLLM_PID   (Port 8001)"
echo "  🌐 Django: PID $DJANGO_PID (Port 8000)"
echo "  🔀 Nginx:  PID $NGINX_PID  (Port 80)"
echo "=========================================="
echo ""
echo "📊 Logs:"
echo "  - vLLM:    tail -f /var/log/vllm.log"
echo "  - Django:  tail -f /var/log/django.log"
echo "  - Gunicorn: tail -f /var/log/gunicorn-error.log"
echo ""

# 프로세스 모니터링
wait $NGINX_PID
