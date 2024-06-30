from django.db import models
from django.contrib.auth.models import User


# Добавление имен классов в котором учатся ученики
class NameOfGrades(models.Model):
    choosing = models.CharField(max_length=20, blank=False, unique=True, verbose_name='Выбор/Тандоо')

    class Meta:
        verbose_name = 'Класстардын аталышы / Название классов'
        verbose_name_plural = 'Класстардын аталышы / Название классов'

    def __str__(self):
        return self.choosing


# Должности среди учащихся (Президент и тд)
class AdministratorTypes(models.Model):
    choosing = models.CharField(max_length=50, blank=False, unique=True, verbose_name='Выбор/Тандоо')

    class Meta:
        verbose_name = 'Должности среди учащихся / Студенттер арасындагы позициялар'
        verbose_name_plural = 'Должности среди учащихся / Студенттер арасындагы позициялар'

    def __str__(self):
        return f"Тип должностного лица среди учащихся: {self.choosing}"


# Имя олимпиады
class NamesOfOlympia(models.Model):
    choosing = models.CharField(max_length=20, blank=False, unique=True, verbose_name='Выбор/Тандоо')

    class Meta:
        verbose_name = 'Название олимпиады / Олимпиаданын аталышы'
        verbose_name_plural = 'Название олимпиады / Олимпиаданын аталышы'

    def __str__(self):
        return self.choosing


