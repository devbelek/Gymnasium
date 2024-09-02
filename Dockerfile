FROM python:3.11-slim-bullseye

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
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

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "4", "--threads", "2", "--worker-class", "gthread", "--timeout", "120", "Gimnasium.wsgi:application"]
