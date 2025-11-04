# 최종 프로젝트 구조

## ✅ 완성된 구조

```
proj_hint_system/
│
├── 🐳 Docker 설정
│   ├── docker-compose.yml
│   ├── .env
│   └── .env.example
│
├── 📂 백엔드 (Django)
│   └── backend/
│       ├── config/              설정
│       ├── common/              공통 유틸
│       ├── vectordb/            ChromaDB
│       └── apps/
│           ├── authentication/   로그인/회원가입
│           ├── coding_test/      ⭐ 코딩 테스트
│           │   ├── models/      ✅ LLM 모델 (hint-system 통합)
│           │   ├── data/        ✅ 문제 데이터 (hint-system 통합)
│           │   ├── services/    힌트/실행/분석 로직
│           │   ├── models.py    Django 모델
│           │   └── views.py     API
│           ├── chatbot/          문답 챗봇
│           ├── mypage/           마이페이지
│           └── admin_panel/      관리자
│
├── 📂 프론트엔드 (React)
│   └── frontend/
│       └── src/
│           ├── components/       공통 컴포넌트
│           ├── pages/
│           │   ├── MainPage/     메인 화면
│           │   ├── CodingTest/   코딩 테스트
│           │   ├── Chatbot/      챗봇
│           │   ├── MyPage/       마이페이지
│           │   └── AdminPanel/   관리자
│           ├── services/         API
│           ├── store/            Redux
│           └── utils/            유틸리티
│
├── 📂 인프라
│   └── nginx/                   Nginx 설정
│
├── 📚 문서 (4개)
│   ├── PROJECT_SUMMARY.md       ⭐ 시작하기
│   ├── DEVELOPMENT_GUIDE.md     개발 가이드
│   ├── DOCKER_SETUP.md          Docker 가이드
│   └── MIGRATION_GUIDE.md       app.py 마이그레이션
│
└── 기타/                        불필요한 파일들
    └── hint-system/             기존 프로젝트 (백업)
```

---

## 🔄 주요 변경사항

### hint-system 통합

**이전:**
```
hint-system/           (별도 폴더)
├── models/           LLM 모델 관리
├── data/             문제 데이터
└── app.py            Gradio 앱
```

**이후:**
```
backend/apps/coding_test/
├── models/           ✅ LLM 모델 (통합됨)
├── data/             ✅ 문제 데이터 (통합됨)
└── services/
    └── hint_generator.py  (models/ 사용)
```

---

## 📊 모듈별 작업 영역

| 담당 탭 | 백엔드 | 프론트엔드 |
|---------|--------|-----------|
| 메인 화면 | `apps/authentication/` | `pages/MainPage/` |
| **코딩 테스트** | `apps/coding_test/` ⭐ | `pages/CodingTest/` |
| 챗봇 | `apps/chatbot/` | `pages/Chatbot/` |
| 마이페이지 | `apps/mypage/` | `pages/MyPage/` |
| 관리자 | `apps/admin_panel/` | `pages/AdminPanel/` |

---

## 🎯 코딩 테스트 앱 구조

```
backend/apps/coding_test/
├── models/                    ✅ LLM 모델 관리
│   ├── model_inference.py    모델 추론
│   ├── model_config.py       모델 설정
│   └── runpod_client.py      RunPod 연동
│
├── data/                      ✅ 문제 데이터
│   └── problems_multi_solution_complete.json
│
├── services/                  비즈니스 로직
│   ├── hint_generator.py     힌트 생성 (models/ 사용)
│   ├── code_executor.py      코드 실행
│   └── user_analyzer.py      성향 분석
│
├── models.py                  Django 모델
│   ├── Problem
│   ├── Submission
│   ├── Bookmark
│   └── HintRequest
│
├── views.py                   REST API
├── serializers.py
├── urls.py
└── admin.py
```

---

## 🚀 실행 방법

```bash
cd /workspace/proj_hint_system
docker compose up -d --build
```

---

## ✨ 완성도

- ✅ 프로젝트 구조 완성
- ✅ 탭별 모듈 분리
- ✅ hint-system 통합
- ✅ Docker 설정 완료
- ⏳ 각 탭 기능 구현 (TODO)

