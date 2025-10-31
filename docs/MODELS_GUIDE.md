# 모델 가이드

## 모델 선택 전략

### Coder 모델의 한계 발견

**문제:**
- Qwen2.5-**Coder**-1.5B, DeepSeek-**Coder** 등은 코드 작성/디버깅에 특화
- 프롬프트에 코드가 없어도 질문 대신 **코드 예시를 생성**하는 경향
- 소크라테스식 질문 생성에 부적합

**V10 테스트 결과 (Qwen2.5-Coder-1.5B):**
```python
def add_numbers(a, b):
    # 여기에 함수 정의를 추가하세요
```
→ 여전히 코드 생성

---

## 추천 모델 (질문 생성 특화)

### 1. Chat/Instruction 모델 (우선)

질문 생성에 적합한 대화 특화 모델:

| 모델 | 크기 | 특징 | 추천도 |
|------|------|------|--------|
| **Qwen2.5-1.5B-Instruct** | 1.5B | 대화 특화, 한국어 지원 | ⭐⭐⭐⭐⭐ |
| **Phi-3.5-mini-Instruct** | 3.8B (4-bit) | Microsoft, 지시 따르기 우수 | ⭐⭐⭐⭐⭐ |
| **Gemma-2-2B-Instruct** | 2B | Google, 안전한 출력 | ⭐⭐⭐⭐ |
| **TinyLlama-1.1B-Chat** | 1.1B | 초경량, 빠름 | ⭐⭐⭐ |

---

### 2. Coder 모델 (참고용)

코드 작성에는 좋지만 질문 생성에는 부적합:

| 모델 | 크기 | 특징 | 추천도 |
|------|------|------|--------|
| Qwen2.5-Coder-1.5B | 1.5B | 코드 디버깅 특화 | ⭐⭐ |
| DeepSeek-Coder-1.3B | 1.3B | 코드 완성 특화 | ⭐⭐ |
| Phi-2-2.7B (4-bit) | 2.7B | 코드/수학 특화 | ⭐⭐ |

---

## 모델별 상세 설명

### ⭐⭐⭐⭐⭐ Qwen2.5-1.5B-Instruct

**경로:** `Qwen/Qwen2.5-1.5B-Instruct`

**특징:**
- **Chat/Instruction 특화** - Coder 버전이 아님
- 다국어 지원 (한국어 포함)
- 대화, 질문 생성에 최적화
- 1.5B로 가벼움

**장점:**
- Coder 모델처럼 코드 생성 강요 없음
- 자연스러운 질문 생성
- 한국어 성능 우수

**단점:**
- Coder 버전보다 코드 이해력은 낮을 수 있음
- 하지만 힌트 생성에는 오히려 유리

**사용 예시:**
```python
{
    "name": "Qwen2.5-1.5B-Instruct",
    "path": "Qwen/Qwen2.5-1.5B-Instruct",
    "quantize": False,
    "size": "1.5B",
    "type": "chat"
}
```

---

### ⭐⭐⭐⭐⭐ Phi-3.5-mini-Instruct

**경로:** `microsoft/Phi-3.5-mini-instruct`

**특징:**
- Microsoft의 소형 언어 모델
- 3.8B지만 4-bit 양자화로 경량화
- **지시 따르기** 성능 우수
- 안전한 출력 (Microsoft Safety)

**장점:**
- 프롬프트 지시를 정확히 따름
- "코드 작성 금지" 같은 제약 잘 지킴
- 4-bit로 메모리 1/4 절약

**단점:**
- 한국어 성능은 Qwen보다 낮을 수 있음
- 4-bit 양자화 시 약간의 품질 저하

**사용 예시:**
```python
{
    "name": "Phi-3.5-mini-Instruct",
    "path": "microsoft/Phi-3.5-mini-instruct",
    "quantize": True,  # 4-bit 양자화
    "size": "3.8B (4-bit)",
    "type": "chat"
}
```

---

### ⭐⭐⭐⭐ Gemma-2-2B-Instruct

**경로:** `google/gemma-2-2b-it`

