# 변경사항 (2025-10-31)

## 개요
Runpod H100 PCIe 32GB/86GB 환경에 최적화된 모델들을 추가하고, 소크라테스 학습법 기반의 반말 힌트 생성으로 프롬프트를 개선했습니다.

---

## 주요 변경사항

### 1. 모델 구성 대폭 확장 (model_config.py)

#### Chat 모델 (소크라테스 질문 생성 특화)
- **Qwen2.5-32B-Instruct** (4-bit) - 20GB VRAM
  - 대형 Chat 모델, 소크라테스 질문 생성에 최적
- **Qwen2.5-14B-Instruct** (full) - 28GB VRAM
  - 중형 Chat 모델, 안정적인 질문 생성
- **Llama-3.1-8B-Instruct** (full) - 16GB VRAM
  - Meta Llama 3.1, 긴 context (131K) 지원
- **Mistral-7B-Instruct-v0.3** (full) - 14GB VRAM
  - Mistral 7B, 균형잡힌 성능

#### Coder 모델 (코드 분석 특화)
- **Qwen2.5-Coder-32B** (4-bit) - 20GB VRAM
  - 대형 코딩 모델, 정확한 코드 분석
- **DeepSeek-Coder-33B** (4-bit) - 20GB VRAM
  - DeepSeek 대형 코딩 모델
- **CodeLlama-34B** (4-bit) - 21GB VRAM
  - Meta CodeLlama 34B

#### 경량 비교 모델
- **Qwen2.5-7B-Instruct** (full) - 14GB VRAM
- **Qwen2.5-3B-Instruct** (full) - 6GB VRAM

**총 9개 모델** (기존 5개 → 9개)

---

### 2. 프롬프트 개선 (app.py - _create_analysis_prompt)

#### Before (기존 V16 프롬프트)
```python
prompt = f"""학생이 "{next_step_goal}" 못함.
코드: 비슷한 줄 {similar_count}개, if {if_count}개, input {input_count}번

질문 예시:
Q: "같은 코드 10번 복사하면 나중에 10군데 다 고쳐야 하는 거 아냐?"
Q: "입력 100개면 손으로 100줄 쓸 거야?"
Q: "계산 5번 반복하는데 숫자만 다르면?"

Q:"""
```

#### After (소크라테스 학습법 + 반말)
```python
prompt = f"""너는 프로그래밍 멘토야. 학생이 문제를 풀다가 막혔어.
절대 답을 직접 알려주지 마. 소크라테스 학습법을 사용해서 학생 스스로 생각하게 만들어야 해.

## 문제 상황
- 학생이 막힌 단계: {next_step_goal}
- 이미 완료한 부분: {completed_desc}
- 아직 구현 안 된 부분: {missing_desc}

## 학생 코드 현황
- 반복되는 패턴: {similar_count}개 라인
- 조건문: {if_count}개
- 반복문: for {for_count}개, while {while_count}개
- 입력/출력: input {input_count}번, print {print_count}번

## 힌트 생성 원칙
1. **질문 형태로만 답해** - "어떻게 ~할까?" "~하면 어떻게 될까?" "~를 사용하면?"
2. **답을 직접 말하지 마** - 코드, 변수명, 함수명 절대 언급 금지
3. **학생이 다음 단계를 떠올리게 유도** - "{next_step_goal}"를 스스로 깨닫게
4. **반말 사용** - 친근하고 편안한 톤으로
5. **짧고 명확하게** - 한 문장, 최대 2문장

## 좋은 힌트 예시 (반말)
- "같은 코드를 10번 복사하면 나중에 수정할 때 10군데 다 고쳐야 하는 거 아냐?"
- "입력이 100개면 손으로 100줄 쓸 거야?"
- "숫자만 바뀌고 똑같은 계산을 5번 반복한다면?"
- "지금 조건이 2개인데, 3개, 4개... 100개로 늘어나면 어떻게 해?"
- "이 값을 나중에 또 써야 하는데 어디에 기억해둘까?"
- "처음부터 끝까지 다 확인해야 하는데 어떻게 하면 자동으로 넘어갈까?"

## 나쁜 힌트 예시 (절대 금지!)
- "for 반복문을 사용하세요" (답을 직접 말함)
- "count_repaint 함수를 만드세요" (함수명 언급)
- "range()를 써보세요" (코드 직접 제시)
- "정답 코드에서는 ..." (정답 언급)

## 학생이 막힌 부분: {next_step_goal}

학생에게 던질 소크라테스식 질문 (반말, 물음표로 끝):"""
```

