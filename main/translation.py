from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Students)
class StudentsTranslationOptions(TranslationOptions):
    fields = ('olympian_status',)


@register(NameOfGrades)
class NameOfGradesTranslationOptions(TranslationOptions):
    pass


@register(AdministratorTypes)
class AdministratorTypesTranslationOptions(TranslationOptions):
    pass


@register(NamesOfOlympia)
class NamesOfOlympiaTranslationOptions(TranslationOptions):
    fields = ('choosing',)


@register(ThanksNoteFromStudents)
class ThanksNoteFromStudentsTranslationOptions(TranslationOptions):
    fields = ('title', 'text')


@register(Olympians)
class OlympiansTranslationOptions(TranslationOptions):
    pass


@register(SuccessfulStudents)
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


@register(Forum)
class ForumTranslationOptions(TranslationOptions):
    pass
