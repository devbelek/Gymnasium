from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group


# Добавление имен классов в котором учатся ученики
class NameOfGrades(models.Model):
    choosing = models.CharField(max_length=20, blank=False, unique=True)

    def __str__(self):
        return self.choosing


# Должности среди учащихся (Президент и тд)
class AdministratorTypes(models.Model):
    choosing = models.CharField(max_length=20, blank=False, unique=True)

    def __str__(self):
        return f"Тип должностного лица среди учащихся: {self.choosing}"


# Имя олимпиады
class NamesOfOlympia(models.Model):
    choosing = models.CharField(max_length=20, blank=False, unique=True)

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
    CHOICES_OLYMPIAN_OR_NO = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    name = models.CharField(max_length=25, blank=False)
    sourname = models.CharField(max_length=25, blank=False)
    grade = models.CharField(max_length=50, choices=CHOICES_GRADE, blank=False)
    name_of_grade = models.ForeignKey(NameOfGrades, on_delete=models.CASCADE)
    olympian_status = models.ForeignKey(NamesOfOlympia, on_delete=models.CASCADE, null=True)
    administrator_status = models.ForeignKey(AdministratorTypes, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"{self.name} {self.sourname} - Класс {self.get_grade_display()} - Название класса {self.name_of_grade}"


# Благодарственное письмо от Учащихся
class ThanksNoteFromStudents(models.Model):
    title = models.CharField(max_length=50, blank=False)
    text = models.TextField(blank=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Олимпийцы
class Olympians(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)

    def __str__(self):
        return f"Олимпиец: {self.student.name} {self.student.sourname}"


# Успешные студенты
class SuccessfulStudents(models.Model):
    image = models.ImageField(upload_to='successful_students/', blank=False)
    content = models.TextField(blank=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Успешные выпускники: {self.content[:20]}"


# Обращение к ученикам от Выпускников
class AppealToStudents(models.Model):
    title = models.CharField(max_length=50, blank=False)
    text = models.TextField(blank=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Выпускники
class Graduates(models.Model):
    name = models.CharField(max_length=25, blank=False)
    sourname = models.CharField(max_length=25, blank=False)
    year = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Выпускники {self.year} года: {self.name} {self.sourname}"


# Благодарственное письмо от Выпускников
class ThanksNoteFromGraduates(models.Model):
    title = models.CharField(max_length=50, blank=False)
    text = models.TextField(blank=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Новости
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Галерея
class Gallery(models.Model):
    title = models.CharField(max_length=20, blank=True)
    content = models.TextField(max_length=200, blank=True)
    images = models.ImageField(upload_to='gallery_images/', blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or 'Без названия'


# Наши достижения
class OurAchievements(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='achievements_images/', blank=False)

    def __str__(self):
        return self.content[:50]


# Учителя
class Teachers(models.Model):
    Experience = (
        ('Год', '1'),
        ('От пяти лет', '5+'),
        ('От десяти лет', '10+'),
    )
    name = models.CharField(max_length=20, blank=False)
    surname = models.CharField(max_length=20, blank=False)
    experience = models.CharField(max_length=50, choices=Experience)
    subject = models.CharField(max_length=20)
    education = models.CharField(max_length=200, blank=True)
    successes = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='teachers_images/', blank=False)

    def __str__(self):
        return f"Учитель: {self.name} {self.surname} - Предмет: {self.subject}"


# Форум
class Forum(models.Model):
    pass

    def __str__(self):
        return f"Форум #{self.id}"
