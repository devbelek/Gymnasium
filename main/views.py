from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions, \
    DjangoModelPermissionsOrAnonReadOnly
from .models import *
from .serializers import *


class NameOfGradesViewSet(viewsets.ModelViewSet):
    queryset = NameOfGrades.objects.all()
    serializer_class = NameOfGradesSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class AdministratorTypesViewSet(viewsets.ModelViewSet):
    queryset = AdministratorTypes.objects.all()
    serializer_class = AdministratorTypesSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class ThanksNoteFromStudentsViewSet(viewsets.ModelViewSet):
    queryset = ThanksNoteFromStudents.objects.all()
    serializer_class = ThanksNoteFromStudentsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class NamesOfOlympiaViewSet(viewsets.ModelViewSet):
    queryset = NamesOfOlympia.objects.all()
    serializer_class = NamesOfOlympiaSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class OlympiansViewSet(viewsets.ModelViewSet):
    queryset = Olympians.objects.all()
    serializer_class = OlympiansSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class SuccessfulStudentsViewSet(viewsets.ModelViewSet):
    queryset = SuccessfulStudents.objects.all()
    serializer_class = SuccessfulStudentsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class AppealToStudentsViewSet(viewsets.ModelViewSet):
    queryset = AppealToStudents.objects.all()
    serializer_class = AppealToStudentsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class GraduatesViewSet(viewsets.ModelViewSet):
    queryset = Graduates.objects.all()
    serializer_class = GraduatesSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class ThanksNoteFromGraduatesViewSet(viewsets.ModelViewSet):
    queryset = ThanksNoteFromGraduates.objects.all()
    serializer_class = ThanksNoteFromGraduatesSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class OurAchievementsViewSet(viewsets.ModelViewSet):
    queryset = OurAchievements.objects.all()
    serializer_class = OurAchievementsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class TeachersViewSet(viewsets.ModelViewSet):
    queryset = Teachers.objects.all()
    serializer_class = TeachersSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]