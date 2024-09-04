from rest_framework import viewsets, filters
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .filters import StudentsFilter, GraduatesFilter
from .models import *
from .serializers import *
from loguru import logger
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings


class CachedViewSetMixin:
    @method_decorator(cache_page(settings.CACHE_TTL))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class BaseViewSet(CachedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    def list(self, request, *args, **kwargs):
        logger.info(f"Запрос списка объектов {self.__class__.__name__}")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Запрос объекта {self.__class__.__name__} с pk={kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Создание нового объекта {self.__class__.__name__}")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Обновление объекта {self.__class__.__name__} с pk={kwargs.get('pk')}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info(f"Удаление объекта {self.__class__.__name__} с pk={kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)


class StudentRelatedViewSet(BaseViewSet):
    filterset_class = StudentsFilter
    search_fields = ['name', 'surname', 'last_name']
    ordering_fields = ['name', 'surname']


class SchoolParliamentViewSet(BaseViewSet):
    queryset = SchoolParliament.objects.select_related('type_of_administrator').prefetch_related('student')
    serializer_class = SchoolParliamentSerializer


class GimnasiumClassViewSet(BaseViewSet):
    queryset = GimnasiumClass.objects.select_related('student', 'name_of_grade')
    serializer_class = GimnasiumClassSerializer


class StudentsViewSet(StudentRelatedViewSet):
    queryset = Students.objects.select_related('school_class', 'olympian_status',
                                               'administrator_status').prefetch_related('classroom_teacher')
    serializer_class = StudentsSerializer
    filterset_fields = ['school_class__grade', 'school_class__parallel']


class ThanksNoteViewSet(BaseViewSet):
    pass


class ThanksNoteFromStudentsViewSet(ThanksNoteViewSet):
    queryset = ThanksNoteFromStudents.objects.all()
    serializer_class = ThanksNoteFromStudentsSerializer


class OlympiansViewSet(BaseViewSet):
    queryset = Olympians.objects.select_related('student', 'name_of_olympia')
    serializer_class = OlympiansSerializer


class SuccessfulGraduatesViewSet(BaseViewSet):
    queryset = SuccessfulGraduates.objects.select_related('graduate')
    serializer_class = SuccessfulGraduatesSerializer


class AppealToStudentsViewSet(BaseViewSet):
    queryset = AppealToStudents.objects.all()
    serializer_class = AppealToStudentsSerializer


class GraduatesViewSet(BaseViewSet):
    queryset = Graduates.objects.select_related('kl_rukovoditel')
    serializer_class = GraduatesSerializer
    filterset_class = GraduatesFilter


class ThanksNoteFromGraduatesViewSet(ThanksNoteViewSet):
    queryset = ThanksNoteFromGraduates.objects.all()
    serializer_class = ThanksNoteFromGraduatesSerializer


class NewsViewSet(BaseViewSet):
    queryset = News.objects.select_related('author')
    serializer_class = NewsSerializer


class GalleryViewSet(BaseViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer


class OurAchievementsViewSet(BaseViewSet):
    queryset = OurAchievements.objects.all()
    serializer_class = OurAchievementsSerializer


class TeachersViewSet(BaseViewSet):
    queryset = Teachers.objects.all()
    serializer_class = TeachersSerializer
