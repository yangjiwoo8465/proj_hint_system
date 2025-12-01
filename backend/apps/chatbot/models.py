from django.db import models
from django.conf import settings


class ChatbotBookmark(models.Model):
    """Chatbot Response Bookmark Model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chatbot_bookmarks'
    )
    content = models.TextField('Bookmark Content')
    sources = models.JSONField('Reference Documents', default=list, blank=True)
    created_at = models.DateTimeField('Created At', auto_now_add=True)

    class Meta:
        db_table = 'chatbot_bookmarks'
        verbose_name = 'Chatbot Bookmark'
        verbose_name_plural = 'Chatbot Bookmarks'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}..."
