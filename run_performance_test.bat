@echo off
chcp 65001 >nul
echo ============================================
echo    P[AI] 성능 테스트 실행
echo ============================================
echo.

REM Docker 백엔드가 실행 중인지 확인
echo [1/3] Docker 컨테이너 상태 확인 중...
docker ps | findstr hint_system_backend >nul
if %errorlevel% neq 0 (
    echo [오류] 백엔드 컨테이너가 실행 중이지 않습니다.
    echo Docker Compose로 서비스를 시작해주세요:
    echo   docker compose up -d
    pause
    exit /b 1
)
echo       백엔드 컨테이너 실행 중 - OK
echo.

REM 테스트 실행
echo [2/3] 성능 테스트 실행 중...
echo.

docker exec hint_system_backend python /app/tests/performance_test.py

echo.
echo [3/3] 테스트 완료
echo.

REM 결과 파일 복사
echo 결과 파일을 로컬로 복사 중...
docker cp hint_system_backend:/app/performance_test_results.json ./backend/tests/performance_test_results.json 2>nul
if %errorlevel% equ 0 (
    echo 결과 파일: backend\tests\performance_test_results.json
) else (
    echo [참고] 결과 파일은 컨테이너 내부에 저장되었습니다.
)

echo.
echo ============================================
echo    테스트 완료!
echo ============================================
pause