**주요 개선점:**
- ✅ 상세한 문제 상황 설명 (학생이 막힌 단계, 완료/미완료 부분)
- ✅ 코드 현황 상세 분석 (조건문, 반복문, 입출력 횟수)
- ✅ 명확한 5가지 원칙 제시
- ✅ 좋은 예시 6개, 나쁜 예시 4개로 확대
- ✅ 반말 톤 강제

---

### 3. 프롬프트 후처리 강화 (model_inference.py - _extract_hint_from_output)

#### 추가된 필터링
1. **존댓말 필터링**
   - `~세요`, `~시`, `~습니다`, `~입니다` 포함 시 필터링
   - 질문 끝이 `~요?`, `~세요?`, `~까요?`인 경우 필터링

2. **반말 종결 확인**
   ```python
   # 올바른 반말 종결: ~야?, ~니?, ~까?, ~ㄹ까?, ~거야?, ~는 거야?, ~냐?, ~을까?
   # 잘못된 존댓말: ~요?, ~세요?, ~까요?
   if sentence.endswith('?'):
       formal_endings = ['요?', '세요?', '까요?', '습니까?', '입니까?']
       if any(sentence.endswith(ending) for ending in formal_endings):
           print(f"[DEBUG] 존댓말 종결 필터링: {sentence[:50]}...")
           continue
   ```

---

### 4. UI 개선 (app.py - setup_default_models)

#### Before
```python
print(f"[{model_type_label}] {model_info['name']} 설정 중...")
if model_info.get('quantize'):
    print(f"  → 4-bit 양자화 사용 (메모리 1/4 절약)")
```

#### After
```python
model_type_label = "💬 Chat" if model_info.get('type') == 'chat' else "💻 Coder"

print(f"\n[{model_type_label}] {model_info['name']} 설정 중...")
print(f"  ├─ 크기: {model_info['size']}")
if model_info.get('quantize'):
    print(f"  └─ 4-bit 양자화 사용 (메모리 절약)")
```

**개선점:**
- 이모지로 Chat/Coder 구분
- 모델 크기 명시
- 우선순위 기반 정렬

---

## 힌트 생성 플로우

```
사용자 코드 입력
    ↓
코드 분석 (_analyze_user_code)
    ↓
Logic 단계 매칭 (_find_best_matching_solution)
    ↓
막힌 단계 파악 (completed_step, next_step_goal)
    ↓
소크라테스 프롬프트 생성 (_create_analysis_prompt)
    ↓
모델 추론 (generate_hint)
    ↓
후처리 (_extract_hint_from_output)
    ├─ 존댓말 필터링
    ├─ 반말 종결 확인
    ├─ 코드/함수명 언급 제거
    └─ 질문 형태만 추출
    ↓
사용자에게 반말 힌트 제공
```

---

## 기대 효과

### 1. 모델 성능 향상
- **기존**: 3B~14B 소형 모델 위주
- **개선**: 32B~34B 대형 모델 추가 (4-bit 양자화로 메모리 효율화)
- **결과**: 더 정확하고 맥락을 이해하는 힌트 생성

### 2. 힌트 품질 개선
- **기존**: 짧은 Few-shot 예시만 제공
- **개선**: 상세한 원칙 + 좋은/나쁜 예시 + 학생 상황 분석
- **결과**: 소크라테스 학습법에 맞는 질문 형태 힌트

### 3. 사용자 경험 개선
- **기존**: 존댓말 힌트 (딱딱함)
- **개선**: 반말 힌트 (친근함)
- **결과**: 학습자가 편하게 받아들일 수 있는 톤

---

