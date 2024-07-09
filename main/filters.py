import django_filters
from django_filters import filters

from .models import Students, Graduates


class StudentsFilter(django_filters.FilterSet):
    class Meta:
        model = Students
        fields = {
            'school_class__grade': ['exact'],
        }


class GraduatesFilter(django_filters.FilterSet):
    year = filters.NumberFilter(field_name='year', lookup_expr='exact')

    class Meta:
        model = Graduates
        fields = ['year']
