from django.contrib import admin
from .models import AdministratorTypes, NameOfGrades, NamesOfOlympia

admin.site.register(NameOfGrades)
admin.site.register(AdministratorTypes)


@admin.register(NamesOfOlympia)
class NamesOfOlympiaAdmin(admin.ModelAdmin):
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
