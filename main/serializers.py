from rest_framework import serializers
from secondary.models import AdministratorTypes, NameOfGrades, NamesOfOlympia
from .models import *
from users.serializers import CommentSerializers
from secondary.serializers import NameOfGradesSerializer, NamesOfOlympiaSerializer, AdministratorTypesSerializer
from django.conf import settings


class MinimalSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'surname']


class StudentMinimalSerializer(MinimalSerializer):
    class Meta(MinimalSerializer.Meta):
        model = Students


class TeacherMinimalSerializer(MinimalSerializer):
    class Meta(MinimalSerializer.Meta):
        model = Teachers
        fields = MinimalSerializer.Meta.fields + ['last_name']


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']


class SchoolParliamentSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    type_of_administrator = serializers.SerializerMethodField()

    class Meta:
        model = SchoolParliament
        fields = ('student', 'type_of_administrator')

    def get_student(self, obj):
        return StudentMinimalSerializer(obj.student.all(), many=True).data

    def get_type_of_administrator(self, obj):
        return AdministratorTypesSerializer(AdministratorTypes.get_cached(id=obj.type_of_administrator_id)).data


class GimnasiumClassSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    name_of_grade = serializers.SerializerMethodField()

    class Meta:
        model = GimnasiumClass
        fields = ('student', 'name_of_grade')

    def get_student(self, obj):
        student = Students.get_cached(id=obj.student_id)
        if student is not None:
            return StudentMinimalSerializer(student).data
        return None

    def get_name_of_grade(self, obj):
        name_of_grade = NameOfGrades.get_cached(id=obj.name_of_grade_id)
        if name_of_grade is not None:
            return NameOfGradesSerializer(name_of_grade).data
        return None


class OlympiansSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    name_of_olympia = serializers.SerializerMethodField()

    class Meta:
        model = Olympians
        fields = ('id', 'student', 'name_of_olympia')

    def get_student(self, obj):
        return StudentMinimalSerializer(Students.get_cached(id=obj.student_id)).data

    def get_name_of_olympia(self, obj):
        return NamesOfOlympiaSerializer(NamesOfOlympia.get_cached(id=obj.name_of_olympia_id)).data


class ContactsSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Contacts


class TeachersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teachers
        fields = '__all__'


class StudentsSerializer(serializers.ModelSerializer):
    school_class = serializers.SerializerMethodField()
    olympian_status = serializers.SerializerMethodField()
    administrator_status = serializers.SerializerMethodField()
    classroom_teacher = serializers.SerializerMethodField()

    class Meta:
        model = Students
        fields = ['id', 'name', 'surname', 'last_name', 'school_class', 'olympian_status', 'administrator_status',
                  'classroom_teacher']

    def get_school_class(self, obj):
        return NameOfGradesSerializer(NameOfGrades.get_cached(id=obj.school_class_id)).data

    def get_olympian_status(self, obj):
        if obj.olympian_status_id:
            return NamesOfOlympiaSerializer(NamesOfOlympia.get_cached(id=obj.olympian_status_id)).data
        return None

    def get_administrator_status(self, obj):
        if obj.administrator_status_id:
            return AdministratorTypesSerializer(AdministratorTypes.get_cached(id=obj.administrator_status_id)).data
        return None

    def get_classroom_teacher(self, obj):
        return TeacherMinimalSerializer(obj.classroom_teacher.all(), many=True).data


class ThanksNoteFromStudentsSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ThanksNoteFromStudents


class GraduatesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Graduates


class SuccessfulGraduatesSerializer(BaseSerializer):
    comments = CommentSerializers(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    graduate = serializers.SerializerMethodField()

    class Meta(BaseSerializer.Meta):
        model = SuccessfulGraduates

    def get_graduate(self, obj):
        return GraduatesSerializer(Graduates.get_cached(id=obj.graduate_id)).data


class AppealToStudentsSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = AppealToStudents


class ThanksNoteFromGraduatesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ThanksNoteFromGraduates


class NewsSerializer(BaseSerializer):
    comments = CommentSerializers(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta(BaseSerializer.Meta):
        model = News


class GallerySerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Gallery


class OurAchievementsSerializer(BaseSerializer):
    comments = CommentSerializers(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta(BaseSerializer.Meta):
        model = OurAchievements
