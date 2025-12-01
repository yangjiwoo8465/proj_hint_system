# 기존 app.py → 관리자 탭 마이그레이션 가이드

## 기존 app.py 기능

기존 `hint-system/app.py`는 Gradio 기반의 힌트 평가 시스템이었습니다.

### 주요 기능
1. **문제 선택** - 문제 ID 선택 및 표시
2. **모델 관리** - LLM 모델 동적 추가/제거
3. **힌트 생성** - 여러 모델로 힌트 생성 (대/중/소)
4. **답안 코드 확인** - 각 문제의 정답 코드 조회
5. **Temperature 조정** - 모델별 temperature 설정
6. **평가** - 힌트 품질 평가 및 저장

---

## 새 프로젝트에서의 위치

### 🔐 관리자 탭 (`apps/admin_panel/`)

기존 app.py의 **관리자 전용 기능**들이 여기로 이전됩니다:

```
backend/apps/admin_panel/
├── models.py           # 모델 설정, 평가 기록
├── views.py            # 관리자 API
├── serializers.py
└── urls.py

frontend/src/pages/AdminPanel/
├── index.jsx           # 관리자 메인
├── HintAdmin.jsx       # 힌트 챗봇 관리 (기존 app.py)
├── ChatbotAdmin.jsx    # 문답 챗봇 관리
└── ModelConfig.jsx     # 모델 설정
```

### ⚙️ 이전될 기능

#### 1. 힌트 챗봇 관리 (`HintAdmin.jsx`)
- **문제 선택** - 모든 문제 목록에서 선택
- **답안 코드 조회** ⭐ (관리자만)
- **모델 선택** - 여러 모델로 힌트 생성
- **Temperature 설정** ⭐ (관리자만)
- **힌트 레벨** - 대/중/소 선택
- **힌트 생성 및 비교** - 여러 모델 결과 비교
- **평가 저장** - 힌트 품질 평가

#### 2. 모델 관리 (`ModelConfig.jsx`)
- **모델 추가/제거** ⭐ (관리자만)
- **모델 정보** - 이름, 경로, 양자화, 타입
- **우선순위 설정**

#### 3. 평가 데이터 관리
- **평가 기록 조회**
- **평가 통계**
- **Export 기능**

---

## 일반 사용자 vs 관리자

### 👤 일반 사용자 (코딩 테스트 탭)
```
frontend/src/pages/CodingTest/
```

**제공 기능:**
- 문제 풀이
- 코드 실행
- 힌트 요청 (대/중/소)
- 북마크

**제한:**
- ❌ 답안 코드 조회 불가
- ❌ 모델 변경 불가
- ❌ Temperature 설정 불가
- ✅ 자신의 성향에 맞는 힌트만 제공

### 🔐 관리자 (관리자 탭)
```
frontend/src/pages/AdminPanel/
```

**추가 권한:**
- ✅ 모든 문제의 답안 코드 조회
- ✅ 모델 선택 및 변경
- ✅ Temperature 조정
- ✅ 여러 모델 결과 비교
- ✅ 힌트 품질 평가
- ✅ 평가 데이터 관리

---

## 화면 구성 변경

### 기존 (Gradio)
```
┌─────────────────────────────────────┐
│  힌트 평가 시스템                     │
├─────────────────────────────────────┤
│  [문제 선택]  [모델 관리]  [설정]     │
│                                     │
│  문제 정보                           │
│  답안 코드                           │
│                                     │
│  힌트 생성 버튼                      │
│  힌트 결과 (여러 모델)               │
│                                     │
│  평가 및 저장                        │
└─────────────────────────────────────┘
```

### 새 프로젝트 (React)
```
┌─────────────────────────────────────────────────┐
│  사이드바                  │  관리자 패널          │
├──────────┼──────────────────────────────────────┤
│ 메인     │  탭: [힌트 관리] [챗봇 관리] [모델]   │
│ 코딩테스트│  ┌──────────────────────────────┐  │
│ 챗봇     │  │ 문제 선택: [1000 ▼]          │  │
│ 마이페이지│  │                              │  │
│ ────────│  │ 문제 정보                     │  │
│ 관리자★  │  │ [답안 코드 보기 ▼]           │  │
│          │  │                              │  │
│          │  │ 모델 선택: [Qwen ▼] [+추가]  │  │
│          │  │ Temperature: [0.7 ━━━━○]     │  │
│          │  │ 힌트 레벨: ●대 ○중 ○소       │  │
│          │  │                              │  │
│          │  │ [힌트 생성하기]               │  │
│          │  │                              │  │
│          │  │ 생성된 힌트:                  │  │
│          │  │ ┌────────────────────┐      │  │
│          │  │ │ Qwen2.5 결과       │      │  │
│          │  │ │ ...                │      │  │
│          │  │ └────────────────────┘      │  │
│          │  │                              │  │
│          │  │ 평가: ★★★★☆ [저장]         │  │
│          │  └──────────────────────────────┘  │
└──────────┴──────────────────────────────────────┘
```

---

## 구현 예정 사항

