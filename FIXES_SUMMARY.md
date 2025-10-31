# 최종 수정 사항 요약

프로젝트의 모든 수정 사항을 시간 순으로 정리한 문서입니다.

---

## 📅 2025-01-30 수정 사항

### 1. 폴더명 변경 및 환경 설정 자동화

#### 변경 내용
- 폴더명: `baekjoon-hint-system` → `5th-project_mvp`
- 하드코딩된 경로를 환경 변수로 변경

#### 신규 파일
1. **[.env.example](.env.example)** - 환경 변수 템플릿
2. **[config.py](config.py)** - 환경 설정 자동화
3. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - 환경 설정 가이드

#### 수정된 파일
1. **[hint-system/app.py](hint-system/app.py)**
   - `Config` import 추가
   - 하드코딩 경로 → `Config.EVALUATION_RESULTS_DIR`, `Config.DATA_FILE_PATH`

2. **[crawler/crawlers/baekjoon_hybrid_crawler.py](crawler/crawlers/baekjoon_hybrid_crawler.py)**
   - `Config` import 추가
   - `output_dir` 기본값 → `Config.CRAWLER_OUTPUT_DIR`

3. **[crawler/crawlers/crawl_all_hybrid.py](crawler/crawlers/crawl_all_hybrid.py)**
   - `Config` import 추가
   - 하드코딩 `"../data/raw"` 제거

4. **Requirements 업데이트**
   - [crawler/crawlers/requirements.txt](crawler/crawlers/requirements.txt): `python-dotenv>=1.0.0` 추가
   - [hint-system/requirements.txt](hint-system/requirements.txt): 이미 포함됨

#### 효과
- 각자의 환경에 맞게 `.env` 파일만 수정하면 자동 설정
- 팀원 간 경로 충돌 문제 해결
- 필요한 폴더 자동 생성

---

### 2. solved.ac API 테스트 파일 정리

#### 이동된 파일
1. **test_solved_ac_api.py** → [crawler/crawlers/test_solved_ac_api.py](crawler/crawlers/test_solved_ac_api.py)
2. **check_tags.py** → [crawler/crawlers/check_tags.py](crawler/crawlers/check_tags.py)

#### 신규 문서
- **[crawler/crawlers/README_API_TESTS.md](crawler/crawlers/README_API_TESTS.md)**
  - API 테스트 파일 설명
  - 하이브리드 크롤러 설계 결정 과정
  - solved.ac API 문서 링크

---

### 3. 프롬프트 개선 V5

#### 문제 상황
**사용자 코드:**
```python
N, M = map(int, input().split())
board = []
for _ in range(N):
    board.append(input())
```

**생성된 힌트 (V4):**
```
"이상한 코드를 100번 쓰려고 하는데 어떤 대안을 고민하나요"
```

**문제:**
- 프롬프트의 "질문 방식" 예시("100번 복사")를 모델이 그대로 따라함
- 모델이 창의적으로 생각하지 않고 예시 복사

#### 해결책 1: 프롬프트 예시 완전 제거 ([app.py:322-348](hint-system/app.py#L322-L348))

**V4 (Before):**
```python
질문 방식:
- "지금 코드를 100번 복사해야 한다면 어떻게 할까?"
- "이 작업을 나중에 다시 써야 한다면?"
```

**V5 (After):**
```python
절대 금지 사항 (매우 중요!):
1. 함수명, 변수명 언급 금지
2. 코드 구조 직접 언급 금지
3. 백틱(`)이나 코드 블록 사용 금지
4. "~해야 합니다", "~하세요" 같은 설명/지시 금지

질문 생성 방법:
- 현재 코드가 감당하기 어려운 상황 제시
- 규모가 커지거나 반복/수정이 필요한 상황 강조
```

**핵심 변경:**
- 구체적 예시 제거 ("100번", "1000개" 등)
- 추상적 원칙만 제시
- 절대 금지 사항 명시 강화

---

### 4. 한국어 필터 오탐 해결

#### 문제 상황
터미널 출력:
```
[DEBUG] 원본 출력: **답변:** 만약 `print_board`라는 함수가...
[DEBUG] 영어 출력 필터링: **답변:** 만약 `print_...
```

화면 표시:
```
📌 Qwen2.5-Coder-1.5B
(모델이 한국어 힌트를 생성하지 못했습니다)
```

**원인:**
- 모델이 백틱으로 함수명 언급: `` `print_board` ``
- 한국어 비율 체크 시 백틱도 포함 → 한국어 비율 30% 미만
- 정상 한국어 힌트가 "영어 출력"으로 오판

