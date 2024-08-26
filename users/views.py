from rest_framework.views import APIView

from .models import UserProfile, Comment, CommentReply, Like, Donation, ConfirmedDonation
from .serializers import UserProfileSerializers, CommentSerializers, CommentReplySerializers, LikeSerializers, \
    RegisterSerializer
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from .models import Donation, ConfirmedDonation
from .serializers import DonationSerializer, ConfirmedDonationSerializer
from .tasks import verify_receipt
import logging
import os

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь успешно создан!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DonationsViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all().order_by('-date')
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        donation = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Чек принят на проверку"}, status=status.HTTP_202_ACCEPTED, headers=headers)

    def perform_create(self, serializer):
        donation = serializer.save(user=self.request.user)
        if donation.confirmation_file:
            verify_receipt.delay(donation.id)
        return donation


class ConfirmedDonationViewSet(viewsets.ModelViewSet):
    queryset = ConfirmedDonation.objects.all().order_by('-date')
    serializer_class = ConfirmedDonationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


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
            return Response({"message": "Вы не можете редактировать этот комментарий"},
                            status=status.HTTP_403_FORBIDDEN)


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


# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
