from rest_framework import viewsets
from .models import *
from .serializers import *


class NameOfGradesViewSet(viewsets.ModelViewSet):
    queryset = NameOfGrades.objects.all()
    serializer_class = NameOfGradesSerializer


class AdministratorTypesViewSet(viewsets.ModelViewSet):
    queryset = AdministratorTypes.objects.all()
    serializer_class = AdministratorTypesSerializer


class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer


class ThanksNoteFromStudentsViewSet(viewsets.ModelViewSet):
    queryset = ThanksNoteFromStudents.objects.all()
    serializer_class = ThanksNoteFromStudentsSerializer


class NamesOfOlympiaViewSet(viewsets.ModelViewSet):
    queryset = NamesOfOlympia.objects.all()
    serializer_class = NamesOfOlympiaSerializer


class OlympiansViewSet(viewsets.ModelViewSet):
    queryset = Olympians.objects.all()
    serializer_class = OlympiansSerializer


class SuccessfulStudentsViewSet(viewsets.ModelViewSet):
    queryset = SuccessfulStudents.objects.all()
    serializer_class = SuccessfulStudentsSerializer


class AppealToStudentsViewSet(viewsets.ModelViewSet):
    queryset = AppealToStudents.objects.all()
    serializer_class = AppealToStudentsSerializer


class GraduatesViewSet(viewsets.ModelViewSet):
    queryset = Graduates.objects.all()
    serializer_class = GraduatesSerializer


class ThanksNoteFromGraduatesViewSet(viewsets.ModelViewSet):
    queryset = ThanksNoteFromGraduates.objects.all()
    serializer_class = ThanksNoteFromGraduatesSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class OurAchievementsViewSet(viewsets.ModelViewSet):
    queryset = OurAchievements.objects.all()
    serializer_class = OurAchievementsSerializer


class TeachersViewSet(viewsets.ModelViewSet):
    queryset = Teachers.objects.all()
    serializer_class = TeachersSerializer
