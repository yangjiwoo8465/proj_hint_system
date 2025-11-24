# 개인화된 힌트 시스템 - 요구사항 정의서

## 1. 프로젝트 개요

### 1.1 목적
코딩 테스트 플랫폼에서 사용자의 실력 수준에 따라 개인화된 힌트를 제공하여 효과적인 학습 경험을 제공하는 시스템

### 1.2 범위
- 사용자 실력 지표 자동/수동 관리
- 실력 수준에 따른 3단계 힌트 시스템
- 문제 풀이 세션 추적 및 분석
- 관리자 패널을 통한 사용자 관리

## 2. 기능 요구사항

### 2.1 사용자 실력 지표 관리

#### 2.1.1 실력 점수 (Skill Score)
- **범위**: 0~100 (Float)
- **의미**: 높을수록 초보, 낮을수록 실력자
- **기본값**: 50.0
- **계산 방식**: 최근 10개 문제 풀이 세션의 난이도 점수 평균

#### 2.1.2 실력 모드 (Skill Mode)
**자동 모드 (auto)**
- 문제를 풀 때마다 실력 점수가 자동으로 업데이트됨
- 실력 점수에 따라 힌트 레벨이 자동 조정됨
- 관리자가 실력 점수와 힌트 레벨을 수정할 수 없음

**수동 모드 (manual)**
- 관리자가 설정한 값으로 고정됨
- 문제를 풀어도 자동 업데이트되지 않음
- 관리자가 실력 점수와 힌트 레벨을 직접 수정 가능

#### 2.1.3 힌트 레벨 (Hint Level)
- **레벨 1 (기초)**: 실력 점수 70 이상
- **레벨 2 (보통)**: 실력 점수 40~70
- **레벨 3 (실력자)**: 실력 점수 40 미만

### 2.2 문제 풀이 세션 추적 (ProblemSession)

#### 2.2.1 시간 추적
- `started_at`: 문제 선택 시점
- `first_hint_at`: 첫 힌트 요청 시점
- `first_run_at`: 첫 코드 실행 시점
- `solved_at`: 문제 해결 시점

#### 2.2.2 행동 추적
- `hint_count`: 힌트 요청 횟수
- `run_count`: 코드 실행 횟수
- `max_code_length`: 작성한 최대 코드 길이

#### 2.2.3 난이도 점수 계산 알고리즘
```
총점 = 0~100 (높을수록 어려워함)

1. 힌트 요청 시간 점수:
   - 1분 이내: +30점
   - 5분 이내: +20점
   - 10분 이내: +10점

2. 힌트 요청 횟수:
   - 횟수 × 10 (최대 30점)

3. 코드 실행 횟수:
   - 횟수 × 3 (최대 20점)

4. 코드 길이 점수:
   - 50자 미만: +20점
   - 100자 미만: +10점
```

### 2.3 개인화된 힌트 시스템

#### 2.3.1 레벨 1 (기초 - 구체적 힌트)
**대상**: 실력 점수 70 이상 (초보자)

**특징**:
- 필요한 함수명, 라이브러리, 메서드를 직접 언급
- 단계별 구체적인 코드 작성 방법 제시
- 150자 이내로 간단명료하게 제공

**예시**:
```
✅ "N줄을 입력받으려면 for _ in range(N)을 사용하고,
   각 줄을 list()로 변환해서 board에 append() 하세요."

✅ "문자열을 리스트로 변환하려면 list(input())을 사용하세요."
```

#### 2.3.2 레벨 2 (보통 - 개념 힌트)
**대상**: 실력 점수 40~70 (중급자)

**특징**:
- 함수명을 직접 언급하지 않고 개념으로 유도
- 필요한 자료구조나 알고리즘 개념 안내
- 180자 이내로 제공

**예시**:
```
✅ "N줄의 보드를 저장하려면 2차원 리스트가 필요합니다.
   반복문으로 각 줄을 입력받아 추가하세요."

✅ "입력받은 문자열을 한 글자씩 접근 가능한 형태로 바꿔야 합니다."
```

