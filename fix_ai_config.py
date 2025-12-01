import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.coding_test.models import AIModelConfig

c = AIModelConfig.objects.first()
if c:
    print("Current config:")
    print(f"  Mode: {c.mode}")
    print(f"  Model: {c.model_name}")
    print(f"  Runpod endpoint: {c.runpod_endpoint or 'NOT SET'}")
    print(f"  Runpod API key: {'SET' if c.runpod_api_key else 'NOT SET'}")
    print(f"  HF API key: {'SET' if c.api_key else 'NOT SET'}")

    # 사용자에게 모드 선택 요청
    print("\n옵션:")
    print("1. api 모드 유지 (HuggingFace - API key 필요)")
    print("2. runpod 모드로 변경 (Runpod vLLM - endpoint/api_key 필요)")
    print("3. local 모드로 변경 (로컬 모델)")

    # 현재는 api 모드로 유지하고, fallback 힌트가 제공되도록 함
    print("\n현재 api 모드이고 HF API key가 설정되어 있으므로 힌트가 작동해야 합니다.")
    print("만약 힌트가 안된다면 HuggingFace API 호출에 문제가 있을 수 있습니다.")
else:
    print("No config found!")
