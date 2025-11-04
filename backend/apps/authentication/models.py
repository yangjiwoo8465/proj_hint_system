"""
사용자 인증 모델
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    커스텀 사용자 모델
    """
    ROLE_CHOICES = (
        ('user', '일반 사용자'),
        ('admin', '관리자'),
    )

    email = models.EmailField('이메일', unique=True)
    role = models.CharField('역할', max_length=10, choices=ROLE_CHOICES, default='user')
    rating = models.IntegerField('레이팅 점수', default=0)
    tendency = models.CharField(
        '문제 풀이 성향',
        max_length=20,
        choices=(
            ('perfectionist', '완벽주의형'),
            ('iterative', '반복형'),
            ('unknown', '미분류'),
        ),
        default='unknown'
    )
    created_at = models.DateTimeField('가입일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_admin(self):
        """관리자 여부"""
        return self.role == 'admin'
