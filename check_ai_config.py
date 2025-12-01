import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.coding_test.models import AIModelConfig

c = AIModelConfig.objects.first()
print("Config exists:", c is not None)
if c:
    print("Mode:", c.mode)
    print("Runpod endpoint:", c.runpod_endpoint)
    print("Runpod API key:", "SET" if c.runpod_api_key else "NOT SET")
    print("API key:", "SET" if c.api_key else "NOT SET")
else:
    print("No AI config found - creating default")
    c = AIModelConfig.objects.create(mode='runpod')
    print("Created default config with mode:", c.mode)
