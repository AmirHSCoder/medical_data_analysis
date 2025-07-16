# Medical Data Analysis Service

This project provides a small Django API for uploading medical CSV data,
training a machine learning model and retrieving the results. The service
stores datasets and model output in MongoDB and exposes REST endpoints for
interactive use.

## Getting started

1. Clone the repository and create a virtual environment:
   ```bash
   git clone https://github.com/AmirHSCoder/medical_data_analysis.git
   cd medical_data_analysis
   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   as an alternative you can use poetry to manage dependencies.
2. Copy `.env` and adjust the values for your environment. Important
   settings include `MONGO_HOST`, `MONGO_NAME`, `MONGO_PORT`,
   `MONGO_USERNAME` and `MONGO_PASSWORD`.
3. Apply database migrations and run the development server:
   ```bash
   export DJANGO_SETTINGS_MODULE=config.settings
   python manage.py migrate
   python manage.py runserver
   ```
   You can alternatively launch with Uvicorn:
   ```bash
   uvicorn config.asgi:application --reload
   ```

## Production deployment

A `Dockerfile` and `docker-compose.yml` are provided. Build the image and
start the containers with:
```bash
docker-compose up --build
```
Ensure environment variables from `.env` are set appropriately (disable
`DEBUG` and configure `ALLOWED_HOSTS`).

## Training the model

Data can be trained locally using the management command:
```bash
python manage.py train_model -d path/to/data
```

example:
```bash
python manage.py train_model -d tests/fixtures
```

The directory must contain `cross.csv` and `long.csv`. The command loads the
files, trains a RandomForest classifier and stores the merged data and model
results in MongoDB.

## Available APIs

All API endpoints require a valid JWT token.

- `POST /api/token/` – obtain a token using username and password.
- `POST /api/token/refresh/` – refresh an access token.
- `GET  /api/rf_result/` – latest classification report.
- `GET  /api/y_result/` – probability predictions for the last run.
- `GET  /api/data/` – merged dataset used for training.

## Running tests

Execute all tests with:
```bash
pytest
```
