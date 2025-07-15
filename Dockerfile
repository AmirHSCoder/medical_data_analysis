FROM python:3.11-slim
ARG APP_PORT=8000
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE ${APP_PORT}
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
