from django.core.cache import cache
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from loguru import logger


class NameOfGrades(models.Model):
    GRADE_CHOICES = (
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
    )
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, verbose_name='Класс')
    parallel = models.CharField(max_length=1, verbose_name='Параллель', help_text='Например, А, Б, В и т.д.')

    def __str__(self):
        return f"{self.grade}{self.parallel}"

    @staticmethod
    def get_cached(id):
        cache_key = f'name_of_grades_{id}'
        result = cache.get(cache_key)
        if not result:
            result = NameOfGrades.objects.get(id=id)
            cache.set(cache_key, result, timeout=60*15)  # Кэшируем на 15 минут
        return result

    class Meta:
        verbose_name = 'класс'
        verbose_name_plural = 'Добавить классы'
        unique_together = ('grade', 'parallel')


class AdministratorTypes(models.Model):
    choosing = models.CharField(max_length=50, blank=False, unique=True, verbose_name='Выбор')

    def __str__(self):
        return f"Тип должностного лица среди учащихся: {self.choosing}"

    @staticmethod
    def get_cached(id):
        cache_key = f'administrator_types_{id}'
        result = cache.get(cache_key)
        if not result:
            result = AdministratorTypes.objects.get(id=id)
            cache.set(cache_key, result, timeout=60*15)
        return result

    class Meta:
        verbose_name = 'должность среди учащихся'
        verbose_name_plural = 'Добавить должности среди учащихся'


class NamesOfOlympia(models.Model):
    choosing = models.CharField(max_length=20, blank=False, unique=True, verbose_name='Название олимпиады')

    def __str__(self):
        return self.choosing

    @staticmethod
    def get_cached(id):
        cache_key = f'names_of_olympia_{id}'
        result = cache.get(cache_key)
        if not result:
            result = NamesOfOlympia.objects.get(id=id)
            cache.set(cache_key, result, timeout=60*15)
        return result

    class Meta:
        verbose_name = 'олимпиаду'
        verbose_name_plural = 'Добавить олимпиады'


class AboutUs(models.Model):
    years_for_school = models.PositiveIntegerField(
        validators=[MaxValueValidator(999)],
        blank=False,
        verbose_name='Годы работы школы'
    )
    students = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999)],
        blank=False,
        verbose_name='Количество учащихся'
    )
    graduates_per_year = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999)],
        blank=False,
        verbose_name='Выпускников в год'
    )
    count_books = models.PositiveIntegerField(
        validators=[MaxValueValidator(999999)],
        blank=False,
        verbose_name='Количество книг'
    )

    class Meta:
        verbose_name = 'Мы в цифрах'
        verbose_name_plural = 'Мы в цифрах'


class Contacts(models.Model):
    phone_number = models.CharField(max_length=30, unique=True, null=True, verbose_name=_('Номер телефона(+996)'))
    address = models.CharField(max_length=200, unique=True, null=True, verbose_name=_('Адрес'))
    instagram = models.URLField(null=True, verbose_name=_('Instagram'))
    youtube = models.URLField(null=True, verbose_name=_('Youtube'))
    telegram = models.URLField(null=True, verbose_name=_('Telegram'))

    class Meta:
        verbose_name = _("Обратная связь")
        verbose_name_plural = _("Обратная связь")

    def __str__(self):
        return 'Контакты'

    def save(self, *args, **kwargs):
        if not self.pk:
            logger.info("Создание новой записи контактов")
        else:
            logger.info("Обновление записи контактов")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        logger.info("Удаление записи контактов")
        super().delete(*args, **kwargs)
