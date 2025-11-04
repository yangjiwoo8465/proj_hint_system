"""
코딩 테스트 모델
"""
from django.db import models
from django.conf import settings


class Problem(models.Model):
    """문제 모델"""
    problem_id = models.CharField('문제 ID', max_length=20, unique=True, db_index=True)
    step_title = models.CharField('단계 제목', max_length=200, blank=True)
    title = models.CharField('제목', max_length=200)
    level = models.IntegerField('난이도', choices=[(i, f'레벨 {i}') for i in range(1, 6)])
    tags = models.JSONField('태그', default=list)
    description = models.TextField('문제 설명')
    input_description = models.TextField('입력 설명')
    output_description = models.TextField('출력 설명')
    examples = models.JSONField('예시', default=list)
    url = models.URLField('문제 URL', blank=True)
    solutions = models.JSONField('정답 코드', default=list)
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        db_table = 'problems'
        verbose_name = '문제'
        verbose_name_plural = '문제 목록'
        ordering = ['problem_id']

    def __str__(self):
        return f"[{self.problem_id}] {self.title}"


class Submission(models.Model):
    """제출 기록 모델"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='submissions')
    code = models.TextField('제출 코드')
    result = models.CharField(
        '결과',
        max_length=20,
        choices=[
            ('pending', '대기 중'),
            ('success', '성공'),
            ('fail', '실패'),
            ('error', '에러'),
        ]
    )
    output = models.TextField('출력', blank=True)
    error_message = models.TextField('에러 메시지', blank=True)
    execution_count = models.IntegerField('실행 횟수', default=1)
    time_spent = models.IntegerField('소요 시간(초)', default=0)
    rating_earned = models.IntegerField('획득 점수', default=0)
    created_at = models.DateTimeField('제출일', auto_now_add=True)

    class Meta:
        db_table = 'submissions'
        verbose_name = '제출 기록'
        verbose_name_plural = '제출 기록 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} ({self.result})"


class Bookmark(models.Model):
    """북마크 모델"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='problem_bookmarks')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField('북마크일', auto_now_add=True)

    class Meta:
        db_table = 'problem_bookmarks'
        verbose_name = '문제 북마크'
        verbose_name_plural = '문제 북마크 목록'
        unique_together = ['user', 'problem']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"


class HintRequest(models.Model):
    """힌트 요청 기록 모델"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hint_requests')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='hint_requests')
    hint_level = models.CharField(
        '힌트 레벨',
        max_length=20,
        choices=[
            ('small', '소 힌트'),
            ('medium', '중 힌트'),
            ('large', '대 힌트'),
        ]
    )
    user_code = models.TextField('사용자 코드')
    hint_response = models.TextField('힌트 응답')
    model_used = models.CharField('사용 모델', max_length=100, blank=True)
    created_at = models.DateTimeField('요청일', auto_now_add=True)

    class Meta:
        db_table = 'hint_requests'
        verbose_name = '힌트 요청'
        verbose_name_plural = '힌트 요청 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} ({self.hint_level})"
