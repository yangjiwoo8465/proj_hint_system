"""
로컬 환경에서 테스트할 가벼운 모델 설정
"""

# 로컬 환경용 가벼운 모델들 (CPU/낮은 GPU 사양)
LOCAL_MODELS = {
    "qwen-1.5b": {
        "name": "Qwen/Qwen2.5-Coder-1.5B-Instruct",
        "type": "huggingface",
        "max_tokens": 2048,
        "context_length": 8192,
        "estimated_ram": "3GB",
        "description": "가장 가벼운 코딩 특화 모델"
    },
    "deepseek-1.3b": {
        "name": "deepseek-ai/deepseek-coder-1.3b-instruct",
        "type": "huggingface",
        "max_tokens": 2048,
        "context_length": 16384,
        "estimated_ram": "3GB",
        "description": "DeepSeek 초경량 코딩 모델"
    },
    "phi-2": {
        "name": "microsoft/phi-2",
        "type": "huggingface",
        "max_tokens": 2048,
        "context_length": 2048,
        "estimated_ram": "5GB",
        "description": "Microsoft의 소형 고성능 모델"
    },
    "tinyllama": {
        "name": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "type": "huggingface",
        "max_tokens": 2048,
        "context_length": 2048,
        "estimated_ram": "2GB",
        "description": "가장 가벼운 범용 모델"
    },
    "codellama-7b-q4": {
        "name": "TheBloke/CodeLlama-7B-Instruct-GGUF",
        "type": "ollama",
        "max_tokens": 4096,
        "context_length": 16384,
        "estimated_ram": "4GB (quantized)",
        "description": "4-bit 양자화된 CodeLlama 7B"
    }
}

# RunPod 환경용 큰 모델들 (H100 PCIe 32GB/86GB 최적화)
RUNPOD_MODELS = {
    # === Chat 모델 (소크라테스 질문 생성에 최적) ===
    "qwen2.5-32b-instruct": {
        "name": "Qwen/Qwen2.5-32B-Instruct",
        "type": "huggingface",
        "max_tokens": 8192,
        "context_length": 32768,
        "estimated_vram": "32GB (full) / 20GB (4-bit)",
        "quantize": True,
        "description": "대형 Chat 모델 - 소크라테스 질문 생성 최적"
    },
    "qwen2.5-14b-instruct": {
        "name": "Qwen/Qwen2.5-14B-Instruct",
        "type": "huggingface",
        "max_tokens": 8192,
        "context_length": 32768,
        "estimated_vram": "28GB (full) / 16GB (4-bit)",
        "quantize": False,
        "description": "중형 Chat 모델 - 안정적인 질문 생성"
    },
    "llama-3.1-8b-instruct": {
        "name": "meta-llama/Llama-3.1-8B-Instruct",
        "type": "huggingface",
        "max_tokens": 8192,
        "context_length": 131072,
        "estimated_vram": "16GB (full) / 8GB (4-bit)",
        "quantize": False,
        "description": "Meta Llama 3.1 - 긴 context 지원"
    },
    "mistral-7b-instruct": {
        "name": "mistralai/Mistral-7B-Instruct-v0.3",
        "type": "huggingface",
        "max_tokens": 8192,
        "context_length": 32768,
        "estimated_vram": "14GB (full) / 7GB (4-bit)",
        "quantize": False,
        "description": "Mistral 7B - 균형잡힌 성능"
    },

    # === Coder 모델 (코드 분석에 최적) ===
    "qwen2.5-coder-32b": {
        "name": "Qwen/Qwen2.5-Coder-32B-Instruct",
        "type": "huggingface",
        "max_tokens": 8192,
        "context_length": 32768,
        "estimated_vram": "32GB (full) / 20GB (4-bit)",
        "quantize": True,
        "description": "대형 코딩 모델 - 정확한 코드 분석"
    },
    "deepseek-coder-33b": {
        "name": "deepseek-ai/deepseek-coder-33b-instruct",
        "type": "huggingface",
        "max_tokens": 8192,
        "context_length": 16384,
        "estimated_vram": "33GB (full) / 20GB (4-bit)",
        "quantize": True,
        "description": "DeepSeek 대형 코딩 모델"
    },
    "codellama-34b": {
        "name": "codellama/CodeLlama-34b-Instruct-hf",
        "type": "huggingface",
        "max_tokens": 16384,
        "context_length": 16384,
        "estimated_vram": "34GB (full) / 21GB (4-bit)",
        "quantize": True,
        "description": "Meta CodeLlama 34B"
    },

    # === 경량 비교 모델 ===
    "qwen2.5-7b-instruct": {
        "name": "Qwen/Qwen2.5-7B-Instruct",
        "type": "huggingface",
        "max_tokens": 8192,
        "context_length": 32768,
        "estimated_vram": "14GB (full) / 7GB (4-bit)",
        "quantize": False,
        "description": "경량 Chat 모델 - 빠른 응답"
    },
    "qwen2.5-3b-instruct": {
        "name": "Qwen/Qwen2.5-3B-Instruct",
        "type": "huggingface",
        "max_tokens": 4096,
        "context_length": 32768,
        "estimated_vram": "6GB (full) / 3GB (4-bit)",
        "quantize": False,
        "description": "초경량 모델 - 기본 비교용"
    }
}

# 생성 파라미터
GENERATION_PARAMS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "max_tokens": 512,
    "repetition_penalty": 1.1,
    "do_sample": True
}

# 평가용 샘플링 파라미터 (더 결정론적)
EVAL_GENERATION_PARAMS = {
    "temperature": 0.3,
    "top_p": 0.95,
    "max_tokens": 512,
    "repetition_penalty": 1.05,
    "do_sample": True
}
