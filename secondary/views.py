from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from .models import NameOfGrades, AdministratorTypes, NamesOfOlympia
from .serializers import NameOfGradesSerializer, AdministratorTypesSerializer, NamesOfOlympiaSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly


class NameOfGradesViewSet(viewsets.ModelViewSet):
    queryset = NameOfGrades.objects.all()
    serializer_class = NameOfGradesSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    @method_decorator(cache_page(60*15))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @method_decorator(cache_page(60*15))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class AdministratorTypesViewSet(viewsets.ModelViewSet):
    queryset = AdministratorTypes.objects.all()
    serializer_class = AdministratorTypesSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    @method_decorator(cache_page(60*15))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @method_decorator(cache_page(60*15))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class NamesOfOlympiaViewSet(viewsets.ModelViewSet):
    queryset = NamesOfOlympia.objects.all()
    serializer_class = NamesOfOlympiaSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    @method_decorator(cache_page(60*15))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @method_decorator(cache_page(60*15))
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)
