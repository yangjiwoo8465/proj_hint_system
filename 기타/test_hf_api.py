"""Test Hugging Face Inference Providers API"""
import requests
import json
import os

# REPLACE WITH YOUR ACTUAL API KEY
API_KEY = "YOUR_API_KEY_HERE"  # User needs to replace this

def test_inference_providers():
    """Test the Inference Providers API"""
    url = "https://router.huggingface.co/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "Qwen/Qwen2.5-Coder-7B-Instruct",
        "messages": [
            {"role": "system", "content": "You are a coding assistant."},
            {"role": "user", "content": "Say hello in one short sentence."}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }

    print("Testing Hugging Face Inference Providers API...")
    print(f"URL: {url}")
    print(f"Model: {payload['model']}")
    print()

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        print(f"Status Code: {response.status_code}")
        print()

        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print("Response:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print()
                print("Generated Text:")
                print(content)
        else:
            print("❌ ERROR!")
            print("Response Body:")
            print(response.text)

    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")

if __name__ == "__main__":
    if API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  Please replace YOUR_API_KEY_HERE with your actual Hugging Face API key in the script!")
        print("You can get one from: https://huggingface.co/settings/tokens")
        print("Make sure it has 'Make calls to Inference Providers' permission!")
    else:
        test_inference_providers()
