from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import AdministratorTypes, NameOfGrades, NamesOfOlympia, AboutUs, Contacts

admin.site.register(NameOfGrades)
admin.site.register(AdministratorTypes)
admin.site.register(AboutUs)
admin.site.register(Contacts)


@admin.register(NamesOfOlympia)
class NamesOfOlympiaAdmin(TranslationAdmin):
    list_display = ('choosing', )

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
