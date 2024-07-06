from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from .models import Feedback


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ['user', 'avatar', 'birth_date', 'updated_at']


class CommentSerializers(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comments
        fields = ['id', 'author', 'text', 'created_at']


class CommentReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = CommentReply
        fields = ['id', 'author', 'text', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'user']


class FeedbackSerializers(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class NamesOfOlympiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NamesOfOlympia
        fields = '__all__'


class NameOfGradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameOfGrades
        fields = '__all__'


class AdministratorTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministratorTypes
        fields = '__all__'


class StudentsSerializer(serializers.ModelSerializer):
    name_of_grade = NameOfGradesSerializer(read_only=True)
    olympian_status = NamesOfOlympiaSerializer(read_only=True)
    administrator_status = AdministratorTypesSerializer(read_only=True)

    class Meta:
        model = Students
        fields = ['id', 'name', 'surname', 'grade', 'name_of_grade', 'olympian_status', 'administrator_status']


class ThanksNoteFromStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThanksNoteFromStudents
        fields = '__all__'


class StudentMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ['name', 'surname']


class OlympiansSerializer(serializers.ModelSerializer):
    student = StudentMinimalSerializer(read_only=True)

    class Meta:
        model = Olympians
        fields = ['id', 'student']


class SuccessfulGraduatesSerializer(serializers.ModelSerializer):
    comments = CommentSerializers(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = SuccessfulGraduates
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
    comments = CommentSerializers(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = News
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class OurAchievementsSerializer(serializers.ModelSerializer):
    comments = CommentSerializers(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = OurAchievements
        fields = '__all__'


class TeachersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teachers
        fields = '__all__'
