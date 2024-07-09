from rest_framework import viewsets
from .models import NameOfGrades, AdministratorTypes, NamesOfOlympia
from .serializers import NameOfGradesSerializer, AdministratorTypesSerializer, NamesOfOlympiaSerializer
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly


class NameOfGradesViewSet(viewsets.ModelViewSet):
    queryset = NameOfGrades.objects.all()
    serializer_class = NameOfGradesSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class AdministratorTypesViewSet(viewsets.ModelViewSet):
    queryset = AdministratorTypes.objects.all()
    serializer_class = AdministratorTypesSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class NamesOfOlympiaViewSet(viewsets.ModelViewSet):
    queryset = NamesOfOlympia.objects.all()
    serializer_class = NamesOfOlympiaSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
