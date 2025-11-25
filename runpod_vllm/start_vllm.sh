#!/bin/bash

# Runpod Workspace에서 vLLM으로 Qwen 2.5 Coder 32B 모델 실행하는 스크립트

echo "========================================="
echo "Starting vLLM Server with Qwen 2.5 Coder 32B"
echo "========================================="

# 환경 변수 설정
export CUDA_VISIBLE_DEVICES=0
export MODEL_NAME="Qwen/Qwen2.5-Coder-32B-Instruct"
export PORT=8000
export MAX_MODEL_LEN=8192
export GPU_MEMORY_UTILIZATION=0.95

echo "Model: $MODEL_NAME"
echo "Port: $PORT"
echo "Max Model Length: $MAX_MODEL_LEN"
echo "GPU Memory Utilization: $GPU_MEMORY_UTILIZATION"

# vLLM 서버 시작
python -m vllm.entrypoints.openai.api_server \
    --model $MODEL_NAME \
    --port $PORT \
    --max-model-len $MAX_MODEL_LEN \
    --gpu-memory-utilization $GPU_MEMORY_UTILIZATION \
    --tensor-parallel-size 1 \
    --dtype auto \
    --trust-remote-code \
    --served-model-name "Qwen/Qwen2.5-Coder-32B-Instruct"

echo "vLLM server stopped"
