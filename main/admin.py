from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

admin.site.register(Feedback)
admin.site.register(Comments)
admin.site.register(CommentReply)
admin.site.register(Like)
admin.site.register(UserProfile)


@admin.register(SuccessfulGraduates)
class SuccessfulGraduatesAdmin(TranslationAdmin):
    list_display = ("content",)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(AppealToStudents)
class AppealToStudentsAdmin(TranslationAdmin):
    list_display = ("title", "text")

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(ThanksNoteFromStudents)
class ThanksNoteFromStudentsAdmin(TranslationAdmin):
    list_display = ("title", "text")

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(ThanksNoteFromGraduates)
class ThanksNoteFromGraduatesAdmin(TranslationAdmin):
    list_display = ("title", "text")

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ("content",)
    fieldsets = [
        ('Русский перевод', {
            'fields': ['questions', 'answer']
        }),
        ('Кыргызский перевод', {
            'fields': ['questions_ky', 'answer_ky']
        }),
        ('Английский перевод', {
            'fields': ['questions_en', 'answer_en']
        }),
    ]


@admin.register(Gallery)
class GalleryAdmin(TranslationAdmin):
    list_display = ("title", "content")

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Students)
class StudentsAdmin(TranslationAdmin):
    list_display = ("name", "surname", "grade", "olympian_status")

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(OurAchievements)
class OurAchievementsAdmin(TranslationAdmin):
    list_display = ("content",)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Teachers)
class TeachersAdmin(TranslationAdmin):
    list_display = ("name", "surname", "experience", "subject")

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(NameOfGrades)
@admin.register(AdministratorTypes)
@admin.register(NamesOfOlympia)
class SimpleAdmin(admin.ModelAdmin):
    list_display = ("choosing",)
