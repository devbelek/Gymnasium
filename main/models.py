from datetime import datetime
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from loguru import logger


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            logger.info(f"Создание новой записи {self.__class__.__name__}")
        else:
            logger.info(f"Обновление записи {self.__class__.__name__} (id: {self.pk})")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info(f"Удаление записи {self.__class__.__name__} (id: {self.pk})")
        super().delete(*args, **kwargs)


class PersonModel(models.Model):
    surname = models.CharField(max_length=25, db_index=True, verbose_name=_('Фамилия'))
    name = models.CharField(max_length=25, db_index=True, verbose_name=_('Имя'))
    last_name = models.CharField(max_length=25, verbose_name=_('Отчество'))

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['surname', 'name']),
        ]

    def __str__(self):
        return f"{self.surname} {self.name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.pk:
            logger.info(f"Создание новой записи {self.__class__.__name__}: {self}")
        else:
            logger.info(f"Обновление записи {self.__class__.__name__}: {self}")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info(f"Удаление записи {self.__class__.__name__}: {self}")
        super().delete(*args, **kwargs)


class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name=_('Изображение'))

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            logger.info(f"Загрузка нового изображения для {self.__class__.__name__}")
        else:
            logger.info(f"Обновление изображения для {self.__class__.__name__} (id: {self.pk})")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info(f"Удаление изображения для {self.__class__.__name__} (id: {self.pk})")
        super().delete(*args, **kwargs)


class ContentModel(models.Model):
    content = models.TextField(verbose_name=_('Контент'))

    class Meta:
        abstract = True


class TitleModel(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name=_('Заголовок'))

    class Meta:
        abstract = True


class Students(PersonModel, ImageModel):
    school_class = models.ForeignKey('secondary.NameOfGrades', on_delete=models.CASCADE, verbose_name=_('Класс'))
    olympian_status = models.ForeignKey('secondary.NamesOfOlympia', on_delete=models.SET_NULL, null=True, blank=True,
                                        verbose_name=_('Олимпиец'))
    administrator_status = models.ForeignKey('secondary.AdministratorTypes', on_delete=models.SET_NULL, null=True,
                                             blank=True, verbose_name=_('Позиция'))
    classroom_teacher = models.ManyToManyField('Teachers', verbose_name=_('Классный руководитель'))

    class Meta:
        verbose_name = _('Ученики')
        verbose_name_plural = _('Ученики')
        indexes = [
            models.Index(fields=['school_class']),
            models.Index(fields=['olympian_status']),
            models.Index(fields=['administrator_status']),
        ]

    @staticmethod
    def get_cached(id):
        cache_key = f'students_{id}'
        result = cache.get(cache_key)
        if not result:
            try:
                result = Students.objects.get(id=id)
                cache.set(cache_key, result, timeout=60 * 15)
            except Students.DoesNotExist:
                logger.error(f"Студент с ID {id} не существует.")
                result = None
        return result

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_gimnasium_class()
        self._update_olympian_status()
        self._update_parliament_status()
        logger.info(f"Обновлены связанные записи для ученика: {self.id}")

    def _update_gimnasium_class(self):
        GimnasiumClass.objects.update_or_create(
            student=self,
            defaults={'name_of_grade': self.school_class}
        )

    def _update_olympian_status(self):
        if self.olympian_status:
            Olympians.objects.update_or_create(
                student=self,
                defaults={'name_of_olympia': self.olympian_status}
            )
        else:
            Olympians.objects.filter(student=self).delete()

    def _update_parliament_status(self):
        if self.administrator_status:
            parliament, _ = SchoolParliament.objects.get_or_create(
                type_of_administrator=self.administrator_status)
            parliament.student.add(self)
        else:
            parliaments = SchoolParliament.objects.filter(student=self)
            for parliament in parliaments:
                parliament.student.remove(self)


class SchoolParliament(models.Model):
    student = models.ManyToManyField(Students, blank=True, verbose_name=_('Ученик'))
    type_of_administrator = models.ForeignKey('secondary.AdministratorTypes', on_delete=models.SET_NULL, blank=True,
                                              null=True, verbose_name=_('Должность'))

    class Meta:
        verbose_name = _('Парламент нашей гимназии')
        verbose_name_plural = _('Парламент нашей гимназии')

    def __str__(self):
        return f"Парламент ID: {self.id} - Должность: {self.type_of_administrator_id}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"Создание новой записи в парламенте: Парламент ID {self.id}")
        else:
            logger.info(f"Обновление записи в парламенте: Парламент ID {self.id}")

    def delete(self, *args, **kwargs):
        logger.info(f"Удаление записи из парламента: Парламент ID {self.id}")
        super().delete(*args, **kwargs)

    def get_students_count(self):
        return self.student.count()

    def get_students_list(self):
        return ", ".join(str(student.id) for student in self.student.all())


class GimnasiumClass(models.Model):
    student = models.OneToOneField(Students, on_delete=models.CASCADE, verbose_name=_('Ученик'))
    name_of_grade = models.ForeignKey('secondary.NameOfGrades', on_delete=models.CASCADE, verbose_name=_('Класс'))

    class Meta:
        verbose_name = _('Классы Гимназии №3')
        verbose_name_plural = _('Классы Гимназии №3')

    def __str__(self):
        return f'Ученик: {self.student.name} - Класс: {self.name_of_grade}'

    def save(self, *args, **kwargs):
        if not self.pk:
            logger.info(f"Создание новой записи класса: {self}")
        else:
            logger.info(f"Обновление записи класса: {self}")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info(f"Удаление записи класса: {self}")
        super().delete(*args, **kwargs)


