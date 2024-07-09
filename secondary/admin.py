from django.contrib import admin
from .models import AdministratorTypes, NameOfGrades, NamesOfOlympia

admin.site.register(NameOfGrades)
admin.site.register(AdministratorTypes)
admin.site.register(NamesOfOlympia)
