
FROM python:3.10
# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1
# Устанавливает рабочий каталог контейнера — "app"
WORKDIR /locallibrary

COPY . .


RUN apt-get update && apt-get install -y libpq-dev build-essential gcc
RUN pip install --no-cache-dir --requirement requirements.txt