### Backend (`apps/admin_panel/`)

#### models.py
```python
class ModelConfiguration(models.Model):
    """LLM 모델 설정"""
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=500)
    quantize = models.BooleanField(default=False)
    model_type = models.CharField(max_length=50)  # chat, coder
    priority = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

class HintEvaluation(models.Model):
    """힌트 평가 기록"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=200)
    hint_level = models.CharField(max_length=20)
    hint_content = models.TextField()
    rating = models.IntegerField()
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
```

#### views.py
```python
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_solution_code(request, problem_id):
    """답안 코드 조회 (관리자만)"""
    problem = Problem.objects.get(problem_id=problem_id)
    return success_response(data={
        'solutions': problem.solutions
    })

@api_view(['POST'])
@permission_classes([IsAdminUser])
def generate_admin_hint(request):
    """관리자용 힌트 생성 (모델/Temperature 선택 가능)"""
    model_name = request.data.get('model')
    temperature = request.data.get('temperature', 0.7)
    # ... 힌트 생성 로직
```

### Frontend (`pages/AdminPanel/`)

#### HintAdmin.jsx
```jsx
const HintAdmin = () => {
  const [selectedProblem, setSelectedProblem] = useState(null)
  const [selectedModel, setSelectedModel] = useState(null)
  const [temperature, setTemperature] = useState(0.7)
  const [showSolution, setShowSolution] = useState(false)
  const [generatedHints, setGeneratedHints] = useState([])

  const generateHint = async () => {
    const response = await adminService.generateHint({
      problem_id: selectedProblem.problem_id,
      model: selectedModel,
      temperature: temperature,
      hint_level: hintLevel
    })
    setGeneratedHints([...generatedHints, response.data])
  }

  return (
    <div className="hint-admin">
      <ProblemSelector onChange={setSelectedProblem} />

      {selectedProblem && (
        <>
          <ProblemInfo problem={selectedProblem} />

          {/* 관리자 전용: 답안 코드 */}
          <Button onClick={() => setShowSolution(!showSolution)}>
            답안 코드 {showSolution ? '숨기기' : '보기'}
          </Button>
          {showSolution && <SolutionCode solutions={selectedProblem.solutions} />}

          {/* 모델 및 설정 */}
          <ModelSelector onChange={setSelectedModel} />
          <TemperatureSlider value={temperature} onChange={setTemperature} />
          <HintLevelSelector value={hintLevel} onChange={setHintLevel} />

          <Button onClick={generateHint}>힌트 생성</Button>

          {/* 생성된 힌트 목록 */}
          <HintResults hints={generatedHints} onRate={saveEvaluation} />
        </>
      )}
    </div>
  )
}
```

---

## 기존 코드 재사용

### 재사용 가능한 부분

1. **모델 추론 로직** (`hint-system/models/`)
   - `model_inference.py` - 그대로 사용
   - `model_config.py` - 설정 부분 재사용
   - `runpod_client.py` - RunPod 연동 시 사용

2. **힌트 생성 로직**
   - 프롬프트 생성 로직
   - 소크라테스 질문 생성
   - 힌트 레벨별 처리

3. **문제 데이터** (`hint-system/data/`)
   - `problems_multi_solution_complete.json`
   - DB로 import 후 사용

### 새로 구현할 부분

1. **React UI** - Gradio → React 컴포넌트
2. **REST API** - Gradio 인터페이스 → Django REST API
3. **권한 관리** - 관리자 전용 기능 분리
4. **데이터베이스** - 평가 기록 저장

---

## 마이그레이션 체크리스트

### Phase 1: Backend 구조
- [ ] `admin_panel` 앱 모델 정의
- [ ] 관리자 권한 체크 (IsAdminUser)
- [ ] 답안 코드 조회 API
- [ ] 힌트 생성 API (모델/Temperature 선택)
- [ ] 평가 저장 API

### Phase 2: Frontend 구조
- [ ] AdminPanel 페이지 기본 구조
- [ ] HintAdmin 컴포넌트
- [ ] 문제 선택 UI
- [ ] 답안 코드 보기 버튼
- [ ] 모델 선택 드롭다운
- [ ] Temperature 슬라이더
- [ ] 힌트 생성 및 표시

### Phase 3: 기존 로직 통합
- [ ] `hint-system/models/` 연동
- [ ] 힌트 생성 로직 적용
- [ ] 프롬프트 생성 로직 재사용

### Phase 4: 추가 기능
- [ ] 여러 모델 동시 비교
- [ ] 평가 통계 대시보드
- [ ] Export 기능

---

## 요약

✅ **기존 app.py의 모든 기능**이 새 프로젝트의 **관리자 탭**으로 이전됩니다.

✅ **관리자만 가능한 기능**:
- 답안 코드 조회
- 모델 선택 및 변경
- Temperature 설정
- 힌트 품질 평가

✅ **일반 사용자**는 코딩 테스트 탭에서 제한된 힌트만 받습니다.

화면 구성은 Gradio에서 React로 바뀌지만, **핵심 기능은 모두 유지**됩니다!