**특징:**
- Google의 경량 모델
- 2B 크기로 중간 성능
- 안전한 출력 보장
- Instruction tuning 버전

**장점:**
- Google 품질 보증
- 윤리적/안전한 출력
- 균형잡힌 성능

**단점:**
- 한국어 성능 제한적
- Qwen/Phi보다 속도 느릴 수 있음

**사용 예시:**
```python
{
    "name": "Gemma-2-2B-Instruct",
    "path": "google/gemma-2-2b-it",
    "quantize": False,
    "size": "2B",
    "type": "chat"
}
```

---

### ⭐⭐⭐ TinyLlama-1.1B-Chat

**경로:** `TinyLlama/TinyLlama-1.1B-Chat-v1.0`

**특징:**
- 초경량 1.1B
- Chat 버전
- 매우 빠른 추론 속도

**장점:**
- 가장 가벼움
- CPU에서도 빠름
- 메모리 사용량 최소

**단점:**
- 성능이 가장 낮음
- 한국어 지원 제한적
- 복잡한 지시 이해 어려움

**사용 예시:**
```python
{
    "name": "TinyLlama-1.1B-Chat",
    "path": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "quantize": False,
    "size": "1.1B",
    "type": "chat"
}
```

---

## Chat vs Coder 모델 비교

### 힌트 생성 작업 특성

**요구 사항:**
1. 한국어 반말 질문 생성
2. 코드가 아닌 **상황 설명**
3. 소크라테스식 질문

---

### Chat 모델의 장점

| 특성 | Chat 모델 | Coder 모델 |
|------|-----------|------------|
| **질문 생성** | ✅ 특화됨 | ❌ 코드 생성 우선 |
| **대화 능력** | ✅ 우수 | △ 보통 |
| **지시 따르기** | ✅ 우수 | △ 보통 |
| **코드 회피** | ✅ 코드 생성 안 함 | ❌ 코드 생성 경향 |
| **한국어** | ✅ 지원 | △ 제한적 |

---

### Coder 모델의 문제점

**V9 테스트 (Qwen2.5-Coder):**
```
N, M = map(int, input().split())
board = []
...
```
→ 질문 대신 코드 생성

**V10 테스트 (Qwen2.5-Coder):**
```python
def add_numbers(a, b):
    # 여기에 함수 정의를 추가하세요
```
→ 여전히 코드 생성

**결론:** Coder 모델은 프롬프트에 관계없이 **코드 생성 모드**로 동작

---

## 메모리 사용량 비교

| 모델 | 정밀도 | 예상 메모리 |
|------|--------|------------|
| TinyLlama-1.1B | FP16 | ~2.2GB |
| Qwen2.5-1.5B-Instruct | FP16 | ~3GB |
| Gemma-2-2B | FP16 | ~4GB |
| Phi-3.5-mini (4-bit) | 4-bit | ~2.5GB |
| DeepSeek-Coder-1.3B | FP16 | ~2.6GB |
| Qwen2.5-Coder-1.5B | FP16 | ~3GB |
| Phi-2-2.7B (4-bit) | 4-bit | ~1.7GB |

**권장 메모리:**
- 최소: 8GB RAM (TinyLlama, 4-bit 모델)
- 권장: 16GB RAM (1.5B-2B 모델 2-3개)
- 이상적: 32GB RAM (모든 모델 동시)

---

## 추천 조합

### 1. 균형 조합 (16GB RAM)

```python
- Qwen2.5-1.5B-Instruct  # 한국어 특화
- Phi-3.5-mini-Instruct (4-bit)  # 지시 따르기
- TinyLlama-1.1B-Chat  # 빠른 테스트용
```

**총 메모리:** ~7.7GB

---

### 2. 고성능 조합 (32GB RAM)

```python
- Qwen2.5-1.5B-Instruct  # 한국어 특화
- Phi-3.5-mini-Instruct (4-bit)  # 지시 따르기
- Gemma-2-2B-Instruct  # Google 품질
- TinyLlama-1.1B-Chat  # 빠른 추론
```

**총 메모리:** ~11.7GB

---

### 3. 경량 조합 (8GB RAM)

