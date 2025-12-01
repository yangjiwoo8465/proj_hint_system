from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ChatbotBookmark


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bookmarks(request):
    """Get user chatbot bookmarks list"""
    bookmarks = ChatbotBookmark.objects.filter(user=request.user)
    data = [
        {
            'id': b.id,
            'content': b.content,
            'sources': b.sources,
            'created_at': b.created_at.isoformat()
        }
        for b in bookmarks
    ]
    return Response({'success': True, 'data': data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_bookmark(request):
    """Add chatbot response bookmark"""
    content = request.data.get('content', '')
    sources = request.data.get('sources', [])

    if not content:
        return Response({
            'success': False,
            'error': 'Bookmark content is required.'
        }, status=status.HTTP_400_BAD_REQUEST)

    bookmark = ChatbotBookmark.objects.create(
        user=request.user,
        content=content,
        sources=sources if isinstance(sources, list) else []
    )

    return Response({
        'success': True,
        'data': {
            'id': bookmark.id,
            'content': bookmark.content,
            'sources': bookmark.sources,
            'created_at': bookmark.created_at.isoformat()
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_bookmark(request, bookmark_id):
    """Delete chatbot bookmark"""
    try:
        bookmark = ChatbotBookmark.objects.get(id=bookmark_id, user=request.user)
        bookmark.delete()
        return Response({'success': True, 'message': 'Bookmark deleted successfully.'})
    except ChatbotBookmark.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Bookmark not found.'
        }, status=status.HTTP_404_NOT_FOUND)
