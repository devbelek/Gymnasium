from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin
from .utils import generate_csv_file, generate_excel_file


admin.site.register(Contacts)
admin.site.register(Graduates)
admin.site.register(ThanksNoteFromGraduates)
admin.site.register(ThanksNoteFromStudents)
admin.site.register(SchoolParliament)
admin.site.register(GimnasiumClass)
admin.site.register(Gallery)


@admin.register(Olympians)
class OlympiansAdmin(admin.ModelAdmin):
    readonly_fields = ['student', 'name_of_olympia']


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


@admin.register(News)
class NewsAdmin(TranslationAdmin):
    list_display = ("content",)
    fieldsets = []

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
class StudentsAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "school_class")
    actions = ['download_csv', 'download_excel']

    def download_csv(self, request, queryset):
        return generate_csv_file(queryset)

    download_csv.short_description = 'Скачать список студентов в формате CSV'

    def download_excel(self, request, queryset):
        return generate_excel_file(queryset)

    download_excel.short_description = 'Скачать список студентов в формате Excel'

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

