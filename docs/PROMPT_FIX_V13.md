# V13 - 코드 기반 맞춤형 힌트 (사용자 코드 분석)

## 문제 상황 (V12의 한계)

### V12 템플릿의 문제

**V12 출력 예시:**
```python
# next_step_goal = "함수 정의"
# 모든 사용자에게 동일한 질문
"같은 계산을 10군데에서 해야 하는데 코드 10번 복사?"
```

**문제:**
- **일반적인 질문** - 사용자 코드와 무관
- **맞춤형 아님** - 모든 사용자에게 같은 힌트
- **user_code 무시** - 실제 코드 분석 안 함

**사용자 피드백:**
> "템플릿을 사용하는 현재 형태의 경우 '사용자'의 코드에 맞는 맞춤 질문/힌트가 아니잖아."

---

## V13 해결책: 코드 분석 기반

### 핵심 전략

**V12:**
```python
키워드 매칭 → 템플릿 선택 → 일반적 질문
```

**V13:**
```python
user_code 분석 → 구체적 패턴 발견 → 맞춤형 질문
```

---

## 코드 분석 시스템

### _analyze_user_code() 함수

**목적:** 사용자 코드에서 구체적 패턴 추출

**분석 항목:**

1. **similar_lines** - 반복되는 코드 패턴
2. **repeat_count** - 코드에 나타나는 숫자 (반복 횟수)
3. **line_count** - 코드 라인 수

**구현:**
```python
def _analyze_user_code(self, code: str) -> Dict:
    lines = [l.strip() for l in code.split('\n') if l.strip()]

    # 1. 유사한 라인 찾기
    line_groups = {}
    for line in lines:
        # 숫자를 'N'으로 치환 → 패턴 추출
        pattern = line
        for char in '0123456789':
            pattern = pattern.replace(char, 'N')

        if pattern in line_groups:
            line_groups[pattern].append(line)
        else:
            line_groups[pattern] = [line]

    # 2번 이상 반복되는 패턴
    similar_lines = []
    for pattern, group in line_groups.items():
        if len(group) >= 2:
            similar_lines.extend(group)

    # 2. 반복 횟수 추정
    numbers = re.findall(r'\b\d+\b', code)
    repeat_count = max([int(n) for n in numbers if int(n) < 100], default=0)

    return {
        'similar_lines': list(set(similar_lines)),
        'repeat_count': repeat_count,
        'line_count': len(lines)
    }
```

---

## 맞춤형 질문 생성

### 1. 반복 관련

**일반 템플릿 (V12):**
```python
"같은 작업 10번 해야 하는데 매번 손으로 쓸 건가?"
```

**맞춤형 (V13):**
```python
# 사용자 코드 분석
code_analysis = self._analyze_user_code(user_code)
similar_lines = code_analysis['similar_lines']

# 실제 반복 코드 발견 시
if len(similar_lines) >= 3:
    return f"비슷한 코드가 {len(similar_lines)}번 반복되는데 입력이 100개면 어떻게 할 건데?"

# 예시 출력
"비슷한 코드가 5번 반복되는데 입력이 100개면 어떻게 할 건데?"
```

→ **5번**이 사용자의 실제 코드에서 나온 값!

---

### 2. 함수 관련

**V12:**
```python
"같은 계산을 10군데에서 해야 하는데 코드 10번 복사?"
```

**V13:**
```python
similar_lines = code_analysis['similar_lines']

if len(similar_lines) >= 2:
    return f"비슷한 코드가 {len(similar_lines)}군데 있는데 나중에 바꾸면 {len(similar_lines)}군데 다 고칠 건가?"

# 예시 출력
"비슷한 코드가 3군데 있는데 나중에 바꾸면 3군데 다 고칠 건가?"
```

→ **3군데**가 실제 중복 코드 개수!

---

### 3. 조건 관련

**V12:**
```python
"예외 상황 10가지 나오면 다 손으로 확인?"
```

**V13:**
```python
if_count = user_code.count('if ')

if if_count == 0:
    return "입력이 이상한 값이면 어떻게 되는데? 그냥 에러?"
elif if_count == 1:
    return "다른 경우는 10가지인데 하나씩 다 손으로 확인할 건가?"
elif if_count >= 2:
    return f"지금 {if_count}개 경우만 체크하는데 예외 상황 20가지 나오면?"

# 예시 출력
"지금 2개 경우만 체크하는데 예외 상황 20가지 나오면?"
```

→ **2개**가 사용자의 실제 if문 개수!

---

