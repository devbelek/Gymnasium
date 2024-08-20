FROM python:3.12

WORKDIR /app

# Установка зависимостей и утилит
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    tesseract-ocr-rus \
    poppler-utils \
    wget \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/bin:${PATH}"
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/tessdata

# Загрузка данных Tesseract
RUN mkdir -p $TESSDATA_PREFIX && \
    wget https://github.com/tesseract-ocr/tessdata_best/raw/main/rus.traineddata -O $TESSDATA_PREFIX/rus.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata_best/raw/main/eng.traineddata -O $TESSDATA_PREFIX/eng.traineddata

# Проверка установки Tesseract
RUN tesseract --version && \
    ls -l $TESSDATA_PREFIX

# Установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

ENV PYTHONUNBUFFERED=1

# Создание директории для MEDIA_ROOT и установка прав
RUN mkdir -p /app/media && \
    chmod -R 755 /app/media

# Открытие порта
EXPOSE 8000

# Команда для миграций и создания суперпользователя, если он не существует
CMD ["sh", "-c", "python manage.py migrate && python manage.py shell -c \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'root@example.com', 'root')\" && python manage.py runserver 0.0.0.0:8000"]

RUN echo "TESSDATA_PREFIX=$TESSDATA_PREFIX" && \
    ls -l $TESSDATA_PREFIX && \
    tesseract --list-langs
