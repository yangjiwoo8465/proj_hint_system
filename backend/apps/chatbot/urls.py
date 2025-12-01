from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    # 북마크 API
    path('bookmarks/', views.get_bookmarks, name='get_bookmarks'),
    path('bookmark/', views.create_bookmark, name='create_bookmark'),
    path('bookmark/<int:bookmark_id>/', views.delete_bookmark, name='delete_bookmark'),
]
