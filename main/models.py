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



# Добавление имен классов в котором учатся ученики
class NameOfGrades(models.Model):
    choosing = models.CharField(max_length=20, blank=False, unique=True, verbose_name='Выбор')

    class Meta:
        verbose_name = 'Название классов'
        verbose_name_plural = 'Название классов'

    def __str__(self):
        return self.choosing


# Должности среди учащихся (Президент и тд)
class AdministratorTypes(models.Model):
    choosing = models.CharField(max_length=50, blank=False, unique=True, verbose_name='Выбор')

    class Meta:
        verbose_name = 'Должности среди учащихся'
        verbose_name_plural = 'Должности среди учащихся'

    def __str__(self):
        return f"Тип должностного лица среди учащихся: {self.choosing}"


# Имя олимпиады
class NamesOfOlympia(models.Model):
    choosing = models.CharField(max_length=20, blank=False, unique=True, verbose_name='Выбор')

    class Meta:
        verbose_name = 'Название олимпиады'
        verbose_name_plural = 'Название олимпиады'

    def __str__(self):
        return self.choosing


# Студенты
class Students(models.Model):
    CHOICES_GRADE = (
        ('fifth', '5'),
        ('sixth', '6'),
        ('seventh', '7'),
        ('eighth', '8'),
        ('ninth', '9'),
        ('tenth', '10'),
        ('eleventh', '11'),
    )
    grade = models.CharField(max_length=50, choices=CHOICES_GRADE, blank=False, verbose_name='Класс')
    name = models.CharField(max_length=25, blank=False, verbose_name='Имя')
    surname = models.CharField(max_length=25, blank=False, verbose_name='Фамилия')
    name_of_grade = models.ForeignKey(NameOfGrades, on_delete=models.CASCADE, verbose_name='Название класса')
    olympian_status = models.ForeignKey(NamesOfOlympia, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Олимпиец')
    administrator_status = models.ForeignKey(AdministratorTypes, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Позиция')

    class Meta:
        verbose_name = 'Ученики'
        verbose_name_plural = 'Ученики'

    def __str__(self):
        return f"{self.name} {self.surname} - Класс {self.get_grade_display()} - Название класса {self.name_of_grade}"


# Благодарственное письмо от Учащихся
class ThanksNoteFromStudents(models.Model):
    title = models.CharField(max_length=50, blank=False, verbose_name='Заголовок')
    text = models.TextField(blank=False, verbose_name='Текст')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Благодарственное письмо (от учеников)'
        verbose_name_plural = 'Благодарственное письмо (от учеников)'

    def __str__(self):
        return self.title


# Олимпийцы
class Olympians(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name='Ученик')

    class Meta:
        verbose_name = 'Олимпийцы'
        verbose_name_plural = 'Олимпийцы'

    def __str__(self):
        return f"Олимпиец: {self.student.name} {self.student.surname}"


# Успешные выпускники
class SuccessfulGraduates(models.Model):
    image = models.ImageField(upload_to='successful_graduates/%Y/%m/%d/', blank=False, verbose_name='Изображение')
    content = models.TextField(blank=False, verbose_name='Контент')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Успешные выпускники'
        verbose_name_plural = 'Успешные выпускники'

    def __str__(self):
        return f"Успешные выпускники: {self.content[:20]}"


# Обращение к ученикам от Выпускников
class AppealToStudents(models.Model):
    title = models.CharField(max_length=50, blank=False, verbose_name='Заголовок')
    text = models.TextField(blank=False, verbose_name='Текст')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Обращение к ученикам'
        verbose_name_plural = 'Обращение к ученикам'

    def __str__(self):
        return self.title


# Выпускники
class Graduates(models.Model):
    image = models.ImageField(upload_to='graduates/%Y/%m/%d/', blank=False, verbose_name='Изображение')
    content = models.TextField(blank=False, verbose_name='Контент')
    name = models.CharField(max_length=25, blank=False, verbose_name='Имя')
    surname = models.CharField(max_length=25, blank=False, verbose_name='Фамилия')
    year = models.PositiveIntegerField(verbose_name='Год')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Выпускники'
        verbose_name_plural = 'Выпускники'

    def __str__(self):
        return f"Выпускники {self.year} года: {self.name} {self.surname}"


# Благодарственное письмо от Выпускников
class ThanksNoteFromGraduates(models.Model):
    title = models.CharField(max_length=50, blank=False, verbose_name='Заголовок')
    text = models.TextField(blank=False, verbose_name='Текст')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Благодарственное письмо'
        verbose_name_plural = 'Благодарственное письмо'

    def __str__(self):
        return self.title


# Новости
class News(models.Model):
    image = models.ImageField(upload_to='news/%Y/%m/%d/', blank=False, verbose_name='Изображение')
    content = models.TextField(blank=False, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return f'Новость от {self.created_at.strftime("%Y-%m-%d")}'


# Галерея
class Gallery(models.Model):
    title = models.CharField(max_length=50, blank=False, verbose_name='Заголовок')
    content = models.TextField(blank=False, verbose_name='Контент')
    image = models.ImageField(upload_to='gallery/%Y/%m/%d/', blank=False, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галерея'

    def __str__(self):
        return self.title or 'Без названия'


# Наши достижения
class OurAchievements(models.Model):
    content = models.TextField(blank=False, verbose_name='Контент')
    image = models.ImageField(upload_to='our_achievements/%Y/%m/%d/', blank=False, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Наши достижения'
        verbose_name_plural = 'Наши достижения'

    def __str__(self):
        return self.content[:50]


# Учителя
class Teachers(models.Model):
    Experience = (
        ('Год', '1'),
        ('От пяти лет', '5+'),
        ('От десяти лет', '10+'),
    )
    name = models.CharField(max_length=25, blank=False, verbose_name='Имя')
    surname = models.CharField(max_length=25, blank=False, verbose_name='Фамилия')
    experience = models.CharField(max_length=50, choices=Experience, verbose_name='Опыт')
    subject = models.CharField(max_length=20, verbose_name='Предмет')
    education = models.CharField(max_length=200, blank=True, verbose_name='Образование')
    successes = models.TextField(blank=True, verbose_name='Успехи')
    image = models.ImageField(upload_to='teachers_images/%Y/%m/%d/', blank=False, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Учителя'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return f"Учитель: {self.name} {self.surname} - Предмет: {self.subject}"


#Контакты
class Feedback(models.Model):
    phone_number = models.CharField(max_length=30, blank=False, unique=True, null=True, verbose_name='Номер телефона(+996)')
    address = models.CharField(max_length=200, blank=False, unique=True, null=True, verbose_name='Адрес')
    instagram = models.URLField(max_length=200, null=True, verbose_name='instagram')
    youtube = models.URLField(max_length=200, null=True, verbose_name='Youtube')
    telegram = models.URLField(max_length=200, null=True, verbose_name='telegram')

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f'Контакты'


#Комментарии
class Comments(models.Model):
    our_achievements = models.ForeignKey(
        OurAchievements, on_delete=models.CASCADE,
        null=True, blank=True, verbose_name='Связка с "Наши достижения"'
    )
    news = models.ForeignKey(
        News, on_delete=models.CASCADE,
        null=True, blank=True, verbose_name='Связка с "Новости"'
    )
    successful_graduates = models.ForeignKey(
        SuccessfulGraduates, on_delete=models.CASCADE,
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
    comment = models.ForeignKey(Comments, related_name='replies', on_delete=models.CASCADE, verbose_name='Комментарий')
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
    comment = models.ForeignKey(Comments, related_name='likes', on_delete=models.CASCADE, verbose_name='Комментарий')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        unique_together = ('comment', 'user')
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def __str__(self):
        return f'Лайк от {self.user.username} на комментарий {self.comment.id}'