#### 2.3.3 레벨 3 (실력자 - 소크라테스식)
**대상**: 실력 점수 40 미만 (고급자)

**특징**:
- 질문 형식으로만 힌트 제공
- 학생이 스스로 답을 찾도록 유도
- 한 번에 하나의 질문만 (200자 이내)
- 평가나 분석 내용 포함하지 않음

**예시**:
```
✅ "전체 보드의 상태를 어떻게 입력받아 저장할 수 있을까요?"

❌ "학생이 입력을 받는 부분까지 올바르게 작성했습니다.
   이제 다음 단계는 보드 상태를 받아와야 합니다.
   어떻게 받을 수 있을까요?"
```

### 2.4 관리자 패널

#### 2.4.1 사용자 관리 기능
- 모든 사용자 목록 조회
- 사용자별 실력 지표 확인:
  - 실력 점수
  - 실력 모드 (자동/수동)
  - 힌트 레벨
  - 레이팅
  - 활성 상태

#### 2.4.2 실력 지표 수정 기능
- "실력 수정" 버튼 클릭 → 편집 모드 진입
- 수정 가능 항목:
  - **실력 모드**: 자동 ↔ 수동 전환
  - **실력 점수**: 수동 모드일 때만 수정 가능
  - **힌트 레벨**: 수동 모드일 때만 수정 가능
- 저장/취소 버튼으로 변경사항 적용/취소

#### 2.4.3 사용자 상태 관리
- 사용자 활성화/비활성화
- 사용자 삭제

## 3. 비기능 요구사항

### 3.1 성능 요구사항
- 힌트 생성 응답 시간: 30초 이내 (Hugging Face API timeout)
- 사용자 목록 조회: 1초 이내
- 실력 지표 업데이트: 1초 이내

### 3.2 보안 요구사항
- 관리자 API는 IsAdminUser 권한 필요
- 일반 사용자는 자신의 실력 지표를 볼 수 없음
- 실력 지표 수정은 관리자만 가능

### 3.3 사용성 요구사항
- 인라인 편집으로 빠른 수정 가능
- 자동 모드일 때는 수정 불가 필드가 시각적으로 구분됨 (disabled)
- 실력 지표 안내 패널로 시스템 이해도 향상

### 3.4 확장성 요구사항
- ProblemSession 모델은 향후 다양한 행동 추적 메트릭 추가 가능
- 난이도 점수 계산 알고리즘은 조정 가능하도록 설계

## 4. 데이터 모델

### 4.1 User 모델 (확장)
```python
class User(AbstractUser):
    # 기존 필드
    email: EmailField (unique)
    role: CharField ('user' | 'admin')
    rating: IntegerField (default=0)
    tendency: CharField ('perfectionist' | 'iterative' | 'unknown')

    # 실력 지표 필드 (신규)
    skill_score: FloatField (default=50.0, range: 0~100)
    skill_mode: CharField ('auto' | 'manual', default='auto')
    hint_level: IntegerField (1|2|3, default=2)

    created_at: DateTimeField
    updated_at: DateTimeField
```

### 4.2 ProblemSession 모델 (신규)
```python
class ProblemSession(Model):
    user: ForeignKey(User)
    problem: ForeignKey(Problem)

    # 시간 추적
    started_at: DateTimeField
    first_hint_at: DateTimeField (nullable)
    first_run_at: DateTimeField (nullable)
    solved_at: DateTimeField (nullable)

    # 행동 추적
    hint_count: IntegerField (default=0)
    run_count: IntegerField (default=0)
    max_code_length: IntegerField (default=0)

    # 결과
    is_solved: BooleanField (default=False)

    # unique_together = ['user', 'problem']
```

## 5. API 명세

