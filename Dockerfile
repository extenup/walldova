# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения в контейнер
COPY . .

# Инициализируем базу данных
RUN python -c 'import app; app.init_db()'

# Указываем порт, который будет использоваться в контейнере
EXPOSE 8000

# Запуск приложения
CMD ["python", "app.py"]
