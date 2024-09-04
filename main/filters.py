import django_filters
from django.db.models import Q
from .models import Students, Graduates


class StudentsFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(method='filter_by_full_name')

    class Meta:
        model = Students
        fields = {
            'school_class__grade': ['exact'],
        }

    def filter_by_full_name(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                Q(name__icontains=value) |
                Q(surname__icontains=value) |
                Q(last_name__icontains=value)
            )
        return queryset


class GraduatesFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='year', lookup_expr='exact')

    class Meta:
        model = Graduates
        fields = ['year']