## 디스크 공간 요구사항

| 모델 | 크기 | 타입 | 우선순위 |
|------|------|------|----------|
| Qwen2.5-32B-Instruct (4-bit) | ~20GB | Chat | ⭐ 1 |
| Qwen2.5-14B-Instruct | ~28GB | Chat | 2 |
| Llama-3.1-8B-Instruct | ~16GB | Chat | 3 |
| Mistral-7B-Instruct-v0.3 | ~14GB | Chat | 4 |
| Qwen2.5-Coder-32B (4-bit) | ~20GB | Coder | 5 |
| DeepSeek-Coder-33B (4-bit) | ~20GB | Coder | 6 |
| Qwen2.5-7B-Instruct | ~14GB | Chat | 7 |
| Qwen2.5-3B-Instruct | ~6GB | Chat | 8 |

**총 디스크 공간: ~130-150GB**

---

## 실행 방법

```bash
cd /workspace/proj_hint_system/hint-system
python app.py
```

앱 실행 시 모델들이 자동으로 다운로드됩니다.
- H100 PCIe 32GB 기준: 1~2개 모델 동시 로드 가능
- 순차 로드 방식으로 메모리 관리

---

## 추가 개선사항 (2025-10-31 오후)

### 문제: 일관성 없는 힌트 생성
- 같은 사용자 코드에 대해 매번 다른 힌트 생성
- 중국어/일본어 출력 발생
- 좋은 질문도 30자 필터에 걸림

### 해결책

#### 1. Temperature 제한 (model_inference.py:127)
```python
# Before: temperature=0.8 (너무 높음)
temperature=max(0.3, min(temperature, 0.5))  # 0.3~0.5로 강제 제한
```

#### 2. UI 슬라이더 범위 축소 (app.py:706-714)
```python
# Before: 0.1~1.0, default=0.8
minimum=0.3, maximum=0.5, value=0.4  # 일관성 향상
```

#### 3. 첫 질문 빠른 통과 로직 (model_inference.py:175-196)
```python
# 첫 물음표까지 추출 후, 15자 이상이고 한국어 60% 이상이면 즉시 반환
# 30자 필터 등 복잡한 검증 skip
if len(clean) >= 15 and korean_ratio >= 0.6 and not formal_ending:
    return clean  # ✅ 바로 통과
```

#### 4. 질문 형태 우대 (model_inference.py:337-340)
```python
# Before: 모든 문장 30자 이상 필요
# After: 질문(?)이면 15자만 있어도 OK
min_length = 15 if sentence.endswith('?') else 30
```

#### 5. 생성 토큰 수 증가 (model_inference.py:126)
```python
# Before: max_new_tokens=30 (너무 짧음)
max_new_tokens=50  # 완전한 질문 생성 가능
```

---

## 기대 효과

### Before
```
temperature=0.8 → 매번 다른 답변
- "똑같은 작업을 여러 번 할 때마다..."
- "같은 동작을 여러 번 반복하면서..."
- "同じコードを何度も書く..." (일본어)
- "똑같은 작업을 여러 번 할 때마다 같은 코드를 계속重复相同的工作时..." (중국어 혼입)
```

### After
```
temperature=0.3~0.5 → 일관적인 답변
- "같은 작업을 여러 번 할 때마다 코드를 다시 적어야 하나?"
- "같은 작업을 여러 번 할 때마다 코드를 다시 적어야 하나?"
- "같은 작업을 여러 번 할 때마다 코드를 다시 적어야 하나?"
```

---

## 다음 단계 (선택사항)

1. **vLLM 서버 설정** (선택)
   - 더 빠른 추론 속도를 원할 경우
   - 여러 모델을 동시에 서빙

2. **평가 자동화**
   - 생성된 힌트의 품질 자동 평가
   - 반말/존댓말 비율 체크

3. **Few-shot 예시 추가**
   - 실제 평가 결과에서 좋은 힌트를 Few-shot으로 추가
   - 모델별 특성에 맞는 예시 커스터마이징

---

## 문의
문제가 발생하면 팀원에게 문의하세요.
