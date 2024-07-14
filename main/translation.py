from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Olympians)
class OlympiansTranslationOptions(TranslationOptions):
    pass


@register(SuccessfulGraduates)
class SuccessfulStudentsTranslationOptions(TranslationOptions):
    fields = ('content',)


@register(AppealToStudents)
class AppealToStudentsTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(Graduates)
class GraduatesTranslationOptions(TranslationOptions):
    pass


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('content',)


@register(OurAchievements)
class OurAchievementsTranslationOptions(TranslationOptions):
    fields = ('content',)


@register(Teachers)
class TeachersTranslationOptions(TranslationOptions):
    fields = ('subject', 'education', 'successes')
