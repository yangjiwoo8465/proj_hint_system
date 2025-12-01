"""
간단한 Runpod vLLM 연결 테스트
"""
import requests
import sys

def test_runpod(endpoint_url):
    """Runpod vLLM 서버 테스트"""

    print("=" * 50)
    print("Runpod vLLM Connection Test")
    print("=" * 50)
    print(f"Endpoint: {endpoint_url}")

    # 1. 모델 목록 확인
    print("\n[1] 모델 목록 확인 중...")
    try:
        response = requests.get(f"{endpoint_url}/v1/models")
        if response.status_code == 200:
            print("✅ 모델 목록 조회 성공!")
            print(f"응답: {response.json()}")
        else:
            print(f"❌ 실패: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 연결 실패: {e}")
        return False

    # 2. Chat Completion 테스트
    print("\n[2] Chat Completion 테스트 중...")
    try:
        payload = {
            "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
            "messages": [
                {
                    "role": "user",
                    "content": "Python으로 1부터 5까지의 합을 구하는 함수를 작성해줘."
                }
            ],
            "max_tokens": 200,
            "temperature": 0.7
        }

        response = requests.post(
            f"{endpoint_url}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Chat Completion 성공!")
            print("\n응답:")
            print("-" * 50)
            print(data['choices'][0]['message']['content'])
            print("-" * 50)

            if 'usage' in data:
                print(f"\n사용 토큰:")
                print(f"  - Prompt: {data['usage']['prompt_tokens']}")
                print(f"  - Completion: {data['usage']['completion_tokens']}")
                print(f"  - Total: {data['usage']['total_tokens']}")

            return True
        else:
            print(f"❌ 실패: {response.status_code}")
            print(f"응답: {response.text}")
            return False

    except Exception as e:
        print(f"❌ 요청 실패: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python test_runpod_simple.py <endpoint_url>")
        print("예시: python test_runpod_simple.py https://abc123-8000.proxy.runpod.net")
        sys.exit(1)

    endpoint = sys.argv[1]

    # URL에서 /v1 제거 (자동으로 추가됨)
    if endpoint.endswith('/v1'):
        endpoint = endpoint[:-3]

    success = test_runpod(endpoint)

    if success:
        print("\n" + "=" * 50)
        print("✅ 모든 테스트 통과!")
        print("=" * 50)
        print("\n다음 단계:")
        print("1. Django 관리자 패널 접속: http://localhost:8000/admin-panel")
        print("2. Models 탭 선택")
        print("3. Runpod vLLM 방식 선택")
        print(f"4. Endpoint URL: {endpoint}")
        print("5. 모델명: Qwen/Qwen2.5-Coder-32B-Instruct")
        print("6. 설정 저장")
    else:
        print("\n" + "=" * 50)
        print("❌ 테스트 실패")
        print("=" * 50)
        print("\n확인 사항:")
        print("1. Runpod vLLM 서버가 실행 중인지 확인")
        print("2. Endpoint URL이 올바른지 확인")
        print("3. 네트워크 연결 확인")

    sys.exit(0 if success else 1)
