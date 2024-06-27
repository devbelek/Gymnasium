from rest_framework import serializers
from .models import *


class TeacherSerializers(serializers.ModelSerializer):
    class Meta:
        model = Teachers
        fields = '__all__'


class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class OurAchievementsSerializers(serializers.ModelSerializer):
    class Meta:
        model = OurAchievements
        fields = '__all__'


class GraduatesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Graduates
        fields = '__all__'


class GallerySerializers(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

