"""
Runpod vLLM 서버 연결 테스트 스크립트
"""
from openai import OpenAI
import sys

def test_vllm_connection(endpoint_url):
    """vLLM 서버 연결 테스트"""

    print("=" * 50)
    print("Runpod vLLM Connection Test")
    print("=" * 50)
    print(f"Endpoint: {endpoint_url}")

    try:
        # OpenAI 클라이언트 생성
        client = OpenAI(
            base_url=f"{endpoint_url}/v1",
            api_key="EMPTY"  # vLLM은 API 키 불필요
        )

        print("\n테스트 요청 전송 중...")

        # 테스트 요청
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful coding assistant."
                },
                {
                    "role": "user",
                    "content": "Python으로 1부터 10까지의 합을 구하는 함수를 작성해줘."
                }
            ],
            temperature=0.7,
            max_tokens=500
        )

        print("\n✅ 연결 성공!")
        print("\n응답:")
        print("-" * 50)
        print(response.choices[0].message.content)
        print("-" * 50)

        print(f"\n사용 토큰:")
        print(f"  - Prompt: {response.usage.prompt_tokens}")
        print(f"  - Completion: {response.usage.completion_tokens}")
        print(f"  - Total: {response.usage.total_tokens}")

        return True

    except Exception as e:
        print(f"\n❌ 연결 실패!")
        print(f"에러: {str(e)}")
        print("\n문제 해결 방법:")
        print("1. Runpod vLLM 서버가 실행 중인지 확인")
        print("2. 엔드포인트 URL이 올바른지 확인")
        print("3. 네트워크 연결 확인")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python test_connection.py <endpoint_url>")
        print("예시: python test_connection.py https://abc123-8000.proxy.runpod.net")
        sys.exit(1)

    endpoint = sys.argv[1]

    # URL에서 /v1 제거 (자동으로 추가됨)
    if endpoint.endswith('/v1'):
        endpoint = endpoint[:-3]

    success = test_vllm_connection(endpoint)
    sys.exit(0 if success else 1)