#### 해결책 2: 한국어 필터 개선 ([model_inference.py:174-185](hint-system/models/model_inference.py#L174-L185))

**Before:**
```python
korean_chars = len(re.findall(r'[가-힣]', clean))
total_chars = len(clean.replace(' ', ''))
```

**After:**
```python
# 백틱/코드 블록 제외하고 한국어 비율 체크
text_without_code = re.sub(r'`[^`]+`', '', clean)
text_without_code = re.sub(r'```[^`]+```', '', text_without_code)

korean_chars = len(re.findall(r'[가-힣]', text_without_code))
total_chars = len(text_without_code.replace(' ', ''))
```

**효과:**
- 코드 부분 제외하고 순수 텍스트만 체크
- 한국어 오탐 방지

---

### 5. 백틱 함수명 필터 추가 ([model_inference.py:251-255](hint-system/models/model_inference.py#L251-L255))

```python
# 백틱으로 감싸진 함수명/변수명 차단
if re.search(r'`[a-z_]+`', sentence):
    print(f"[DEBUG] 백틱 함수명 언급 필터링: {sentence[:50]}...")
    continue
```

**효과:**
- `` `print_board` ``, `` `count_repaint` `` 같은 백틱 함수명 자동 차단
- 함수명 언급 원천 차단

---

### 6. 불완전한 문장 필터 추가

#### 문제 상황
**생성된 힌트:**
```
입력 받는 두 수 N, M에서 각 행마다 특정 문자열 확인하고,
```

**문제:**
- 문장이 쉼표(,)로 끝남 → 불완전한 문장
- 물음표(?)가 없어서 질문 아님
- 모델이 생성을 중간에 멈춤

#### 해결책 1: 불완전한 문장 필터 ([model_inference.py:295-299](hint-system/models/model_inference.py#L295-L299))

```python
# 불완전한 문장 필터링
incomplete_endings = [',', '그리고', '그런데', '또는', '및', '와', '과', '~고', '~며']
if any(sentence.endswith(ending) for ending in incomplete_endings):
    print(f"[DEBUG] 불완전한 문장 필터링: {sentence[:50]}...")
    continue
```

#### 해결책 2: 프롬프트 출력 형식 강화 ([app.py:346-352](hint-system/app.py#L346-L352))

**Before:**
```python
출력 형식:
한국어 반말로 질문 1개만. 코드나 구체적 이름 없이 순수 질문만:
```

**After:**
```python
출력 형식:
- 한국어 반말로 완전한 질문 1개만
- 반드시 물음표(?)로 끝나야 함
- 불완전한 문장 금지 (예: "~하고,", "~하며," 같은 끝맺음)
- 코드나 구체적 이름 없이 순수 질문만

질문:
```

**효과:**
- 불완전한 문장 자동 제거
- 모델에게 완전한 질문 생성 강제

---

### 7. 프롬프트 개선 V6 - 초간단 명령 ([app.py:322-346](hint-system/app.py#L322-L346))

#### 문제 상황
터미널 출력:
```
그런데... 어떻게~? I'm really confused about how to define functions here.
```

**원인:**
- V5 프롬프트가 너무 복잡 (9개 항목)
- 모델이 혼란스러워하며 영어로 전환
- "소크라테스식 질문 원칙" 같은 추상적 개념

#### 해결책

**프롬프트 간소화:**
- 불필요한 설명 제거 (9개 → 5개 규칙)
- 직접적 명령형: "작성하세요"
- 영어 금지 명시
- 출력 형식 단순화

**영어 필터링 강화 ([model_inference.py:174-192](hint-system/models/model_inference.py#L174-L192)):**

3단계 검증:
1. 백틱/코드 블록 제거
2. 영어 문장 감지 (5자 이상 영어 단어)
3. 한국어 비율 30% → 50%로 상향

---

### 8. 프롬프트 개선 V7 - 대조 학습 (진짜 소크라테스식) ([app.py:322-348](hint-system/app.py#L322-L348))

#### 문제 상황
**생성된 힌트:**
```
만약 이 작업을 큰 규모로 해야 한다면?
```

**사용자 피드백:**
> "애초에 '만약 이 작업을 큰 규모로 해야 한다면?'를 좋은 '힌트'라고 생각 안 해. 소크라테스 공부법에 맞는 질문이 아니잖아."

**문제:**
- "큰 규모"가 너무 추상적
- 학생이 구체적으로 무엇을 해야 할지 모름
- 소크라테스 학습법의 핵심인 **구체적 상황**이 없음

#### 해결책: 대조 학습

**V7 프롬프트 핵심:**
```python
질문 작성 원칙:
1. 구체적 상황: "큰 규모"(X) → "10개", "100번", "1000개"(O)
2. 현실적 불편: 추상적 질문(X) → 직접 겪을 불편함(O)
3. 학생 관점: "어떻게 하면 좋을까?"(X) → "너는 어떻게 할 건데?"(O)

나쁜 질문 vs 좋은 질문:
- "큰 규모로 하려면?" (막연) vs "10개 처리하려면 코드 10번 복사?" (구체적)
- "효율적 방법은?" (추상) vs "나중에 숫자 바꾸면 어쩔 건데?" (현실적)
```

**개선 사항:**
- 대조(Contrast) 방식: 나쁜 예 vs 좋은 예
- 구체적 숫자 요구
- 현실적 불편 강조
- 완전한 예시 문장 제거 (복사 방지)

---

### 9. 프롬프트 개선 V8 - 개념 질문 완전 차단

#### 문제 상황
**생성된 힌트:**
```
함수 정의를 이해하고 사용하기 위한 과정에서 중요한 단계 중 하나가 무엇일까요
```

**사용자 피드백:**
> "힌트는 해당 문제의 해답 코드를 N개의 Logic으로 분할한 후,
> - 사용자가 M번째 Logic을 틀릴 경우 → M번째 Logic을 풀어낼 수 있는 형태
> - 사용자가 M번째까지 완벽하고 M+1번째를 모르는 경우 → M+1번째 Logic을 떠올릴 수 있는 형태
> - 소크라테스 학습법으로 사용자가 직접 생각할 수 있도록"

**문제:**
- "함수 정의를 이해하고" → 교육적/개념적 질문
- "중요한 단계" → 추상적 학습 질문
- 사용자 코드의 **구체적 문제 상황** 없음

#### 해결책: 개념 질문 명시적 차단

**V8 프롬프트 핵심:**
```python
임무: 학생이 지금 코드로는 "{next_step_goal}"를 할 수 없다는 걸 깨닫게 만드는 질문

절대 금지:
- "함수가 뭐야?", "반복문이 뭐야?" 같은 개념 질문 금지
- "중요한 단계", "핵심 개념", "이해하기" 같은 교육적 표현 금지

나쁜 질문 (교육적, 개념적):
- "함수 정의를 이해하는 중요한 단계가 뭘까?" (교육적)
- "효율적인 방법이 있을까?" (추상적)

좋은 질문 (상황적, 구체적):
- "같은 계산을 10군데에서 해야 하는데 코드 10번 복사할 건가?" (상황)
- "나중에 계산 방법 바꾸면 10군데를 다 찾아서 수정해?" (불편)
```

**개선 사항:**
- 명시적 개념 질문 차단 (예시 제공)
- 교육적 표현 금지 리스트
- 프레임 변경: "필요성" → "지금 코드로는 불가능"
- 나쁜 질문 예시 추가 (교육적/개념적)

**V8의 한계:**
- Logic Step 컨텍스트 없음
- 학생이 어느 단계인지 불명확
- 소크라테스 학습법의 진짜 의미 누락

---

### 10. 프롬프트 개선 V9 - Logic Step 기반 소크라테스 학습법 ([app.py:322-369](hint-system/app.py#L322-L369))

#### 문제 상황 (V8의 치명적 결함)

**사용자 요구사항 재확인:**
> "힌트는 해당 문제의 해답 코드를 N개의 Logic으로 분할한 후,
> - 사용자가 M번째 Logic을 틀릴 경우 → M번째 Logic을 풀어낼 수 있는 형태
> - 사용자가 M번째까지 완벽하고 M+1번째를 모르는 경우 → M+1번째 Logic을 떠올릴 수 있는 형태"

**V8의 문제:**
```python
# V8 - 컨텍스트 부족
학생이 막힌 부분: {next_step_goal}
임무: 학생이 지금 코드로는 "{next_step_goal}"를 할 수 없다는 걸 깨닫게
```

❌ Logic Step 개념 없음
❌ M번째/M+1번째 구분 불가능
❌ 학생의 진행 상황 컨텍스트 없음

#### 해결책: Logic Step 기반 프롬프트

**V9 프롬프트 핵심:**
```python
상황:
이 문제의 정답 코드는 여러 Logic으로 나뉩니다.
학생은 지금까지 일부 Logic은 구현했지만, "{next_step_goal}"를 아직 구현하지 못했습니다.

다음 단계 (학생이 구현해야 하는 Logic):
{next_step_goal}

임무:
학생의 현재 코드로는 "{next_step_goal}"를 할 수 없다는 것을 깨닫게 만드는 질문을 작성하세요.
학생이 스스로 "{next_step_goal}"의 필요성을 발견하도록 구체적인 상황/불편함을 제시하세요.

질문 작성 전략 (소크라테스 학습법):
1. 현재 코드의 한계: 지금 코드로는 어떤 상황을 처리 못하는지
2. 구체적 숫자 사용: "여러 개"(X) → "10개", "100번", "1000줄"(O)
3. 직접적 불편 제시: "좋은 방법은?"(X) → "너는 매번 손으로 할 건데?"(O)
4. 확장 상황 제시: "입력이 2개가 아니라 100개면?", "문제가 바뀌면 또 처음부터?"
```

**개선 사항:**
1. ✅ **Logic Step 명시** - "정답 코드는 여러 Logic으로 나뉩니다"
2. ✅ **진행 상황 제시** - "일부 Logic은 구현했지만"
3. ✅ **다음 단계 명확화** - "다음 단계 (학생이 구현해야 하는 Logic)"
4. ✅ **발견 학습 강조** - "스스로 필요성을 발견하도록"
5. ✅ **확장 상황 전략** - "입력 100개면?", "문제 바뀌면?"
6. ✅ **직접 언급 금지** - "{next_step_goal} 내용을 직접 말하지 말고 상황으로 유도"

**사용자 요구사항 충족:**
- ✅ N개 Logic 분할 명시
- ✅ M번째 Logic 틀린 경우 → "현재 코드의 한계" 제시
- ✅ M+1번째 Logic 모름 → "일부 구현 + 확장 상황" 유도
- ✅ 소크라테스 학습법 → "스스로 발견" + "상황/불편함 제시"

**V9 테스트 결과:**
- ❌ 질문 대신 코드 생성
- ❌ 에러 메시지 출력 (TypeError)
- ❌ Coder 모델이 디버깅 모드 진입

---

### 11. 프롬프트 개선 V10 - Coder 모델 특성 고려 (코드 제거) ([app.py:322-366](hint-system/app.py#L322-L366))

#### 문제 상황 (V9 실패)

**V9 테스트 출력:**
```
N, M = map(int, input().split())
board = []
for _ in range(N):
    board.append(input())

결과 출력:
TypeError: 'str' object is not callable
```

**필터링 결과:**
```
[DEBUG] 영어 문장 감지 필터링: ['board', 'board', 'TypeError']
```

**문제:**
- 질문 대신 코드 생성
- 에러 메시지 출력
- Coder 모델이 디버깅 모드로 전환

#### 근본 원인: Qwen2.5-Coder 모델 특성

**모델 특성:**
- Qwen2.5-**Coder** → 코드 작성/디버깅에 특화
- 프롬프트에 코드 보이면 → 디버깅 모드 활성화
- 질문 생성보다 코드 수정 우선

**V9 프롬프트의 실수:**
```python
학생이 작성한 코드:
{user_code}  # ← Coder 모델에게 코드를 보여줌!
```

#### 해결책: 코드 컨텍스트 제거

**V10 프롬프트 핵심:**
```python
너는 학생에게 힌트를 주는 선생님이다.

상황 설명:
- 학생이 코딩 문제를 풀고 있다
- 학생은 일부는 구현했지만 "{next_step_goal}"를 아직 못했다

절대 금지 (중요!):
1. 코드 작성 금지 - 질문만 만들어라
2. 개념 질문 금지 - "함수가 뭐야?", "반복문이 뭐야?" 같은 거 금지

질문 만드는 방법:
1. 구체적 숫자로 불편한 상황 만들기
   - "여러 개"(X) → "10개", "100번"(O)
2. 직접 체감하는 불편함
   - "좋은 방법?"(X) → "손으로 100번 쓸 건데?"(O)
3. 확장 상황 제시
   - "입력 2개가 아니라 100개면?"

출력:
한국어 반말 질문 1개 (물음표 필수, 구체적 숫자 포함)
```

**개선 사항:**
1. ✅ **코드 완전 제거** - user_code 변수 삭제
2. ✅ **"코드 작성 금지" 명시** - Coder 모델에게 명시적 지시
3. ✅ **역할 명시** - "너는 선생님이다"
4. ✅ **Logic Step 간소화** - "일부 구현, 일부 못함"
5. ✅ **짧고 직접적** - 43줄로 축소

**Coder 모델 대응 전략:**
- 코드를 보여주지 않기
- "코드 금지" 명시적 지시
- 역할 부여 ("선생님")
- 간단 명령 위주

---

## 📚 관련 문서

### 개발 과정 문서 (docs/)
1. **[PROMPT_IMPROVEMENT_LOG.md](docs/PROMPT_IMPROVEMENT_LOG.md)** - V1→V2 변경사항
2. **[PROMPT_FIX_V3.md](docs/PROMPT_FIX_V3.md)** - V2→V3 함수명 차단
3. **[PROMPT_FIX_V5.md](docs/PROMPT_FIX_V5.md)** - V4→V5 예시 제거
4. **[PROMPT_FIX_V6.md](docs/PROMPT_FIX_V6.md)** - V5→V6 초간단 명령
5. **[PROMPT_FIX_V7.md](docs/PROMPT_FIX_V7.md)** - V6→V7 대조 학습
6. **[PROMPT_FIX_V8.md](docs/PROMPT_FIX_V8.md)** - V7→V8 개념 질문 차단
7. **[PROMPT_FIX_V9.md](docs/PROMPT_FIX_V9.md)** - V8→V9 Logic Step 기반
8. **[PROMPT_FIX_V10.md](docs/PROMPT_FIX_V10.md)** - V9→V10 Coder 모델 특화 (최신)
9. **[MIGRATION_SUMMARY.md](docs/MIGRATION_SUMMARY.md)** - 데이터 구조 변경

### 사용자 가이드
1. **[README.md](README.md)** - 프로젝트 개요
2. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - 환경 설정 가이드
3. **[hint-system/README.md](hint-system/README.md)** - 힌트 시스템 상세
4. **[crawler/README.md](crawler/README.md)** - 크롤러 사용법

---

## 🎯 V1 → V10 변천사

| 버전 | 핵심 전략 | Logic Step | Coder 모델 | 결과 |
|------|-----------|------------|------------|------|
| **V1** | solution_code 제공 | ❌ | ❌ | 함수명 언급 |
| **V2** | 나쁜 예시 추가 | ❌ | ❌ | 나쁜 예시 복사 |
| **V3** | 나쁜 예시 제거 | ❌ | ❌ | 예시 의존 |
| **V4** | 질문 방식 예시 | ❌ | ❌ | 예시 복사 |
| **V5** | 모든 예시 제거 | ❌ | ❌ | 프롬프트 복잡 |
| **V6** | 초간단 명령 | ❌ | ❌ | 막연한 질문 |
| **V7** | 대조 학습 | ❌ | ❌ | 개념 질문 생성 |
| **V8** | 개념 질문 차단 | ❌ | ❌ | Logic Step 없음 |
| **V9** | Logic Step 기반 | ✅ | ❌ | **코드 디버깅** |
| **V10** | 코드 제거 | ✅ | ✅ | 테스트 필요 |

---

## ✅ 최종 상태

### 프롬프트 (V10)
- ✅ **Coder 모델 대응** - user_code 완전 제거
- ✅ **"코드 작성 금지"** - Coder 모델에게 명시적 지시
- ✅ **역할 명시** - "너는 선생님이다"
- ✅ **Logic Step 간소화** - "일부 구현, 일부 못함"
- ✅ **발견 학습** - "스스로 필요성 깨닫도록"
- ✅ **개념 질문 차단** - "함수가 뭐야?" 금지
- ✅ **교육적 표현 차단** - "중요한 단계", "핵심 개념" 금지
- ✅ **구체적 숫자** - "10개", "100번"
- ✅ **확장 상황** - "입력 100개면?"
- ✅ **짧고 직접적** - 43줄로 간소화

### 필터링 시스템
- ✅ 백틱 함수명 자동 차단
- ✅ snake_case/camelCase 패턴 감지
- ✅ 한국어 비율 체크 개선 (코드 제외)
- ✅ 직접 답 요구 필터링
- ✅ 막연한 지시문 필터링

### 환경 설정
- ✅ `.env` 파일 기반 자동 설정
- ✅ 경로 충돌 문제 해결
- ✅ 필요한 폴더 자동 생성

---

**작성일:** 2025-01-30
**최종 버전:** V10 (Coder 모델 특화)
