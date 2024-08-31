FROM python:3.11-slim-buster as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    tesseract-ocr-rus \
    poppler-utils \
    wget \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/usr/bin:/usr/local/bin:${PATH}"
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/tessdata

RUN mkdir -p $TESSDATA_PREFIX && \
    wget -q https://github.com/tesseract-ocr/tessdata_best/raw/main/rus.traineddata -O $TESSDATA_PREFIX/rus.traineddata && \
    wget -q https://github.com/tesseract-ocr/tessdata_best/raw/main/eng.traineddata -O $TESSDATA_PREFIX/eng.traineddata

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/media && chmod -R 777 /app/media

# Финальный этап
FROM python:3.11-slim-buster

WORKDIR /app

# Копируем приложение
COPY --from=builder /app /app

# Копируем установленные Python-пакеты и исполняемые файлы
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib /usr/local/lib

# Копируем дополнительные необходимые каталоги
COPY --from=builder /usr/share /usr/share
COPY --from=builder /usr/lib /usr/lib

ENV PYTHONUNBUFFERED=1
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/tessdata
ENV PATH="/usr/local/bin:${PATH}"

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "Gimnasium.wsgi:application"]
