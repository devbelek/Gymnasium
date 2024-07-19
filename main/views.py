from rest_framework import viewsets, filters
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from .filters import StudentsFilter, GraduatesFilter
from .models import *
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.db.models.functions import Lower
import logging
logger = logging.getLogger('main')


class SchoolParliamentViewSet(viewsets.ModelViewSet):
    queryset = SchoolParliament.objects.all()
    serializer_class = SchoolParliamentSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class GimnasiumClassViewSet(viewsets.ModelViewSet):
    queryset = GimnasiumClass.objects.all()
    serializer_class = GimnasiumClassSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializers
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['school_class__grade', 'school_class__parallel']
    filterset_class = StudentsFilter
    search_fields = ['name', 'surname', 'last_name']
    ordering_fields = ['name', 'surname']
    logger.debug('working!')

class ThanksNoteFromStudentsViewSet(viewsets.ModelViewSet):
    queryset = ThanksNoteFromStudents.objects.all()
    serializer_class = ThanksNoteFromStudentsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class OlympiansViewSet(viewsets.ModelViewSet):
    queryset = Olympians.objects.all()
    serializer_class = OlympiansSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class SuccessfulGraduatesViewSet(viewsets.ModelViewSet):
    queryset = SuccessfulGraduates.objects.all()
    serializer_class = SuccessfulGraduatesSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class AppealToStudentsViewSet(viewsets.ModelViewSet):
    queryset = AppealToStudents.objects.all()
    serializer_class = AppealToStudentsSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class GraduatesViewSet(viewsets.ModelViewSet):
    queryset = Graduates.objects.all()
    serializer_class = GraduatesSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = GraduatesFilter


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