class ThanksNoteFromStudents(ImageModel, TitleModel, ContentModel, TimestampedModel):
    class Meta:
        verbose_name = _('Благодарственное письмо (от учеников)')
        verbose_name_plural = _('Благодарственное письмо (от учеников)')

    def __str__(self):
        return f'{self.title}'


class Olympians(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, verbose_name=_('Ученик'))
    name_of_olympia = models.ForeignKey('secondary.NamesOfOlympia', on_delete=models.SET_NULL, null=True,
                                        verbose_name=_('Предмет'))

    class Meta:
        verbose_name = _('Олимпийцы')
        verbose_name_plural = _('Олимпийцы')

    def __str__(self):
        return f"Олимпиец: {self.student} - Предмет: {self.name_of_olympia}"

    def save(self, *args, **kwargs):
        if not self.pk:
            logger.info(f"Создание новой записи олимпийца: {self}")
        else:
            logger.info(f"Обновление записи олимпийца: {self}")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info(f"Удаление записи олимпийца: {self}")
        super().delete(*args, **kwargs)


class SuccessfulGraduates(ImageModel, ContentModel):
    graduate = models.OneToOneField('Graduates', on_delete=models.CASCADE, verbose_name=_('Выберите его(её) из списка'))
    year = models.PositiveIntegerField(verbose_name=_('Год'))

    class Meta:
        verbose_name = _('Успешные выпускники')
        verbose_name_plural = _('Успешные выпускники')

    def __str__(self):
        return f"Успешные выпускники: {self.content[:20]}"

    def save(self, *args, **kwargs):
        if not self.pk:
            logger.info(f"Создание новой записи успешного выпускника: {self}")
        else:
            logger.info(f"Обновление записи успешного выпускника: {self}")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info(f"Удаление записи успешного выпускника: {self}")
        super().delete(*args, **kwargs)


class AppealToStudents(TitleModel, ContentModel, TimestampedModel):
    class Meta:
        verbose_name = _('Обращение к ученикам (от выпускников)')
        verbose_name_plural = _('Обращение к ученикам (от выпускников)')


class Graduates(PersonModel):
    @staticmethod
    def get_current_year():
        return datetime.now().year

    year = models.PositiveIntegerField(
        verbose_name=_('Год'),
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(get_current_year())
        ]
    )
    ort = models.PositiveSmallIntegerField(verbose_name=_('ОРТ'), blank=False)
    kl_rukovoditel = models.ForeignKey(
        'Teachers',
        on_delete=models.CASCADE,
        related_name='graduates_teachers',
        verbose_name=_('Классный руководитель')
    )

    class Meta:
        verbose_name = _('Выпускники')
        verbose_name_plural = _('Выпускники')

    @staticmethod
    def get_cached(id):
        key = f"graduate_{id}"
        result = cache.get(key)
        if result is None:
            try:
                result = Graduates.objects.get(id=id)
                cache.set(key, result)
            except Graduates.DoesNotExist:
                result = None
        return result

    def __str__(self):
        return f"Выпускники {self.year} года: {self.name} {self.surname}"


class ThanksNoteFromGraduates(ImageModel, TitleModel, ContentModel, TimestampedModel):
    class Meta:
        verbose_name = _('Благодарственное письмо (от выпускников)')
        verbose_name_plural = _('Благодарственное письмо (от выпускников)')

    def __str__(self):
        return f'{self.title}'


class News(ImageModel, ContentModel, TimestampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Автор'))
    description = models.CharField(max_length=300, verbose_name=_('Описание'))
    
    class Meta:
        verbose_name = _('Новости')
        verbose_name_plural = _('Новости')

    def __str__(self):
        return f'Новость от {self.created_at.strftime("%Y-%m-%d")}'


class Gallery(ImageModel, ContentModel):
    title = models.CharField(max_length=200, verbose_name=_('Заголовок'))
    url_video = models.URLField(verbose_name=_('Ссылка на видео'), blank=True)

    class Meta:
        verbose_name = _('Галерея')
        verbose_name_plural = _('Галерея')

    def __str__(self):
        return self.title


class OurAchievements(ImageModel, ContentModel):
    class Meta:
        verbose_name = _('Наши достижения')
        verbose_name_plural = _('Наши достижения')

    def __str__(self):
        return self.content[:50]


class Teachers(PersonModel, ImageModel):
    EXPERIENCE_CHOICES = [
        ('Год', _('Более 1 года')),
        ('От пяти лет', _('Более 5 лет')),
        ('От десяти лет', _('Более 15 лет')),
    ]
    experience = models.CharField(max_length=200, choices=EXPERIENCE_CHOICES, verbose_name=_('Опыт'))
    subject = models.CharField(max_length=200, verbose_name=_('Предмет'))
    education = models.TextField(blank=True, verbose_name=_('Образование'))
    successes = models.TextField(blank=True, verbose_name=_('Успехи'))

    class Meta:
        verbose_name = _('Учителя')
        verbose_name_plural = _('Учителя')

    def __str__(self):
        return f"Учитель: {self.name} {self.surname} - Предмет: {self.subject}"

