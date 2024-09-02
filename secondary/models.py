from django.core.cache import cache
from django.db import models


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
        verbose_name = 'Добавить имени класса'
        verbose_name_plural = 'Добавить имена классов'
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
        verbose_name = 'Добавить должность среди учащихся'
        verbose_name_plural = 'Добавить должность среди учащихся'

    def __str__(self):
        return f"Тип должностного лица среди учащихся: {self.choosing}"


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
        verbose_name = 'Добавить название олимпиады'
        verbose_name_plural = 'Добавить названия олимпиад'

