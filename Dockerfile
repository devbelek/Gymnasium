FROM python:3.12

WORKDIR /app

# Установка необходимых системных пакетов
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    tesseract-ocr-rus \
    poppler-utils \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Добавление Tesseract в PATH и установка TESSDATA_PREFIX
ENV PATH="/usr/bin:${PATH}"
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/tessdata

# Создание директории для данных Tesseract и скачивание файлов данных
RUN mkdir -p $TESSDATA_PREFIX && \
    wget https://github.com/tesseract-ocr/tessdata_best/raw/main/rus.traineddata -O $TESSDATA_PREFIX/rus.traineddata && \
    wget https://github.com/tesseract-ocr/tessdata_best/raw/main/eng.traineddata -O $TESSDATA_PREFIX/eng.traineddata

# Проверка версии Tesseract и наличия файлов данных
RUN tesseract --version && \
    ls -l $TESSDATA_PREFIX

# Копирование и установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода проекта
COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Запуск миграций, создание суперпользователя и запуск сервера
CMD ["sh", "-c", "python manage.py migrate && python manage.py shell -c \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'root@example.com', 'root')\" && python manage.py runserver 0.0.0.0:8000"]

RUN echo "TESSDATA_PREFIX=$TESSDATA_PREFIX" && \
    ls -l $TESSDATA_PREFIX && \
    tesseract --list-langs