from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from django.contrib.auth.models import User
from .models import UserProfile, Comment, CommentReply, Like, Donation, ConfirmedDonation
from .serializers import UserProfileSerializers, CommentSerializers, CommentReplySerializers, LikeSerializers, ConfirmedDonationSerializer, DonationSerializer
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os
import logging
from pdf2image import convert_from_path
import re


logger = logging.getLogger(__name__)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_pdf(pdf_path):
    try:
        pages = convert_from_path(pdf_path, 300)
        text = ""
        for i, page in enumerate(pages):
            img = enhance_image_from_image(page)
            if img:
                page_text = pytesseract.image_to_string(img, config='--oem 3 --psm 6')
                logger.debug(f"Extracted text from page {i + 1}: {page_text}")
                text += page_text
        return text
    except Exception as e:
        logger.error(f"Ошибка при извлечении текста из PDF: {e}")
        return ""

def enhance_image(image_path):
    try:
        img = Image.open(image_path)
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2.0)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        img = img.filter(ImageFilter.MedianFilter())
        logger.debug("Изображение успешно улучшено")
        return img
    except Exception as e:
        logger.error(f"Ошибка при улучшении изображения: {e}")
        return None

def enhance_image_from_image(img):
    try:
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2.0)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        img = img.filter(ImageFilter.MedianFilter())
        logger.debug("Изображение успешно улучшено")
        return img
    except Exception as e:
        logger.error(f"Ошибка при улучшении изображения: {e}")
        return None

class DonationsViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all().order_by('-date')
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        donation = serializer.save(user=self.request.user)
        if donation.confirmation_file:
            try:
                confirmation_file_path = donation.confirmation_file.path
                logger.debug(f"Путь к файлу подтверждения: {confirmation_file_path}")
                if not os.path.exists(confirmation_file_path):
                    raise FileNotFoundError(f"Файл подтверждения не найден: {confirmation_file_path}")

                # Проверяем, является ли файл PDF
                if confirmation_file_path.lower().endswith('.pdf'):
                    text = extract_text_from_pdf(confirmation_file_path)
                else:
                    img = enhance_image(confirmation_file_path)
                    if img is None:
                        raise Exception("Не удалось улучшить изображение")

                    text = pytesseract.image_to_string(img, config='--oem 3 --psm 6')

                logger.info(f"OCR Text: {text}")

                cleaned_text = re.sub(r'\s+', '', text).replace(",", ".")
                cleaned_amount = re.sub(r'\s+', '', str(donation.amount)).replace(",", ".")

                logger.info(f"Cleaned OCR Text: {cleaned_text}")
                logger.info(f"Cleaned Amount: {cleaned_amount}")

                # Проверка наличия суммы в тексте OCR
                if cleaned_amount in cleaned_text or f"{cleaned_amount}.00" in cleaned_text:
                    donation.is_verified = True
                    donation.save()
                    if not ConfirmedDonation.objects.filter(donation=donation).exists():
                        ConfirmedDonation.objects.create(
                            donation=donation,
                            user=donation.user,
                            comment=donation.comment
                        )
                        logger.info(f"ConfirmedDonation создан для Donation ID: {donation.id}")
                    else:
                        logger.info(f"Для Donation ID: {donation.id} уже существует подтверждение")
                else:
                    logger.info("Сумма пожертвования не найдена в тексте OCR")
            except FileNotFoundError as fnf_error:
                logger.error(f"Ошибка OCR: {fnf_error}")
            except pytesseract.TesseractError as tess_error:
                logger.error(f"Ошибка Tesseract OCR: {tess_error}")
            except Exception as e:
                logger.error(f"Неизвестная ошибка OCR: {e}")
        else:
            logger.info("Файл подтверждения отсутствует")

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
