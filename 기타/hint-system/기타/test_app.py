"""
간단한 app.py 테스트 (모델 로드 없이)
"""
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import Config

print("\n" + "=" * 60)
print("코딩 힌트 모델 평가 시스템 테스트")
print("=" * 60 + "\n")

# 환경 설정 출력
Config.print_config()

# 데이터 경로 확인
DATA_PATH = Config.DATA_FILE_PATH
if not DATA_PATH.exists():
    print(f"[ERROR] 데이터 파일을 찾을 수 없습니다: {DATA_PATH}")
    exit(1)

print(f"\n[OK] 데이터 파일 확인 완료: {DATA_PATH}")

# 앱 초기화 (모델 자동 로드 비활성화)
print("\n[TEST] HintEvaluationApp 초기화 중 (auto_setup_models=False)...")

# app.py에서 HintEvaluationApp 임포트
import os
os.chdir('/workspace/proj_hint_system/hint-system')
from app import HintEvaluationApp

app = HintEvaluationApp(str(DATA_PATH), auto_setup_models=False)
print(f"[OK] {len(app.problems)}개 문제 로드 완료!")

print("\n" + "=" * 60)
print("테스트 완료! app.py는 정상적으로 작동합니다.")
print("=" * 60)
print("\n실제 실행 방법:")
print("  cd /workspace/proj_hint_system/hint-system")
print("  python app.py")
print("\n주의: 실제 실행 시 모델을 자동으로 다운로드하므로 시간이 걸립니다.")
