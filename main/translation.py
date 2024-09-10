from modeltranslation.translator import register, TranslationOptions
from .models import (
    SuccessfulGraduates,
    AppealToStudents,
    News,
    OurAchievements,
    Teachers,
    ThanksNoteFromGraduates,
    ThanksNoteFromStudents,
)
from secondary.models import NamesOfOlympia


@register(NamesOfOlympia)
class ThanksNoteFromGraduatesTranslationOptions(TranslationOptions):
    fields = ('choosing', )


@register(ThanksNoteFromGraduates)
class ThanksNoteFromGraduatesTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


@register(ThanksNoteFromStudents)
class ThanksNoteFromStudentsTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


@register(SuccessfulGraduates)
class SuccessfulGraduatesTranslationOptions(TranslationOptions):
    fields = ('content',)


@register(AppealToStudents)
class AppealToStudentsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('content', 'description')


@register(OurAchievements)
class OurAchievementsTranslationOptions(TranslationOptions):
    fields = ('content',)


@register(Teachers)
class TeachersTranslationOptions(TranslationOptions):
    fields = ('subject', 'education', 'successes')
