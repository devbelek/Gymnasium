import django_filters
from django_filters import filters

from .models import Students, Graduates


class StudentsFilter(django_filters.FilterSet):
    full_name = filters.CharFilter(method='filter_by_full_name')
    class Meta:
        model = Students
        fields = {
            'school_class__grade': ['exact'],
        }

    def filter_by_full_name(self, queryset, name, value):
        return queryset.filter(
            Q(surname__icontains=value) |
            Q(name__icontains=value) |
            Q(last_name__icontains=value)
        )


class GraduatesFilter(django_filters.FilterSet):
    year = filters.NumberFilter(field_name='year', lookup_expr='exact')

    class Meta:
        model = Graduates
        fields = ['year']
