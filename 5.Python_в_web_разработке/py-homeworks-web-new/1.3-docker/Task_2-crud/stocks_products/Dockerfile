# Устанавливаем базовый образ Python и Alpine Linux
FROM python:3.12-alpine

# Установка компилятора gcc для Alpine Linux
RUN apk add --no-cache gcc musl-dev

# Устанавливаем рабочую директорию в контейнере
WORKDIR /stocks_products

# Копируем файл requirements.txt локального проекта в WORKDIR контейнера
COPY ./requirements.txt ./requirements.txt

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Указываем порт, который будет слушать сервер
EXPOSE 8000

# !ЭТИ СЕКЦИИ (COPY, RUN, EXPOSE) ПЕРЕМЕЩЕНЫ ВВЕРХ ДЛЯ УСКОРЕНИЯ СБОРКИ ОБРАЗА ЗА СЧЕТ КЕШИРОВАНИЯ: 
# Параметры секций, код проекта, requirements не должны меняться после сборки образа, 
# иначе переместить их ниже секции COPY . .!

# Копируем файлы локального проекта в WORKDIR контейнера
COPY . .

# Команда на запуск сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
