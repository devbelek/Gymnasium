from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile, Comment, CommentReply, Like
from .serializers import UserProfileSerializers, CommentSerializers, CommentReplySerializers, LikeSerializers


class UserProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
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
    serializer_class = CommentReplySerializers
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
    serializer_class = LikeSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Вы не можете удалить этот лайк"}, status=status.HTTP_403_FORBIDDEN)
