from modeltranslation.translator import register, TranslationOptions
from .models import *



@register(ThanksNoteFromStudents)
class ThanksNoteFromStudentsTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


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


@register(ThanksNoteFromGraduates)
class ThanksNoteFromGraduatesTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('content',)


@register(Gallery)
class GalleryTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(OurAchievements)
class OurAchievementsTranslationOptions(TranslationOptions):
    fields = ('content',)


@register(Teachers)
class TeachersTranslationOptions(TranslationOptions):
    fields = ('subject', 'education', 'successes')
