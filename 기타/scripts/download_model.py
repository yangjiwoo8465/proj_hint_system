#!/usr/bin/env python3
"""
Qwen 2.5 Coder 32B 모델 다운로드 스크립트
- Hugging Face에서 모델 다운로드
- 4-bit quantization 지원
"""

import os
from huggingface_hub import snapshot_download

MODEL_NAME = "Qwen/Qwen2.5-Coder-32B-Instruct"
MODEL_PATH = os.getenv("MODEL_PATH", "/workspace/models/qwen2.5-coder-32b")

def download_model():
    """모델 다운로드"""
    print(f"🔽 Downloading {MODEL_NAME} to {MODEL_PATH}...")

    try:
        snapshot_download(
            repo_id=MODEL_NAME,
            local_dir=MODEL_PATH,
            local_dir_use_symlinks=False,
            resume_download=True,
            # 4-bit quantization을 위해 필요한 파일만 다운로드 (선택사항)
            # allow_patterns=["*.json", "*.safetensors", "*.bin", "*.txt", "*.model"],
        )
        print(f"✅ Model downloaded successfully to {MODEL_PATH}")

        # 다운로드된 파일 목록 확인
        files = os.listdir(MODEL_PATH)
        print(f"\n📁 Downloaded files ({len(files)} total):")
        for f in sorted(files)[:10]:  # 처음 10개만 표시
            print(f"  - {f}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more files")

    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        raise

if __name__ == "__main__":
    # Hugging Face 토큰 확인 (Private 모델인 경우)
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        print("🔑 Using Hugging Face token for authentication")

    # 모델 디렉토리가 이미 존재하고 파일이 있으면 스킵
    if os.path.exists(MODEL_PATH) and len(os.listdir(MODEL_PATH)) > 5:
        print(f"✅ Model already exists at {MODEL_PATH}")
        print("⏭️  Skipping download...")
    else:
        download_model()
