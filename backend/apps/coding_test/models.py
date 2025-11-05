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


class TestCaseProposal(models.Model):
    """테스트 케이스 제안 모델"""
    STATUS_CHOICES = [
        ('pending', '승인 대기'),
        ('approved', '승인됨'),
        ('rejected', '거부됨'),
    ]

    problem_id = models.CharField('문제 ID', max_length=20, db_index=True)
    proposed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='test_case_proposals',
        verbose_name='제안자'
    )
    input_data = models.TextField('입력 데이터')
    expected_output = models.TextField('예상 출력')
    description = models.TextField('설명', blank=True, help_text='이 테스트 케이스가 필요한 이유')
    status = models.CharField(
        '상태',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_test_cases',
        verbose_name='검토자'
    )
    review_comment = models.TextField('검토 의견', blank=True)
    created_at = models.DateTimeField('제안일', auto_now_add=True)
    reviewed_at = models.DateTimeField('검토일', null=True, blank=True)

    class Meta:
        db_table = 'test_case_proposals'
        verbose_name = '테스트 케이스 제안'
        verbose_name_plural = '테스트 케이스 제안 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.problem_id}] {self.proposed_by.username} - {self.get_status_display()}"


class SolutionProposal(models.Model):
    """솔루션 제안 모델"""
    STATUS_CHOICES = [
        ('pending', '승인 대기'),
        ('approved', '승인됨'),
        ('rejected', '거부됨'),
    ]

    problem_id = models.CharField('문제 ID', max_length=20, db_index=True)
    proposed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='solution_proposals',
        verbose_name='제안자'
    )
    solution_code = models.TextField('솔루션 코드')
    language = models.CharField('프로그래밍 언어', max_length=50, default='python')
    description = models.TextField('설명', blank=True, help_text='이 솔루션에 대한 설명')
    is_reference = models.BooleanField('참조 솔루션 여부', default=True, help_text='JSON에 추가할지 여부')
    status = models.CharField(
        '상태',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_solutions',
        verbose_name='검토자'
    )
    review_comment = models.TextField('검토 의견', blank=True)
    created_at = models.DateTimeField('제안일', auto_now_add=True)
    reviewed_at = models.DateTimeField('검토일', null=True, blank=True)

    class Meta:
        db_table = 'solution_proposals'
        verbose_name = '솔루션 제안'
        verbose_name_plural = '솔루션 제안 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.problem_id}] {self.proposed_by.username} - {self.get_status_display()}"


class ProblemProposal(models.Model):
    """문제 제안 모델"""
    STATUS_CHOICES = [
        ('pending', '승인 대기'),
        ('approved', '승인됨'),
        ('rejected', '거부됨'),
    ]

    problem_id = models.CharField('문제 ID', max_length=20, db_index=True)
    title = models.CharField('문제 제목', max_length=200)
    step_title = models.CharField('단계 제목', max_length=200, blank=True)
    description = models.TextField('문제 설명')
    input_description = models.TextField('입력 설명')
    output_description = models.TextField('출력 설명')
    level = models.IntegerField('난이도', choices=[(i, f'레벨 {i}') for i in range(1, 16)])
    tags = models.JSONField('태그', default=list)
    solution_code = models.TextField('참조 솔루션 코드')
    language = models.CharField('프로그래밍 언어', max_length=50, default='python')
    test_cases = models.JSONField('테스트 케이스', default=list, help_text='입력/출력 테스트 케이스 목록')

    proposed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='problem_proposals',
        verbose_name='제안자'
    )
    status = models.CharField(
        '상태',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_problems',
        verbose_name='검토자'
    )
    review_comment = models.TextField('검토 의견', blank=True)
    created_at = models.DateTimeField('제안일', auto_now_add=True)
    reviewed_at = models.DateTimeField('검토일', null=True, blank=True)

    class Meta:
        db_table = 'problem_proposals'
        verbose_name = '문제 제안'
        verbose_name_plural = '문제 제안 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.problem_id}] {self.title} - {self.get_status_display()}"


class AIModelConfig(models.Model):
    """AI 모델 설정 (싱글톤 패턴)"""
    MODE_CHOICES = [
        ('api', 'API 방식 (Hugging Face)'),
        ('local', '로컬 로드 방식'),
    ]

    mode = models.CharField(
        '모델 사용 방식',
        max_length=20,
        choices=MODE_CHOICES,
        default='api'
    )
    api_key = models.CharField(
        'Hugging Face API Key',
        max_length=200,
        blank=True,
        help_text='API 방식 사용 시 필요'
    )
    model_name = models.CharField(
        '모델 이름',
        max_length=200,
        default='Qwen/Qwen2.5-Coder-32B-Instruct'
    )
    is_model_loaded = models.BooleanField(
        '모델 로드 여부',
        default=False,
        help_text='로컬 모드에서 모델이 메모리에 로드되었는지 여부'
    )
    updated_at = models.DateTimeField('마지막 수정일', auto_now=True)

    class Meta:
        db_table = 'ai_model_config'
        verbose_name = 'AI 모델 설정'
        verbose_name_plural = 'AI 모델 설정'

    def save(self, *args, **kwargs):
        # 싱글톤 패턴: 항상 ID=1인 레코드만 사용
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        """설정 가져오기 (없으면 기본값으로 생성)"""
        config, created = cls.objects.get_or_create(pk=1)
        return config

    def __str__(self):
        return f"AI 모델 설정 ({self.get_mode_display()})"
