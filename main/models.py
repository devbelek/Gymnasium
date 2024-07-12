from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError


class SchoolParliament(models.Model):
    student = models.ManyToManyField('Students', blank=True, verbose_name='Ученик')
    type_of_administrator = models.ForeignKey('secondary.AdministratorTypes', on_delete=models.SET_NULL, blank=True, null=True,
                                              verbose_name='Должность')

    class Meta:
        verbose_name = 'Парламент нашей гимназии'
        verbose_name_plural = 'Парламент нашей гимназии'

    def __str__(self):
        students = ", ".join([student.name for student in self.student.all()])
        return f"Ученик: {students} - Должность: {self.type_of_administrator.choosing}"


# Студенты
class Students(models.Model):
    surname = models.CharField(max_length=25, blank=False, verbose_name='Фамилия')
    name = models.CharField(max_length=25, blank=False, verbose_name='Имя')
    last_name = models.CharField(max_length=25, blank=False, verbose_name='Отчество')
    school_class = models.ForeignKey('secondary.NameOfGrades', on_delete=models.CASCADE, verbose_name='Класс')

    olympian_status = models.ForeignKey('secondary.NamesOfOlympia', on_delete=models.CASCADE, null=True, blank=True,
                                        verbose_name='Олимпиец')
    administrator_status = models.ForeignKey('secondary.AdministratorTypes', on_delete=models.CASCADE, null=True, blank=True,
                                             verbose_name='Позиция')
    classroom_teacher = models.ManyToManyField('Teachers', blank=False,
                                               verbose_name='Классный руководитель')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        gimnasium_class, created = GimnasiumClass.objects.get_or_create(student=self,
                                                                        defaults={'name_of_grade': self.school_class})
        if not created:
            gimnasium_class.name_of_grade = self.school_class
            gimnasium_class.save()

        if self.olympian_status:
            olympian, created = Olympians.objects.get_or_create(student=self,
                                                                defaults={'name_of_olympia': self.olympian_status})
            if not created:
                olympian.name_of_olympia = self.olympian_status
                olympian.save()
        else:
            Olympians.objects.filter(student=self).delete()
        if self.administrator_status:
            parliament, created = SchoolParliament.objects.get_or_create(
                type_of_administrator=self.administrator_status)
            parliament.student.add(self)
        else:
            parliaments = SchoolParliament.objects.filter(student=self)
            for parliament in parliaments:
                parliament.student.remove(self)

    class Meta:
        verbose_name = 'Ученики'
        verbose_name_plural = 'Ученики'

    def __str__(self):
        return f'{self.name} {self.surname} {self.last_name}'


class GimnasiumClass(models.Model):
    student = models.OneToOneField(Students, on_delete=models.CASCADE, blank=True, verbose_name='Ученик')
    name_of_grade = models.ForeignKey('secondary.NameOfGrades', on_delete=models.CASCADE, blank=True, verbose_name='Класс')

    def __str__(self):
        return f'Ученик: {self.student.name} - Класс: {self.name_of_grade.grade} {self.name_of_grade.parallel}'

    class Meta:
        verbose_name = 'Классы Гимназии №3'
        verbose_name_plural = 'Классы Гимназии №3'


# Благодарственное письмо от Учащихся
class ThanksNoteFromStudents(models.Model):
    image = models.ImageField(upload_to='thanks_note_from_students_images/%Y/%m/%d/', blank=False,
                              verbose_name='Изображение')
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
    name_of_olympia = models.ForeignKey('secondary.NamesOfOlympia', on_delete=models.SET_NULL, null=True, verbose_name='Предмет')

    class Meta:
        verbose_name = 'Олимпийцы'
        verbose_name_plural = 'Олимпийцы'

    def __str__(self):
        return f"Олимпиец: {self.student.name} {self.student.surname} - Предмет: {self.name_of_olympia}"


# Успешные выпускники
class SuccessfulGraduates(models.Model):
    image = models.ImageField(upload_to='successful_graduates/%Y/%m/%d/', blank=False, verbose_name='Изображение')
    graduate = models.OneToOneField('Graduates', on_delete=models.CASCADE, verbose_name='Выберите его(её) из списка')
    content = models.TextField(blank=False, verbose_name='Контент')
    year = models.PositiveIntegerField(verbose_name='Год')

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
        verbose_name = 'Обращение к ученикам (от выпускников)'
        verbose_name_plural = 'Обращение к ученикам (от выпускников)'

    def __str__(self):
        return self.title


# Выпускники
class Graduates(models.Model):
    surname = models.CharField(max_length=25, blank=False, verbose_name='Фамилия')
    name = models.CharField(max_length=25, blank=False, verbose_name='Имя')
    last_name = models.CharField(max_length=25, blank=False, verbose_name='Отчество')
    graduate_year = datetime.now().year
    year = models.PositiveIntegerField(
        verbose_name='Год',
        validators=[MinValueValidator(2000), MaxValueValidator(graduate_year)]
    )

    class Meta:
        verbose_name = 'Выпускники'
        verbose_name_plural = 'Выпускники'

    def __str__(self):
        return f"Выпускники {self.year} года: {self.name} {self.surname}"


# Благодарственное письмо от Выпускников
class ThanksNoteFromGraduates(models.Model):
    image = models.ImageField(upload_to='thanks_note_from_graduates_images/%Y/%m/%d/', blank=False,
                              verbose_name='Изображение')
    title = models.CharField(max_length=50, blank=False, verbose_name='Заголовок')
    text = models.TextField(blank=False, verbose_name='Текст')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Благодарственное письмо (от выпускников)'
        verbose_name_plural = 'Благодарственное письмо (от выпускников)'

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
    image = models.ImageField(upload_to='gallery/%Y/%m/%d/', blank=False, verbose_name='Изображение')
    title = models.CharField(max_length=50, blank=False, verbose_name='Заголовок')
    content = models.TextField(blank=False, verbose_name='Контент')
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
        ('Год', 'Более 1 года'),
        ('От пяти лет', 'Более 5 лет'),
        ('От десяти лет', 'Более 15 лет'),
    )
    surname = models.CharField(max_length=25, blank=False, verbose_name='Фамилия')
    name = models.CharField(max_length=25, blank=False, verbose_name='Имя')
    last_name = models.CharField(max_length=25, blank=False, verbose_name='Отчество')
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


# Контакты
class Contacts(models.Model):
    phone_number = models.CharField(max_length=30, blank=False, unique=True, null=True,
                                    verbose_name='Номер телефона(+996)')
    address = models.CharField(max_length=200, blank=False, unique=True, null=True, verbose_name='Адрес')
    instagram = models.URLField(max_length=200, null=True, verbose_name='instagram')
    youtube = models.URLField(max_length=200, null=True, verbose_name='Youtube')
    telegram = models.URLField(max_length=200, null=True, verbose_name='telegram')

    class Meta:
        verbose_name = "Контакты"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f'Контакты'
