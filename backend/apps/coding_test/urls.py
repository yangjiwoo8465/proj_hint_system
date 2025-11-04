"""
코딩 테스트 URL 설정
"""
from django.urls import path
from . import views

app_name = 'coding_test'

urlpatterns = [
    # 문제 관리
    path('problems/', views.ProblemListView.as_view(), name='problem_list'),
    path('problems/<str:problem_id>/', views.ProblemDetailView.as_view(), name='problem_detail'),

    # 코드 실행
    path('execute/', views.execute_code, name='execute_code'),

    # 힌트
    path('hints/', views.get_hint, name='get_hint'),

    # 제출 기록
    path('submissions/', views.SubmissionListView.as_view(), name='submission_list'),
    path('submissions/<int:pk>/', views.SubmissionDetailView.as_view(), name='submission_detail'),

    # 북마크
    path('bookmarks/', views.BookmarkListView.as_view(), name='bookmark_list'),
    path('bookmarks/toggle/', views.toggle_bookmark, name='toggle_bookmark'),
]
