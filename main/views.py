from rest_framework import viewsets
from .models import *
from .serializers import *


class TeacherViews(viewsets.ModelViewSet):
    queryset = Teachers.objects.all()
    serializer_class = TeacherSerializers


class NewsViews(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializers


class GalleryViews(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializers


class GraduatesViews(viewsets.ModelViewSet):
    queryset = Graduates.objects.all()
    serializer_class = GraduatesSerializers


class OurAchievementsViews(viewsets.ModelViewSet):
    queryset = OurAchievements.objects.all()
    serializer_class = OurAchievementsSerializers