```python
- TinyLlama-1.1B-Chat  # 초경량
- Phi-3.5-mini-Instruct (4-bit)  # 지시 따르기
```

**총 메모리:** ~4.7GB

---

## 모델 선택 가이드

### 한국어 성능 중요 → Qwen2.5-1.5B-Instruct

**이유:**
- Qwen 시리즈는 다국어 특화
- 한국어 자연스러움
- 1.5B로 가벼움

---

### 프롬프트 준수 중요 → Phi-3.5-mini-Instruct

**이유:**
- Microsoft의 지시 따르기 특화
- "코드 금지" 같은 제약 잘 지킴
- 4-bit로 메모리 효율적

---

### 속도 중요 → TinyLlama-1.1B-Chat

**이유:**
- 가장 가벼움 (1.1B)
- 추론 속도 빠름
- 성능은 낮지만 실시간 테스트 가능

---

### 품질 중요 → Gemma-2-2B-Instruct

**이유:**
- Google 품질 보증
- 안전하고 윤리적 출력
- 2B로 성능 우수

---

## Coder 모델을 피해야 하는 이유

### 1. 코드 생성 우선순위

**Coder 모델의 학습 목적:**
- 코드 완성
- 디버깅
- 코드 설명

**힌트 생성과의 충돌:**
- 질문 생성 < 코드 생성
- 대화 능력 낮음
- 프롬프트 지시 무시

---

### 2. 테스트 결과

| 프롬프트 버전 | Coder 모델 결과 | Chat 모델 기대 |
|---------------|-----------------|----------------|
| V9 (코드 포함) | 코드 디버깅 | 질문 생성 |
| V10 (코드 제거) | 코드 예시 생성 | 질문 생성 |

---

### 3. 결론

**Coder 모델:**
- ❌ 질문 생성 부적합
- ✅ 코드 작성 특화
- 💡 사용처: 코드 완성, 디버깅

**Chat 모델:**
- ✅ 질문 생성 특화
- ✅ 대화 능력 우수
- 💡 사용처: 힌트 생성, 소크라테스 학습

---

## 현재 시스템의 모델 목록

```python
# Chat/Instruction 모델 (우선 사용)
1. Qwen2.5-1.5B-Instruct (💬 Chat)
2. Phi-3.5-mini-Instruct (💬 Chat, 4-bit)
3. Gemma-2-2B-Instruct (💬 Chat)
4. TinyLlama-1.1B-Chat (💬 Chat)

# Coder 모델 (참고용)
5. Qwen2.5-Coder-1.5B (💻 Coder)
6. DeepSeek-Coder-1.3B (💻 Coder)
7. Phi-2-2.7B (💻 Coder, 4-bit)
```

**권장:** 1-4번 Chat 모델 사용

---

## 사용 방법

### Gradio UI에서

1. **모델 선택** 섹션에서 체크박스 선택
2. 💬 마크가 있는 모델 우선 선택
3. 여러 모델 선택 가능 (비교용)

### 예시

```
☑️ 💬 Qwen2.5-1.5B-Instruct
☑️ 💬 Phi-3.5-mini-Instruct
☐ 💬 Gemma-2-2B-Instruct
☑️ 💬 TinyLlama-1.1B-Chat
☐ 💻 Qwen2.5-Coder-1.5B
```

→ 3개 Chat 모델로 힌트 생성 및 비교

---

## 향후 개선 방향

### 1. Chat 모델 테스트

V10 프롬프트를 Chat 모델로 테스트:
- Qwen2.5-1.5B-Instruct
- Phi-3.5-mini-Instruct

### 2. 프롬프트 최적화

Chat 모델 특성에 맞춰:
- 더 간결한 명령
- 역할극 강화 ("너는 선생님")
- 예시 최소화

### 3. 한국어 모델 추가

한국어 특화 모델 고려:
- KoAlpaca
- Polyglot-Ko
- 하지만 메모리 사용량 확인 필요

---

**작성일:** 2025-01-30
**목적:** Coder 모델 한계 파악 및 Chat 모델 추천
**핵심:** 질문 생성 = Chat 모델, 코드 작성 = Coder 모델
