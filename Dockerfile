# Використовуємо офіційний slim-образ (він менший за повний, але має все необхідне)
FROM python:3.12-slim

# Встановлюємо змінні оточення для оптимізації Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Вимикаємо створення venv всередині Docker, бо контейнер сам по собі ізольований
    POETRY_VIRTUALENVS_CREATE=false

# Встановлюємо робочу директорію
WORKDIR /app

# Встановлюємо системні залежності (потрібні для компіляції psycopg2 та інших ліб)
# curl - для встановлення poetry
# gcc, libpq-dev - для збірки python-пакетів (особливо для БД)
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Додаємо poetry до PATH
ENV PATH="/root/.local/bin:$PATH"

# КРОК ОПТИМІЗАЦІЇ: Копіюємо лише файли залежностей
COPY pyproject.toml poetry.lock ./

# Встановлюємо залежності (без dev-залежностей для продакшену, але поки можемо залишити всі)
# --no-root означає "не встановлюй сам проект як пакет", бо ми копіюємо код вручну
RUN poetry install --no-root --no-interaction --no-ansi

# Нарешті копіюємо сам код проекту
COPY app/ .

# Відкриваємо порт (інформативно, для документації)
EXPOSE 8000

# Команда запуску за замовчуванням (можна перевизначити в docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]