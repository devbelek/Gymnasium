from django.contrib.auth.models import User
from django.db import models
from rest_framework.exceptions import ValidationError


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='Аватар')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Личные кабинеты пользователей"
        verbose_name_plural = "Личные кабинеты пользователей"


class Comment(models.Model):
    our_achievements = models.ForeignKey(
        'main.OurAchievements', on_delete=models.CASCADE,
        null=True, blank=True, verbose_name='Связка с "Наши достижения"'
    )
    news = models.ForeignKey(
        'main.News', on_delete=models.CASCADE,
        null=True, blank=True, verbose_name='Связка с "Новости"'
    )
    successful_graduates = models.ForeignKey(
        'main.SuccessfulGraduates', on_delete=models.CASCADE,
        null=True, blank=True, verbose_name='Связка с "Успешные студенты"'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = "Комментарии к постам"
        verbose_name_plural = "Комментарии к постам"

    def __str__(self):
        return f'Комментарий от {self.author.username}'

    def clean(self):
        super().clean()
        if sum(bool(x) for x in [self.our_achievements, self.news, self.successful_graduates]) != 1:
            raise ValidationError('Комментарий должен быть связан только с одной категорией постов.')


class CommentReply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE, verbose_name='Комментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Ответ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = "Ответ на комментарий"
        verbose_name_plural = "Ответы на комментарии"

    def __str__(self):
        return f'Ответ от {self.author.username}'


class Like(models.Model):
    comment = models.ForeignKey(Comment, related_name='likes', on_delete=models.CASCADE, verbose_name='Комментарий')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        unique_together = ('comment', 'user')
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def __str__(self):
        return f'Лайк от {self.user.username} на комментарий {self.comment.id}'
