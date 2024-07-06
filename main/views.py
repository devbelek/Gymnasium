from rest_framework import viewsets, status, generics
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from .models import *
from .serializers import *


class UserProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author == self.request.user:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Вы не можете удалить этот комментарий"}, status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        if self.get_object().author == self.request.user:
            serializer.save()
        else:
            return Response({"message": "Вы не можете редактировать этот комментарий"}, status=status.HTTP_403_FORBIDDEN)


class CommentReplyViewSet(viewsets.ModelViewSet):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author == self.request.user:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Вы не можете удалить этот ответ"}, status=status.HTTP_403_FORBIDDEN)

    def perform_update(self, serializer):
        if self.get_object().author == self.request.user:
            serializer.save()
        else:
            return Response({"message": "Вы не можете редактировать этот ответ"}, status=status.HTTP_403_FORBIDDEN)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Вы не можете удалить этот лайк"}, status=status.HTTP_403_FORBIDDEN)


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializers
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


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