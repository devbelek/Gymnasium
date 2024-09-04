from rest_framework.views import APIView
from .models import UserProfile, Comment, CommentReply, Like, Donation, ConfirmedDonation
from .serializers import (
    UserProfileSerializers, CommentSerializers, CommentReplySerializers,
    LikeSerializers, RegisterSerializer, DonationSerializer, ConfirmedDonationSerializer
)
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from .tasks import verify_receipt
from loguru import logger
from django.core.exceptions import PermissionDenied


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info(f"Попытка регистрации нового пользователя с данными: {request.data}")
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Пользователь {serializer.data.get('username')} успешно зарегистрирован.")
            return Response({"message": "Пользователь успешно создан!"}, status=status.HTTP_201_CREATED)
        logger.warning(f"Ошибка регистрации пользователя: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DonationsViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all().order_by('-date')
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        logger.info(f"Пользователь {request.user.username} запросил список пожертвований.")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Пользователь {request.user.username} инициировал создание пожертвования.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        donation = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(f"Пожертвование ID: {donation.id} создано пользователем {request.user.username}.")
        return Response({"message": "Чек принят на проверку"}, status=status.HTTP_202_ACCEPTED, headers=headers)

    def perform_create(self, serializer):
        donation = serializer.save(user=self.request.user)
        if donation.confirmation_file:
            logger.info(f"Запуск задачи проверки чека для пожертвования ID: {donation.id}")
            verify_receipt.delay(donation.id)
        return donation

    def update(self, request, *args, **kwargs):
        logger.info(f"Пользователь {request.user.username} пытается обновить пожертвование ID: {kwargs.get('pk')}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info(f"Пользователь {request.user.username} пытается удалить пожертвование ID: {kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)


class ConfirmedDonationViewSet(viewsets.ModelViewSet):
    queryset = ConfirmedDonation.objects.all().order_by('-date')
    serializer_class = ConfirmedDonationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        logger.info(f"Пользователь {request.user.username} запросил список подтвержденных пожертвований.")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Пользователь {request.user.username} инициировал подтверждение пожертвования.")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Пользователь {request.user.username} обновляет подтвержденное пожертвование ID: {kwargs.get('pk')}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info(f"Пользователь {request.user.username} пытается удалить подтвержденное пожертвование ID: {kwargs.get('pk')}")
        return super().destroy(request, *args, **kwargs)


class UserProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers
    permission_classes = [IsAuthenticated]

    def get_object(self):
        logger.info(f"Пользователь {self.request.user.username} запрашивает свой профиль.")
        return self.request.user.profile

    def perform_update(self, serializer):
        logger.info(f"Пользователь {self.request.user.username} обновляет свой профиль.")
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        logger.info(f"Пользователь {request.user.username} запросил список комментариев.")
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        logger.info(f"Пользователь {self.request.user.username} создал комментарий ID: {serializer.instance.id}")

    def perform_destroy(self, instance):
        if instance.author == self.request.user:
            logger.info(f"Пользователь {self.request.user.username} удалил комментарий ID: {instance.id}")
            instance.delete()
        else:
            logger.warning(f"Пользователь {self.request.user.username} попытался удалить чужой комментарий ID: {instance.id}")

    def perform_update(self, serializer):
        if self.get_object().author == self.request.user:
            logger.info(f"Пользователь {self.request.user.username} обновил комментарий ID: {self.get_object().id}")
            serializer.save()
        else:
            logger.warning(f"Пользователь {self.request.user.username} попытался обновить чужой комментарий ID: {self.get_object().id}")
            raise PermissionDenied("Вы не можете редактировать этот комментарий")


class CommentReplyViewSet(viewsets.ModelViewSet):
    queryset = CommentReply.objects.all()
    serializer_class = CommentReplySerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        logger.info(f"Пользователь {request.user.username} запросил список ответов на комментарии.")
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        logger.info(f"Пользователь {self.request.user.username} создал ответ ID: {serializer.instance.id} на комментарий ID: {serializer.instance.comment.id}")

    def perform_destroy(self, instance):
        if instance.author == self.request.user:
            logger.info(f"Пользователь {self.request.user.username} удалил ответ ID: {instance.id}")
            instance.delete()
        else:
            logger.warning(f"Пользователь {self.request.user.username} попытался удалить чужой ответ ID: {instance.id}")

    def perform_update(self, serializer):
        if self.get_object().author == self.request.user:
            logger.info(f"Пользователь {self.request.user.username} обновил ответ ID: {self.get_object().id}")
            serializer.save()
        else:
            logger.warning(f"Пользователь {self.request.user.username} попытался обновить чужой ответ ID: {self.get_object().id}")
            raise PermissionDenied("Вы не можете редактировать этот ответ")


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        logger.info(f"Пользователь {request.user.username} запросил список лайков.")
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.info(f"Пользователь {self.request.user.username} поставил лайк на комментарий ID: {serializer.instance.comment.id}")

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            logger.info(f"Пользователь {self.request.user.username} удалил лайк с комментария ID: {instance.comment.id}")
            instance.delete()
        else:
            logger.warning(f"Пользователь {self.request.user.username} попытался удалить чужой лайк на комментарий ID: {instance.comment.id}")
