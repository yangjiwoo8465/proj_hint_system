"""
Runpod API 클라이언트
원격 서버에서 무거운 모델을 실행하고 결과를 받아옵니다.
"""

import requests
import time
from typing import Dict
import sys
sys.path.append('..')
from config import Config


class RunpodClient:
    """Runpod API를 통해 원격 모델 실행"""

    def __init__(self, model_name: str):
        """
        Args:
            model_name: 모델 이름 (표시용)
        """
        self.model_name = model_name
        self.api_endpoint = Config.RUNPOD_API_ENDPOINT
        self.api_key = Config.RUNPOD_API_KEY

        if not self.api_endpoint or not self.api_key:
            raise ValueError(
                "Runpod API 설정이 필요합니다. .env 파일에서 "
                "RUNPOD_API_ENDPOINT와 RUNPOD_API_KEY를 설정하세요."
            )

    def generate_hint(self, prompt: str, max_tokens: int = 30, temperature: float = 0.8) -> Dict:
        """
        Runpod API를 통해 힌트 생성

        Args:
            prompt: 입력 프롬프트
            max_tokens: 최대 생성 토큰 수
            temperature: 샘플링 온도

        Returns:
            힌트 생성 결과 딕셔너리
        """
        try:
            start_time = time.time()

            # Runpod API 요청 페이로드
            payload = {
                "input": {
                    "prompt": prompt,
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": 0.9,
                    "do_sample": True,
                    "repetition_penalty": 1.2
                }
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            print(f"[RUNPOD] {self.model_name}에 요청 중...")

            # API 호출
            response = requests.post(
                self.api_endpoint,
                json=payload,
                headers=headers,
                timeout=60  # 60초 타임아웃
            )

            response.raise_for_status()
            result = response.json()

            # Runpod 응답 파싱
            if "output" in result:
                hint = result["output"].strip()
            elif "delayTime" in result:
                # Job이 큐에 들어간 경우 (비동기 처리)
                job_id = result.get("id")
                print(f"[RUNPOD] Job {job_id} 큐에 등록됨, 대기 중...")
                hint = "(Runpod 작업 대기 중 - 비동기 엔드포인트 사용 중)"
            else:
                hint = "(Runpod 응답 형식 오류)"

            elapsed = time.time() - start_time

            return {
                'hint': hint,
                'time': elapsed,
                'model': f"{self.model_name} (Runpod)",
                'error': None
            }

        except requests.exceptions.Timeout:
            return {
                'hint': '',
                'time': 60,
                'model': f"{self.model_name} (Runpod)",
                'error': "Runpod API 타임아웃 (60초 초과)"
            }
        except requests.exceptions.RequestException as e:
            return {
                'hint': '',
                'time': 0,
                'model': f"{self.model_name} (Runpod)",
                'error': f"Runpod API 에러: {str(e)}"
            }
        except Exception as e:
            return {
                'hint': '',
                'time': 0,
                'model': f"{self.model_name} (Runpod)",
                'error': f"예상치 못한 에러: {str(e)}"
            }

    def is_available(self) -> bool:
        """Runpod API 사용 가능 여부 확인"""
        return bool(self.api_endpoint and self.api_key)