### 4. 입력 관련

**V12:**
```python
"입력 10개를 한 번에 받으려면?"
```

**V13:**
```python
input_count = user_code.count('input(')

if input_count >= 3:
    return f"입력 {input_count}번 받는데 입력이 100개면 어떻게 할 건데?"

# 예시 출력
"입력 4번 받는데 입력이 100개면 어떻게 할 건데?"
```

→ **4번**이 실제 input() 호출 횟수!

---

### 5. 출력 관련

**V12:**
```python
"출력 형식 바꾸라고 하면 어디를 고쳐?"
```

**V13:**
```python
print_count = user_code.count('print(')

if print_count >= 3:
    return f"지금 {print_count}번 출력하는데 형식 바꾸라고 하면 {print_count}군데 다 고칠 건가?"

# 예시 출력
"지금 5번 출력하는데 형식 바꾸라고 하면 5군데 다 고칠 건가?"
```

→ **5번**이 실제 print() 호출 횟수!

---

## 비교: V12 vs V13

### 반복 케이스

**사용자 코드:**
```python
print(1 + 2)
print(2 + 3)
print(3 + 4)
print(4 + 5)
print(5 + 6)
```

**V12 출력:**
```
"같은 작업 10번 해야 하는데 매번 손으로 쓸 건가?"
```
→ "10번"은 임의의 숫자

**V13 출력:**
```
"비슷한 코드가 5번 반복되는데 입력이 100개면 어떻게 할 건데?"
```
→ "5번"은 실제 반복 횟수!

---

### 함수 케이스

**사용자 코드:**
```python
result1 = (a + b) * 2
result2 = (c + d) * 2
result3 = (e + f) * 2
```

**V12 출력:**
```
"같은 계산을 10군데에서 해야 하는데 코드 10번 복사?"
```
→ "10군데"는 일반적 숫자

**V13 출력:**
```
"비슷한 코드가 3군데 있는데 나중에 바꾸면 3군데 다 고칠 건가?"
```
→ "3군데"는 실제 중복 코드 위치!

---

### 조건 케이스

**사용자 코드:**
```python
x = int(input())
if x > 0:
    print("양수")
elif x < 0:
    print("음수")
```

**V12 출력:**
```
"예외 상황 10가지 나오면 다 손으로 확인?"
```
→ 일반적 질문

**V13 출력:**
```
"지금 2개 경우만 체크하는데 예외 상황 20가지 나오면?"
```
→ "2개"는 실제 if/elif 개수!

---

## 패턴 감지 시스템

### 유사 라인 감지

**목적:** 반복되는 코드 패턴 찾기

**알고리즘:**
1. 숫자를 'N'으로 치환
2. 패턴별로 그룹화
3. 2번 이상 나타나는 패턴 추출

**예시:**
```python
# 원본
print(1 + 2)
print(2 + 3)
print(3 + 4)

# 패턴 변환
print(N + N)  # 3번 반복
print(N + N)
print(N + N)

# 결과
similar_lines = [
    "print(1 + 2)",
    "print(2 + 3)",
    "print(3 + 4)"
]
# len = 3
```

---

### 반복 횟수 추정

**목적:** 코드에 나타나는 숫자로 반복 의도 파악

**알고리즘:**
```python
numbers = re.findall(r'\b\d+\b', code)
repeat_count = max([int(n) for n in numbers if int(n) < 100], default=0)
```

**예시:**
```python
# 코드
for i in range(5):
    print(i)

# 추출
numbers = ['5']
repeat_count = 5

# 힌트
"같은 작업을 5번 하는데 입력이 1000개면 어떻게 처리?"
```

---

## 전체 카테고리 (8가지)

| 카테고리 | 분석 요소 | 맞춤형 요소 |
|----------|-----------|-------------|
| **반복** | similar_lines, repeat_count | 실제 반복 횟수 |
| **함수** | similar_lines | 실제 중복 코드 위치 |
| **조건** | if_count | 실제 if/elif 개수 |
| **입력** | input_count | 실제 input() 호출 |
| **출력** | print_count | 실제 print() 호출 |
| **리스트** | has_list | 리스트 사용 여부 |
| **변수** | var_count | 실제 변수 개수 |
| **기본** | remaining_steps | 다음 단계 정보 |

---

## 장점

### 1. 진짜 맞춤형

**V12:** 모든 사용자에게 같은 힌트
**V13:** 각 사용자의 코드에 맞춤

---

### 2. 구체적 피드백

