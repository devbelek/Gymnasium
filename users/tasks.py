import os
import pytesseract
from PIL import Image
import pdf2image
import re
from celery import shared_task
from django.conf import settings
from .models import Donation
import cv2
import easyocr
import logging
from django.db import transaction

logger = logging.getLogger(__name__)

# os.environ['TESSDATA_PREFIX'] = '/opt/homebrew/share/tessdata'
# pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/tessdata'
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


def preprocess_image(image_path):
    try:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        processed_path = image_path.replace('.', '_processed.')
        cv2.imwrite(processed_path, threshold)
        logger.info(f"Обработанное изображение сохранено: {processed_path}")
        return processed_path
    except Exception as e:
        logger.error(f"Ошибка при обработке изображения: {str(e)}")
        return image_path


def extract_text_from_image_tesseract(image_path):
    try:
        processed_path = preprocess_image(image_path)
        text = pytesseract.image_to_string(Image.open(processed_path), lang='rus')
        logger.info(f"Текст Tesseract: {text}")
        return text
    except Exception as e:
        logger.error(f"Ошибка Tesseract: {str(e)}")
        return ""


def extract_text_from_image_easyocr(image_path):
    try:
        reader = easyocr.Reader(['ru'])
        result = reader.readtext(image_path)
        text = ' '.join([text for _, text, _ in result])
        logger.info(f"Текст EasyOCR: {text}")
        return text
    except Exception as e:
        logger.error(f"Ошибка EasyOCR: {str(e)}")
        return ""


def extract_text_from_pdf(pdf_path):
    try:
        pages = pdf2image.convert_from_path(pdf_path)
        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page, lang='rus')
        logger.info(f"Текст из PDF: {text}")
        return text
    except Exception as e:
        logger.error(f"Ошибка при обработке PDF: {str(e)}")
        return ""


def verify_receipt_content(text, donation_amount):
    try:
        logger.debug(f"Проверяемый текст: {text}")
        text_lower = re.sub(r'[^\w\s.,]', '', text.lower())
        keywords = ['чек', 'реквизит', 'итого', 'сумма', 'оплата', 'кассовый', 'приход', 'услуга', 'квитанция',
                    'успешно', 'комиссия', 'источник средств', 'оплачено', 'статус', 'получатель', 'отправитель',
                    'тип операции']
        found_keywords = [keyword for keyword in keywords if keyword in text_lower]
        logger.debug(f"Найденные ключевые слова: {found_keywords}")
        if not found_keywords:
            return False, "Ключевые слова не найдены"

        amounts = re.findall(r'\d+[.,]\d{2}(?:\s*сом)?', text_lower)
        logger.debug(f"Найденные суммы: {amounts}")
        if amounts:
            amounts = [float(re.sub(r'[^\d.,]', '', amount).replace(',', '.')) for amount in amounts]
            logger.debug(f"Суммы после преобразования: {amounts}")
            if any(abs(donation_amount - amount) < 0.01 for amount in amounts):
                return True, "Чек прошел проверку"
            else:
                return False, "Сумма в чеке не соответствует введенной сумме"
        else:
            return False, "Сумма платежа не найдена"

        date_match = re.search(r'\d{2}[./]\d{2}[./]\d{4}', text) or re.search(r'\d{2}[./]\d{2}[./]\d{4}\s*\d{2}:\d{2}',
                                                                              text)
        if not date_match:
            return False, "Дата не найдена"

        return True, "Чек прошел проверку"
    except Exception as e:
        logger.error(f"Ошибка при проверке чека: {str(e)}")
        return False, "Ошибка при проверке чека"


@shared_task
def verify_receipt(donation_id):
    logger.info(f"Начало verify_receipt для id: {donation_id}")
    try:
        with transaction.atomic():
            donation = Donation.objects.select_for_update().get(id=donation_id)
            file_path = os.path.join(settings.MEDIA_ROOT, str(donation.confirmation_file))
            logger.info(f"Обработка файла: {file_path}")
            logger.info(f"Текущее состояние: is_verified={donation.is_verified}")

            if file_path.lower().endswith('.pdf'):
                text = extract_text_from_pdf(file_path)
            else:
                text_tesseract = extract_text_from_image_tesseract(file_path)
                text_easyocr = extract_text_from_image_easyocr(file_path)
                text = text_tesseract if len(text_tesseract) > len(text_easyocr) else text_easyocr

            logger.info(f"Извлеченный текст: {text}")
            try:
                donation_amount = float(donation.amount)
            except ValueError:
                logger.error("Ошибка преобразования суммы пожертвования в число.")
                return False, "Ошибка преобразования суммы пожертвования в число."

            is_valid, message = verify_receipt_content(text, donation_amount)
            logger.info(f"Результат проверки: valid={is_valid}, message={message}")

            donation.is_verified = is_valid
            logger.info(f"Перед сохранением: is_verified={donation.is_verified}")
            donation.save()
            logger.info(f"После сохранения: is_verified={donation.is_verified}")

        donation.refresh_from_db()
        logger.info(f"Финальное состояние: is_verified={donation.is_verified}")
        return is_valid, message
    except Donation.DoesNotExist:
        logger.error(f"Donation id {donation_id} не найден")
        return False, f"Donation id {donation_id} не найден"
    except Exception as e:
        logger.error(f"Ошибка при проверке чека: {str(e)}", exc_info=True)
        return False, f"Ошибка при проверке чека: {str(e)}"
    finally:
        logger.info(f"Завершение verify_receipt для id: {donation_id}")