# Студенты
class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
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
    name = models.CharField(max_length=25, blank=False, verbose_name='Имя/Аты')
    surname = models.CharField(max_length=25, blank=False, verbose_name='Фамилия')
    grade = models.CharField(max_length=50, choices=CHOICES_GRADE, blank=False, verbose_name='Класс')
    name_of_grade = models.ForeignKey(NameOfGrades, on_delete=models.CASCADE, verbose_name='Название класса/Классынын '
                                                                                           'аты')
    olympian_status = models.ForeignKey(NamesOfOlympia, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Олимпийц')
    administrator_status = models.ForeignKey(AdministratorTypes, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Позициясы')

    class Meta:
        verbose_name = 'Ученики/Окуучулар'
        verbose_name_plural = 'Ученики/Окуучулар'

    def __str__(self):
        return f"{self.name} {self.surname} - Класс {self.get_grade_display()} - Название класса {self.name_of_grade}"


# Благодарственное письмо от Учащихся
class ThanksNoteFromStudents(models.Model):
    title = models.CharField(max_length=50, blank=False, verbose_name='Заголовок/Кириш сөз')
    text = models.TextField(blank=False, verbose_name='Текст')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки/Чыгаруу күнү')

    class Meta:
        verbose_name = 'Благодарственное письмо (от учеников) / Ыраазычылык кат (окуучулардан)'
        verbose_name_plural = 'Благодарственное письмо (от учеников) / Ыраазычылык кат (окуучулардан)'

    def __str__(self):
        return self.title


# Олимпийцы
class Olympians(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name='Окуучу')

    class Meta:
        verbose_name = 'Олимпийцы / Олимпиецтер'
        verbose_name_plural = 'Олимпийцы / Олимпиецтер'

    def __str__(self):
        return f"Олимпиец: {self.student.name} {self.student.surname}"


# Успешные студенты
class SuccessfulStudents(models.Model):
    image = models.ImageField(upload_to='successful_students/%Y/%m/%d/', blank=False, verbose_name='Изображение/Сүрөт')
    content = models.TextField(blank=False, verbose_name='Контент')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки/Чыгаруу күнү')

    class Meta:
        verbose_name = 'Успешные выпускники / Ийгиликтүү бүтүрүүчүлөр'
        verbose_name_plural = 'Успешные выпускники / Ийгиликтүү бүтүрүүчүлөр'

    def __str__(self):
        return f"Успешные выпускники: {self.content[:20]}"


# Обращение к ученикам от Выпускников
class AppealToStudents(models.Model):
    title = models.CharField(max_length=50, blank=False, verbose_name='Заголовок/Кириш сөз')
    text = models.TextField(blank=False, verbose_name='Текст')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки/Чыгаруу күнү')

    class Meta:
        verbose_name = 'Обращение к ученикам / Окуучуларга бүтүрүүчүлөрдөн кайрылуу'
        verbose_name_plural = 'Обращение к ученикам / Окуучуларга бүтүрүүчүлөрдөн кайрылуу'

    def __str__(self):
        return self.title


# Выпускники
class Graduates(models.Model):
    image = models.ImageField(upload_to='graduates/%Y/%m/%d/', blank=False, verbose_name='Изображение/Сүрөт')
    content = models.TextField(blank=False, verbose_name='Контент')
    name = models.CharField(max_length=25, blank=False, verbose_name='Имя/Аты')
    surname = models.CharField(max_length=25, blank=False, verbose_name='Фамилия')
    year = models.PositiveIntegerField(verbose_name='Год/Жылы')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки/Чыгаруу күнү')

    class Meta:
        verbose_name = 'Выпускники / Бүтүрүүчүлөр'
        verbose_name_plural = 'Выпускники / Бүтүрүүчүлөр'

    def __str__(self):
        return f"Выпускники {self.year} года: {self.name} {self.surname}"


# Благодарственное письмо от Выпускников
class ThanksNoteFromGraduates(models.Model):
    title = models.CharField(max_length=50, blank=False, verbose_name='Заголовок/Кириш сөз')
    text = models.TextField(blank=False, verbose_name='Текст')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки/Чыгаруу күнү')

    class Meta:
        verbose_name = 'Благодарственное письмо / Ыраазычылык кат'
        verbose_name_plural = 'Благодарственное письмо / Ыраазычылык кат'

    def __str__(self):
        return self.title


# Новости
class News(models.Model):
    image = models.ImageField(upload_to='news/%Y/%m/%d/', blank=False, verbose_name='Изображение/Сүрөт')
    content = models.TextField(blank=False, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания/Жаралуу күнү')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки/Чыгаруу күнү')

    class Meta:
        verbose_name = 'Новости / Жаңылыктар'
        verbose_name_plural = 'Новости / Жаңылыктар'

    def __str__(self):
        return self.title


# Галерея
class Gallery(models.Model):
    title = models.CharField(max_length=50, blank=False, verbose_name='Заголовок/Кириш сөз')
    content = models.TextField(blank=False, verbose_name='Контент')
    image = models.ImageField(upload_to='gallery/%Y/%m/%d/', blank=False, verbose_name='Изображение/Сүрөт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания/Жаралуу күнү')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата загрузки/Чыгаруу күнү')

    class Meta:
        verbose_name = 'Галерея / Галерея'
        verbose_name_plural = 'Галерея / Галерея'

    def __str__(self):
        return self.title or 'Без названия'


# Наши достижения
class OurAchievements(models.Model):
    content = models.TextField(blank=False, verbose_name='Контент')
    image = models.ImageField(upload_to='our_achievements/%Y/%m/%d/', blank=False, verbose_name='Изображение/Сүрөт')

    class Meta:
        verbose_name = 'Наши достижения / Биздин жетишкендиктерибиз'
        verbose_name_plural = 'Наши достижения / Биздин жетишкендиктер'

    def __str__(self):
        return self.content[:50]


# Учителя
class Teachers(models.Model):
    Experience = (
        ('Год', '1'),
        ('От пяти лет', '5+'),
        ('От десяти лет', '10+'),
    )
    name = models.CharField(max_length=25, blank=False, verbose_name='Имя/Аты')
    surname = models.CharField(max_length=25, blank=False, verbose_name='Фамилия')
    experience = models.CharField(max_length=50, choices=Experience, verbose_name='Опыт/Тажрыйбасы')
    subject = models.CharField(max_length=20, verbose_name='Предмет/Сабак')
    education = models.CharField(max_length=200, blank=True, verbose_name='Образование/Билими')
    successes = models.TextField(blank=True, verbose_name='Успехи/Ийгиликтери')
    image = models.ImageField(upload_to='teachers_images/%Y/%m/%d/', blank=False, verbose_name='Изображение/Сүрөт')

    class Meta:
        verbose_name = 'Учителя / Мугалимдер'
        verbose_name_plural = 'Учителя / Мугалимдер'

    def __str__(self):
        return f"Учитель: {self.name} {self.surname} - Предмет: {self.subject}"


# Форум
class Forum(models.Model):
    pass

    class Meta:
        verbose_name = 'Форум / Форум'
        verbose_name_plural = 'Форум / Форум'

    def __str__(self):
        return f"Форум #{self.id}"