### 5.1 힌트 요청 API
```
POST /api/v1/coding-test/hint/
Authorization: Required (IsAuthenticated)

Request:
{
  "problem_id": "string",
  "user_code": "string"
}

Response:
{
  "success": true,
  "data": {
    "hint": "string",
    "problem_id": "string"
  }
}

Process:
1. request.user.hint_level 조회
2. hint_level에 따라 다른 프롬프트 생성
3. Hugging Face API 호출
4. HintRequest 기록 저장
5. 힌트 반환
```

### 5.2 관리자 - 사용자 목록 조회
```
GET /api/v1/admin/users/
Authorization: Required (IsAdminUser)

Response:
{
  "success": true,
  "data": [
    {
      "id": 1,
      "username": "string",
      "email": "string",
      "rating": 0,
      "is_active": true,
      "is_staff": false,
      "is_superuser": false,
      "created_at": "ISO8601",
      "skill_score": 50.0,
      "skill_mode": "auto",
      "hint_level": 2
    }
  ]
}
```

### 5.3 관리자 - 실력 지표 업데이트
```
PATCH /api/v1/admin/users/{user_id}/skill/
Authorization: Required (IsAdminUser)

Request:
{
  "skill_score": 75.5,
  "skill_mode": "manual",
  "hint_level": 1
}

Response:
{
  "success": true,
  "message": "사용자 실력 지표가 업데이트되었습니다.",
  "data": {
    "id": 1,
    "username": "string",
    "skill_score": 75.5,
    "skill_mode": "manual",
    "hint_level": 1
  }
}

Validation:
- skill_mode: 'auto' | 'manual'만 허용
- hint_level: 1|2|3만 허용
- skill_score: 0~100 범위
```

### 5.4 관리자 - 사용자 상태 업데이트
```
PATCH /api/v1/admin/users/{user_id}/
Authorization: Required (IsAdminUser)

Request:
{
  "is_active": false
}

Response:
{
  "success": true,
  "message": "사용자 정보가 업데이트되었습니다."
}
```

### 5.5 관리자 - 사용자 삭제
```
DELETE /api/v1/admin/users/{user_id}/delete/
Authorization: Required (IsAdminUser)

Response:
{
  "success": true,
  "message": "사용자가 삭제되었습니다."
}
```

## 6. 사용자 인터페이스

### 6.1 관리자 패널 - 사용자 관리 탭

#### 6.1.1 테이블 컬럼
| 컬럼명 | 표시 내용 | 비고 |
|--------|-----------|------|
| 사용자명 | username | - |
| 이메일 | email | - |
| 레이팅 | rating | 기존 점수 시스템 |
| 실력 점수 | skill_score | 0~100, 소수점 1자리 |
| 실력 모드 | skill_mode | 배지 형태 (자동/수동) |
| 힌트 레벨 | hint_level | 배지 형태 (레벨 1/2/3) |
| 상태 | is_active | 활성/비활성 |
| 관리 | 버튼 그룹 | 실력 수정/활성화/삭제 |

#### 6.1.2 편집 모드
- "실력 수정" 버튼 클릭 시:
  - 실력 점수 → number input (0~100, step 0.1)
  - 실력 모드 → select (자동/수동)
  - 힌트 레벨 → select (레벨 1/2/3)
  - 버튼 → 저장/취소

- 자동 모드 선택 시:
  - 실력 점수 input disabled
  - 힌트 레벨 select disabled
  - 배경색 회색으로 변경

#### 6.1.3 실력 지표 안내 패널
하단에 3개 항목으로 구성된 안내 패널:
1. **실력 점수 (0~100)**: 계산 방식 설명
2. **실력 모드**: 자동/수동 차이 설명
3. **힌트 레벨**: 각 레벨별 힌트 스타일 설명

## 7. 시스템 흐름