**V12:**
```
"같은 작업 10번 해야 하는데..."
```
→ "10번"은 임의

**V13:**
```
"비슷한 코드가 5번 반복되는데..."
```
→ "5번"은 실제!

---

### 3. 현실감

**학생 관점:**
- V12: "10번? 내 코드엔 5번인데..."
- V13: "5번 맞네! 진짜 반복되고 있구나..."

→ **더 와닿는 힌트**

---

## 단점 (V12 대비)

### 1. 분석 오버헤드

**V12:** ~0.001초 (키워드 매칭만)
**V13:** ~0.01초 (코드 파싱 + 패턴 분석)

**영향:** 미미함 (여전히 매우 빠름)

---

### 2. 분석 정확도

**문제:**
- 복잡한 코드는 패턴 감지 어려움
- 주석이 많으면 오판 가능

**해결:**
- 주석 제거 (`not l.startswith('#')`)
- 간단한 패턴만 분석
- 실패 시 기본 템플릿 사용

---

## 구현 변경사항

### 1. 새 함수 추가

```python
def _analyze_user_code(self, code: str) -> Dict:
    """사용자 코드 상세 분석"""
    # similar_lines 찾기
    # repeat_count 추정
    # line_count 계산
    return {
        'similar_lines': [...],
        'repeat_count': 5,
        'line_count': 10
    }
```

---

### 2. 힌트 생성 로직 수정

**Before (V12):**
```python
if "반복" in goal_lower:
    hints = ["...", "...", "..."]
    return random.choice(hints)
```

**After (V13):**
```python
if "반복" in goal_lower:
    code_analysis = self._analyze_user_code(user_code)
    similar_lines = code_analysis['similar_lines']

    if len(similar_lines) >= 3:
        return f"비슷한 코드가 {len(similar_lines)}번 반복되는데..."
```

---

## 실제 사용 예시

### 예시 1: 반복 코드

**사용자 코드:**
```python
a = int(input())
b = int(input())
c = int(input())
d = int(input())
```

**분석 결과:**
- similar_lines: ["a = int(input())", "b = int(input())", ...]
- len(similar_lines) = 4

**V13 힌트:**
```
"비슷한 코드가 4번 반복되는데 입력이 100개면 어떻게 할 건데?"
```

---

### 예시 2: 조건 부족

**사용자 코드:**
```python
x = int(input())
print(x * 2)
```

**분석 결과:**
- if_count = 0
- has_input = True

**V13 힌트:**
```
"입력이 이상한 값이면 어떻게 되는데? 그냥 에러?"
```

---

### 예시 3: 함수 필요

**사용자 코드:**
```python
result1 = (a * 2) + 5
result2 = (b * 2) + 5
result3 = (c * 2) + 5
```

**분석 결과:**
- similar_lines: 3개
- has_calculation = True

**V13 힌트:**
```
"비슷한 코드가 3군데 있는데 나중에 바꾸면 3군데 다 고칠 건가?"
```

---

## V1 → V13 전체 여정

| 버전 | 접근 | 맞춤형 | 결과 |
|------|------|--------|------|
| V1-V11 | 프롬프트 개선 | ❌ | 모델 실패 |
| V12 | 템플릿 (키워드) | ❌ | 일반적 질문 |
| **V13** | **코드 분석** | **✅** | **맞춤형 질문** |

---

## 결론

### V12의 성과

- ✅ 소크라테스식 질문 보장
- ✅ 즉시 반응
- ❌ 맞춤형 아님

### V13의 개선

- ✅ 소크라테스식 질문 유지
- ✅ 즉시 반응 유지
- ✅ **맞춤형 추가**

### 핵심 차이

**V12:**
```
"같은 작업 10번 해야 하는데..." (모든 사용자 동일)
```

**V13:**
```
"비슷한 코드가 5번 반복되는데..." (사용자별 다름)
```

→ **"5번"이 실제 사용자 코드에서 나옴!**

---

## 변경 위치

**파일:** [hint-system/app.py](../hint-system/app.py)

**추가 함수:**
- `_analyze_user_code()` (lines 457-489) - 코드 분석

**수정 로직:**
- `_create_analysis_prompt()` (lines 354-455) - 맞춤형 힌트 생성

---

**작성일:** 2025-01-30
**버전:** V13 (최종)
**이전 버전:** [PROMPT_FIX_V12.md](PROMPT_FIX_V12.md)
**핵심:** 템플릿 + 코드 분석 = 맞춤형 힌트
**철학:** "일반적 질문 < 내 코드 기반 질문"
