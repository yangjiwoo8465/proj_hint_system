# 백준 문제 크롤러

백준(acmicpc.net) + solved.ac 하이브리드 크롤러

## 📁 구조

```
crawler/
└── crawlers/
    └── baekjoon_hybrid_crawler.py  # 메인 크롤러
```

## 🚀 사용법

### 기본 실행

```bash
cd crawlers
python baekjoon_hybrid_crawler.py
```

### 스크립트 내 설정

```python
if __name__ == "__main__":
    crawler = BaekjoonHybridCrawler(output_dir="../data/raw")

    # 1~68단계 크롤링
    problems = crawler.crawl_by_steps(
        start_step=1,
        end_step=68,
        delay=1.0  # 요청 간격 (초)
    )
```

## 📊 크롤링 데이터

### 백준에서 수집
- **단계 목록**: https://www.acmicpc.net/step
- **문제 목록**: 각 단계별 문제 리스트
- **문제 상세**:
  - 제목
  - 설명
  - 입력 조건
  - 출력 조건
  - 예제 (입력/출력)

### solved.ac API에서 수집
- **난이도**: Level 1~30 (Bronze~Ruby)
- **태그**: 알고리즘 분류 (구현, 수학, DP 등)
- **API 엔드포인트**: https://solved.ac/api/v3/problem/show

## 📝 출력 형식

### 파일명
```
problems_hybrid_step_{start}_to_{end}.json
```

예시: `problems_hybrid_step_1_to_68.json`

### JSON 구조

```json
[
  {
    "problem_id": "1000",
    "step_title": "입출력과 사칙연산",
    "title": "A+B",
    "level": 1,
    "tags": ["구현", "사칙연산", "수학"],
    "description": "두 정수 A와 B를 입력받은 다음, A+B를 출력하는 프로그램을 작성하시오.",
    "input_description": "첫째 줄에 A와 B가 주어진다. (0 < A, B < 10)",
    "output_description": "첫째 줄에 A+B를 출력한다.",
    "examples": [
      {
        "input": "1 2",
        "output": "3"
      }
    ],
    "url": "https://www.acmicpc.net/problem/1000"
  }
]
```

## ⚙️ 주요 기능

### 1. 단계별 크롤링
```python
crawler.crawl_by_steps(start_step=1, end_step=10)
```

### 2. 요청 간격 설정
```python
delay=1.0  # 1초 대기 (서버 부하 방지)
```

### 3. 에러 처리
- 네트워크 오류 시 재시도
- 실패한 문제는 로그 출력
- 성공/실패 통계 제공

## 🛠️ 필수 패키지

```bash
pip install requests beautifulsoup4
```

또는

```bash
pip install -r requirements_crawler.txt
```

## 📊 크롤링 결과 예시

```
======================================================================
단계별 문제 크롤링: 1 ~ 68
======================================================================

[1/68] 입출력과 사칙연산 (8개 문제)
  1000. A+B.................................. [OK]
  1001. A-B.................................. [OK]
  ...

[SUCCESS] 성공: 531
[FAIL] 실패: 2
총 529개 문제 저장
======================================================================
```

## 🚨 주의사항

### 1. 크롤링 에티켓
- **요청 간격 준수**: delay를 최소 1초 이상 설정
- **과도한 요청 금지**: 한 번에 너무 많은 단계 크롤링 X
- **robots.txt 준수**

### 2. API 제한
- **solved.ac API**: 일일 요청 제한 있음
- 대량 크롤링 시 API 키 필요할 수 있음

### 3. 데이터 사용
- 교육 목적으로만 사용
- 상업적 이용 금지

## 🔧 커스터마이징

### 특정 단계만 크롤링

```python
# 단계 1~3만
problems = crawler.crawl_by_steps(start_step=1, end_step=3)
```

### 특정 문제 ID 크롤링

```python
problem_id = "1000"
problem_url = f"{crawler.BAEKJOON_URL}/problem/{problem_id}"

# 백준 문제 상세
problem_data = crawler.get_problem_detail(problem_url)

# solved.ac 메타데이터
meta = crawler.get_solved_ac_data(problem_id)
problem_data.update(meta)
```

## 📈 성능

- **속도**: 약 1문제/초 (delay=1.0)
- **531개 문제**: 약 9분 소요
- **메모리**: 매우 적음 (< 100MB)

## 🐛 문제 해결

### 1. 크롤링 실패
```
[FAIL] 1234. 문제 제목
```

**원인:**
- 네트워크 오류
- 백준 서버 응답 지연
- HTML 구조 변경

**해결:**
1. 다시 실행 (자동 재시도)
2. delay 늘리기 (2.0 이상)
3. 해당 문제만 따로 크롤링

### 2. solved.ac API 오류
```
[ERROR] solved.ac API 호출 실패
```

**원인:**
- API 요청 제한 초과
- 네트워크 오류

**해결:**
1. 잠시 후 재시도
2. API 키 사용 (고급)

### 3. HTML 파싱 실패
```
[ERROR] 문제 설명을 찾을 수 없습니다
```

**원인:**
- 백준 HTML 구조 변경

**해결:**
1. crawler 코드 업데이트 필요
2. BeautifulSoup selector 수정

## 📝 로그

### 성공 로그
```
[OK] - 정상 크롤링
[SUCCESS] - 전체 성공 개수
```

### 실패 로그
```
[FAIL] - 크롤링 실패
[ERROR] - 에러 상세
```

## 🔄 업데이트

### v1.0.0 (2025-01-30)
- 초기 버전
- 백준 + solved.ac 하이브리드
- 단계별 크롤링 지원

---

**마지막 업데이트:** 2025-01-30