### 7.1 자동 모드 - 실력 지표 갱신 흐름
```
1. 사용자가 문제 풀이 시작
   ↓
2. ProblemSession 생성 (started_at 기록)
   ↓
3. 힌트 요청 시
   - first_hint_at 기록 (첫 요청인 경우)
   - hint_count 증가
   ↓
4. 코드 실행 시
   - first_run_at 기록 (첫 실행인 경우)
   - run_count 증가
   - max_code_length 업데이트
   ↓
5. 문제 해결 시
   - solved_at 기록
   - is_solved = True
   - user.update_skill_score() 호출
   ↓
6. update_skill_score() 메서드
   - skill_mode가 'auto'인지 확인
   - 최근 10개 세션의 난이도 점수 계산
   - 평균 점수로 skill_score 업데이트
   - 점수에 따라 hint_level 자동 조정
   ↓
7. 다음 힌트 요청 시 새로운 hint_level 적용
```

### 7.2 수동 모드 - 관리자 설정 흐름
```
1. 관리자가 "관리자 패널" 접속
   ↓
2. "사용자 관리" 탭 선택
   ↓
3. 특정 사용자의 "실력 수정" 클릭
   ↓
4. 편집 모드 진입
   - skill_mode를 'manual'로 선택
   - skill_score 직접 입력 (예: 75.5)
   - hint_level 직접 선택 (예: 레벨 1)
   ↓
5. "저장" 버튼 클릭
   ↓
6. API 호출: PATCH /api/v1/admin/users/{id}/skill/
   ↓
7. 백엔드: User 모델 업데이트
   - skill_score = 75.5
   - skill_mode = 'manual'
   - hint_level = 1
   ↓
8. 사용자는 다음 힌트 요청부터 레벨 1 힌트 받음
   (문제를 풀어도 자동 업데이트되지 않음)
```

## 8. 제약사항 및 가정

### 8.1 제약사항
- Hugging Face API 키 필요 (월 30,000회 무료)
- 0.5B, 1.5B 모델은 Inference Providers 미지원
- 7B, 32B 모델만 API 방식으로 사용 가능
- 힌트 생성 timeout: 30초

### 8.2 가정
- 사용자는 한 문제에 대해 하나의 세션만 유지 (unique_together)
- 실력 점수는 최근 10개 세션만 고려
- 세션 추적 기능은 향후 구현 예정 (현재는 모델만 정의됨)

## 9. 향후 개선 사항

### 9.1 세션 추적 구현
- 문제 선택 시 ProblemSession 자동 생성
- 힌트/실행 버튼 클릭 시 자동 기록
- 문제 해결 시 자동 완료 처리

### 9.2 대시보드 추가
- 사용자별 실력 점수 변화 그래프
- 힌트 레벨 분포 차트
- 평균 문제 해결 시간 통계

### 9.3 알고리즘 개선
- 문제 난이도별 가중치 적용
- 시간대별 학습 패턴 분석
- 더 세분화된 힌트 레벨 (5단계 등)

## 10. 테스트 시나리오

### 10.1 자동 모드 테스트
1. 신규 사용자 생성 (skill_score=50.0, skill_mode='auto', hint_level=2)
2. 10개 문제를 쉽게 풀도록 시뮬레이션 (낮은 난이도 점수)
3. update_skill_score() 호출
4. 예상 결과: skill_score < 40, hint_level = 3

### 10.2 수동 모드 테스트
1. 관리자 로그인
2. 사용자 실력 지표를 수동으로 설정 (score=80, mode='manual', level=1)
3. 해당 사용자가 문제를 여러 개 풀어도 지표 변경되지 않는지 확인
4. 힌트가 레벨 1 스타일로 제공되는지 확인

### 10.3 힌트 레벨별 테스트
각 레벨에서 동일한 문제에 대해:
- 레벨 1: 함수명이 직접 언급되는지 확인
- 레벨 2: 개념만 언급되는지 확인
- 레벨 3: 질문 형태인지, 평가 문구가 없는지 확인

---

**문서 버전**: 1.0
**최종 업데이트**: 2025-01-06
**작성자**: Claude Code Assistant
