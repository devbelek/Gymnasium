from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class NameOfGradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameOfGrades
        fields = '__all__'


class AdministratorTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministratorTypes
        fields = '__all__'


class StudentsSerializer(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Students
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        student = Students.objects.create(user=user, **validated_data)
        return student


class ThanksNoteFromStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThanksNoteFromStudents
        fields = '__all__'


class NamesOfOlympiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NamesOfOlympia
        fields = '__all__'


class OlympiansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Olympians
        fields = '__all__'


class SuccessfulStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessfulStudents
        fields = '__all__'


class AppealToStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppealToStudents
        fields = '__all__'


class GraduatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graduates
        fields = '__all__'


class ThanksNoteFromGraduatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThanksNoteFromGraduates
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class OurAchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurAchievements
        fields = '__all__'


class TeachersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teachers
        fields = '__all__'
