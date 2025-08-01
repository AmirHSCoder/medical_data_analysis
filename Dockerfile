FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py train_model -d tests/fixtures
CMD ["uvicorn", "config.asgi:application", "--reload"]
