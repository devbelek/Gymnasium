from django.contrib.auth.models import User
from django.db import models
from rest_framework.exceptions import ValidationError


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='Аватар')
    about = models.CharField(max_length=100, blank=True, null=True, verbose_name='О себе')

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


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations', verbose_name='Пользователь')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма(сом)')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    comment = models.CharField(max_length=300, blank=True, null=True)
    confirmation_file = models.FileField(upload_to='checks/%Y/%m/%d/', blank=False, verbose_name='Квитанция о переводе')
    is_verified = models.BooleanField(default=False, verbose_name='Статус подтверждения')

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.date}"

    class Meta:
        verbose_name = "Не подтвержденные переводы средств"
        verbose_name_plural = "Не подтвержденные переводы средств"


class ConfirmedDonation(models.Model):
    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name='confirmed_donation', verbose_name='Перевод')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confirmed_donations', verbose_name='Пользователь')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name='Комментарий')

    def __str__(self):
        return f"{self.user.username} - {self.donation.amount} - {self.date}"

    @property
    def amount(self):
        return self.donation.amount

    class Meta:
        verbose_name = "Подтвержденные переводы средств"
        verbose_name_plural = "Подтвержденные переводы средств"



