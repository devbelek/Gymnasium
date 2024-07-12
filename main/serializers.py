from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from users.serializers import CommentSerializers
from secondary.serializers import NameOfGradesSerializer, NamesOfOlympiaSerializer, AdministratorTypesSerializer
from secondary.models import NameOfGrades, NamesOfOlympia, AdministratorTypes


class StudentMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['name', 'surname']


class SchoolParliamentSerializer(serializers.ModelSerializer):
    student = StudentMinimalSerializer(read_only=True, many=True)
    type_of_administrator = AdministratorTypesSerializer(read_only=True)

    class Meta:
        model = SchoolParliament
        fields = ('student', 'type_of_administrator')


class GimnasiumClassSerializer(serializers.ModelSerializer):
    student = StudentMinimalSerializer(read_only=True)
    name_of_grade = NameOfGradesSerializer(read_only=True)

    class Meta:
        model = GimnasiumClass
        fields = ('student', 'name_of_grade')


class OlympiansSerializer(serializers.ModelSerializer):
    student = StudentMinimalSerializer(read_only=True)
    name_of_olympia = NamesOfOlympiaSerializer(read_only=True)

    class Meta:
        model = Olympians
        fields = ('id', 'student', 'name_of_olympia')


class ContactsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'


class TeachersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teachers
        fields = ['name', 'surname', 'last_name']


class StudentsSerializer(serializers.ModelSerializer):
    school_class = NameOfGradesSerializer(read_only=True)
    olympian_status = NamesOfOlympiaSerializer(read_only=True)
    administrator_status = AdministratorTypesSerializer(read_only=True)
    classroom_teacher = TeachersSerializer(many=True, read_only=True)

    class Meta:
        model = Students
        fields = ['id', 'name', 'surname', 'last_name', 'school_class', 'olympian_status', 'administrator_status', 'classroom_teacher']


class ThanksNoteFromStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThanksNoteFromStudents
        fields = ['title', 'text', 'updated_at']


class GraduatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graduates
        fields = ['name', 'surname', 'last_name', 'year']


class SuccessfulGraduatesSerializer(serializers.ModelSerializer):
    comments = CommentSerializers(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    graduate = GraduatesSerializer(read_only=True)
    class Meta:
        model = SuccessfulGraduates
        fields = ['image', 'graduate', 'content', 'comments', 'author']


class AppealToStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppealToStudents
        fields = ['title', 'text', 'updated_at']


class ThanksNoteFromGraduatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThanksNoteFromGraduates
        fields = ['title', 'text', 'updated_at']


class NewsSerializer(serializers.ModelSerializer):
    comments = CommentSerializers(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = News
        fields = ['image', 'content', 'created_at', 'updated_at', 'comments', 'author']


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ['title', 'content', 'image', 'created_at', 'updated_at']


class OurAchievementsSerializer(serializers.ModelSerializer):
    comments = CommentSerializers(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = OurAchievements
        fields = '__all__'
