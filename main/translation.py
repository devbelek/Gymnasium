from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Olympians)
class OlympiansTranslationOptions(TranslationOptions):
    fields = ('name_of_olympia',)


@register(SuccessfulGraduates)
class SuccessfulStudentsTranslationOptions(TranslationOptions):
    fields = ('content',)


@register(AppealToStudents)
class AppealToStudentsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(Graduates)
class GraduatesTranslationOptions(TranslationOptions):
    fields = ('ort',)  # Добавляем поле, если оно должно быть переведено


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('content',)


@register(OurAchievements)
class OurAchievementsTranslationOptions(TranslationOptions):
    fields = ('content',)


@register(Teachers)
class TeachersTranslationOptions(TranslationOptions):
    fields = ('subject', 'education', 'successes')