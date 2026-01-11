FROM python:3.12.3

WORKDIR /app

# Копируем только файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

CMD ["python", "main.py"]