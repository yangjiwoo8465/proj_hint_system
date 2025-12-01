"""
시스템 아키텍처 다이어그램 생성
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 그림 크기 설정
fig, ax = plt.subplots(figsize=(20, 14))
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')

# 색상 정의
COLOR_FRONTEND = '#667eea'
COLOR_BACKEND = '#764ba2'
COLOR_DATABASE = '#f093fb'
COLOR_EXTERNAL = '#4facfe'
COLOR_MODEL = '#43e97b'

# 제목
ax.text(10, 13.5, '개인화된 힌트 시스템 아키텍처',
        ha='center', va='center', fontsize=24, fontweight='bold')

# ============ Frontend Layer ============
# Frontend 배경
frontend_box = FancyBboxPatch((0.5, 9.5), 6, 3.5,
                             boxstyle="round,pad=0.1",
                             edgecolor=COLOR_FRONTEND,
                             facecolor=COLOR_FRONTEND,
                             alpha=0.1, linewidth=2)
ax.add_patch(frontend_box)
ax.text(3.5, 12.7, 'Frontend (React)', ha='center', va='center',
        fontsize=14, fontweight='bold', color=COLOR_FRONTEND)

# React 컴포넌트들
components = [
    (1.5, 11.5, 'MyPage'),
    (3.5, 11.5, 'AdminPanel'),
    (5.5, 11.5, 'CodingTest'),
    (2.5, 10.2, 'UsersTab'),
    (4.5, 10.2, 'Chatbot')
]

for x, y, name in components:
    box = FancyBboxPatch((x-0.4, y-0.25), 0.8, 0.5,
                         boxstyle="round,pad=0.05",
                         edgecolor=COLOR_FRONTEND,
                         facecolor='white', linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, y, name, ha='center', va='center', fontsize=9)

# ============ Backend Layer ============
# Backend 배경
backend_box = FancyBboxPatch((7.5, 9.5), 12, 3.5,
                            boxstyle="round,pad=0.1",
                            edgecolor=COLOR_BACKEND,
                            facecolor=COLOR_BACKEND,
                            alpha=0.1, linewidth=2)
ax.add_patch(backend_box)
ax.text(13.5, 12.7, 'Backend (Django REST Framework)', ha='center', va='center',
        fontsize=14, fontweight='bold', color=COLOR_BACKEND)

# Django Apps
apps = [
    (9, 11.5, 'Authentication'),
    (11.5, 11.5, 'Coding Test'),
    (14, 11.5, 'Admin Panel'),
    (16.5, 11.5, 'Chatbot'),
    (10.2, 10.2, 'hint_api.py'),
    (12.8, 10.2, 'views.py'),
    (15.5, 10.2, 'admin views')
]

for x, y, name in apps:
    box = FancyBboxPatch((x-0.6, y-0.25), 1.2, 0.5,
                         boxstyle="round,pad=0.05",
                         edgecolor=COLOR_BACKEND,
                         facecolor='white', linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, y, name, ha='center', va='center', fontsize=9)

# ============ API Layer ============
api_box = FancyBboxPatch((7.5, 8), 12, 1,
                         boxstyle="round,pad=0.1",
                         edgecolor='gray',
                         facecolor='lightgray',
                         alpha=0.3, linewidth=1.5)
ax.add_patch(api_box)
ax.text(13.5, 8.5, 'REST API Endpoints', ha='center', va='center',
        fontsize=12, fontweight='bold')

# API 엔드포인트
endpoints = [
    (9, 8.2, '/auth/*'),
    (11, 8.2, '/coding-test/*'),
    (13, 8.2, '/admin/*'),
    (15, 8.2, '/chatbot/*'),
    (17, 8.2, '/hint/')
]

for x, y, name in endpoints:
    ax.text(x, y, name, ha='center', va='center', fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray'))

# ============ Data Models Layer ============
models_box = FancyBboxPatch((0.5, 5.5), 6, 2,
                           boxstyle="round,pad=0.1",
                           edgecolor=COLOR_MODEL,
                           facecolor=COLOR_MODEL,
                           alpha=0.1, linewidth=2)
ax.add_patch(models_box)
ax.text(3.5, 7.3, 'Data Models', ha='center', va='center',
        fontsize=12, fontweight='bold', color=COLOR_MODEL)

# 모델들
models = [
    (1.5, 6.5, 'User\n+ skill_score\n+ skill_mode\n+ hint_level'),
    (3.5, 6.5, 'ProblemSession\n+ started_at\n+ hint_count\n+ run_count'),
    (5.5, 6.5, 'Problem\n+ title\n+ level\n+ solutions')
]

for x, y, name in models:
    box = FancyBboxPatch((x-0.6, y-0.5), 1.2, 1,
                         boxstyle="round,pad=0.05",
                         edgecolor=COLOR_MODEL,
                         facecolor='white', linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, y, name, ha='center', va='center', fontsize=7)

# ============ Database Layer ============
db_box = FancyBboxPatch((7.5, 5.5), 5, 2,
                       boxstyle="round,pad=0.1",
                       edgecolor=COLOR_DATABASE,
                       facecolor=COLOR_DATABASE,
                       alpha=0.1, linewidth=2)
ax.add_patch(db_box)
ax.text(10, 7.3, 'Database (PostgreSQL)', ha='center', va='center',
        fontsize=12, fontweight='bold', color=COLOR_DATABASE)

# 데이터베이스 테이블
tables = [
    (8.5, 6.5, 'users'),
    (10, 6.5, 'problem_sessions'),
    (11.5, 6.5, 'problems')
]

for x, y, name in tables:
    ax.text(x, y, name, ha='center', va='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                     edgecolor=COLOR_DATABASE, linewidth=1.5))

# ============ External Services ============
external_box = FancyBboxPatch((14, 5.5), 5.5, 2,
                             boxstyle="round,pad=0.1",
                             edgecolor=COLOR_EXTERNAL,
                             facecolor=COLOR_EXTERNAL,
                             alpha=0.1, linewidth=2)
ax.add_patch(external_box)
ax.text(16.75, 7.3, 'External Services', ha='center', va='center',
        fontsize=12, fontweight='bold', color=COLOR_EXTERNAL)

# Hugging Face API
hf_box = FancyBboxPatch((14.5, 6), 2, 1,
                       boxstyle="round,pad=0.05",
                       edgecolor=COLOR_EXTERNAL,
                       facecolor='white', linewidth=1.5)
ax.add_patch(hf_box)
ax.text(15.5, 6.7, 'Hugging Face', ha='center', va='center', fontsize=9, fontweight='bold')
ax.text(15.5, 6.4, 'Inference Providers', ha='center', va='center', fontsize=7)
ax.text(15.5, 6.1, 'Qwen 7B/32B', ha='center', va='center', fontsize=7, style='italic')

# Docker 표시
docker_box = FancyBboxPatch((17.2, 6), 1.8, 1,
                           boxstyle="round,pad=0.05",
                           edgecolor=COLOR_EXTERNAL,
                           facecolor='white', linewidth=1.5)
ax.add_patch(docker_box)
ax.text(18.1, 6.5, 'Docker', ha='center', va='center', fontsize=9, fontweight='bold')
ax.text(18.1, 6.2, 'Compose', ha='center', va='center', fontsize=7)

# ============ Business Logic Layer ============
logic_box = FancyBboxPatch((0.5, 3), 19, 2,
                          boxstyle="round,pad=0.1",
                          edgecolor='darkgreen',
                          facecolor='lightgreen',
                          alpha=0.1, linewidth=2)
ax.add_patch(logic_box)
ax.text(10, 4.7, '핵심 비즈니스 로직', ha='center', va='center',
        fontsize=12, fontweight='bold', color='darkgreen')

# 로직 컴포넌트
logics = [
    (3, 4, '실력 점수 계산\ncalculate_difficulty_score()', 1.8),
    (7, 4, '힌트 레벨 결정\nuser.hint_level', 1.5),
    (10.5, 4, '개인화 프롬프트 생성\n레벨 1/2/3 분기', 2),
    (14, 4, '자동/수동 모드 관리\nupdate_skill_score()', 1.8),
    (17, 4, 'AI 모델 호출\nHugging Face API', 1.5)
]

for x, y, name, width in logics:
    box = FancyBboxPatch((x-width/2, y-0.4), width, 0.8,
                         boxstyle="round,pad=0.05",
                         edgecolor='darkgreen',
                         facecolor='white', linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, y, name, ha='center', va='center', fontsize=7)

# ============ Data Flow Arrows ============
# Frontend -> Backend
arrow1 = FancyArrowPatch((6.5, 11), (7.5, 11),
                        arrowstyle='->', mutation_scale=20, linewidth=2,
                        color=COLOR_BACKEND)
ax.add_patch(arrow1)
ax.text(7, 11.3, 'HTTP\nRequests', ha='center', va='center', fontsize=7)

# Backend -> Database
arrow2 = FancyArrowPatch((10, 7.5), (10, 8),
                        arrowstyle='<->', mutation_scale=20, linewidth=2,
                        color=COLOR_DATABASE)
ax.add_patch(arrow2)
ax.text(10.5, 7.75, 'ORM', ha='center', va='center', fontsize=7)

# Backend -> External API
arrow3 = FancyArrowPatch((14, 10), (15.5, 7),
                        arrowstyle='->', mutation_scale=20, linewidth=2,
                        color=COLOR_EXTERNAL, linestyle='--')
ax.add_patch(arrow3)
ax.text(14.5, 8.5, 'API Call', ha='center', va='center', fontsize=7)

# Models -> Database
arrow4 = FancyArrowPatch((3.5, 5.5), (10, 5.5),
                        arrowstyle='<->', mutation_scale=20, linewidth=2,
                        color=COLOR_MODEL)
ax.add_patch(arrow4)
ax.text(6.75, 5.8, 'Django ORM', ha='center', va='center', fontsize=7)

# Business Logic connections
arrow5 = FancyArrowPatch((10, 5), (10, 5.5),
                        arrowstyle='<->', mutation_scale=15, linewidth=1.5,
                        color='darkgreen', linestyle=':')
ax.add_patch(arrow5)

# ============ Legend ============
legend_elements = [
    mpatches.Patch(facecolor=COLOR_FRONTEND, alpha=0.3, label='Frontend Layer'),
    mpatches.Patch(facecolor=COLOR_BACKEND, alpha=0.3, label='Backend Layer'),
    mpatches.Patch(facecolor=COLOR_DATABASE, alpha=0.3, label='Database Layer'),
    mpatches.Patch(facecolor=COLOR_EXTERNAL, alpha=0.3, label='External Services'),
    mpatches.Patch(facecolor=COLOR_MODEL, alpha=0.3, label='Data Models'),
    mpatches.Patch(facecolor='lightgreen', alpha=0.3, label='Business Logic')
]

ax.legend(handles=legend_elements, loc='lower center', ncol=6,
         frameon=True, fontsize=9, bbox_to_anchor=(0.5, 0.05))

# ============ 시스템 플로우 설명 ============
flow_text = """
주요 데이터 흐름:
1. 사용자가 힌트 요청 → Frontend에서 POST /coding-test/hint/
2. hint_api.py에서 user.hint_level 조회 → 레벨별 프롬프트 생성
3. Hugging Face API 호출 → AI 힌트 생성
4. ProblemSession에 행동 기록 → skill_score 자동 계산
5. 관리자가 UsersTab에서 실력 지표 수정 가능
"""

ax.text(10, 1.5, flow_text, ha='center', va='center', fontsize=8,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
                 edgecolor='orange', linewidth=1))

# ============ 기술 스택 ============
tech_stack = """
기술 스택:
• Frontend: React 18, Redux, Monaco Editor, React Router
• Backend: Django 4.2, Django REST Framework
• Database: PostgreSQL
• AI: Hugging Face Inference Providers (Qwen 7B/32B)
• Infrastructure: Docker, Docker Compose
"""

ax.text(3.5, 1.5, tech_stack, ha='center', va='center', fontsize=7,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue',
                 edgecolor='blue', linewidth=1))

ax.text(16.5, 1.5, '버전: 1.0\n날짜: 2025-01-06', ha='center', va='center', fontsize=7,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgray', edgecolor='gray'))

plt.tight_layout()
plt.savefig('C:/Users/playdata2/Desktop/playdata/Workspace/팀프로젝트5/5th-project_mvp/docs/system_architecture.png',
           dpi=300, bbox_inches='tight', facecolor='white')
print("✅ 시스템 아키텍처 다이어그램이 생성되었습니다: docs/system_architecture.png")
