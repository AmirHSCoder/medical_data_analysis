


# Getting Started
Clone the project
git clone ....
cd ....
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements/development.txt

# Install Django and ASGI server
pip install django uvicorn

# Using Poetry
The repository also contains a `pyproject.toml` so it can be managed with
[Poetry](https://python-poetry.org/). No lock file is committed and the
environment may not have network access. Running `poetry install` therefore
attempts to download packages from PyPI and can fail. If that happens, install
dependencies with the requirements file instead:

```bash
pip install -r requirements/development.txt
```

# Run the Project

# Export dev settings
export DJANGO_SETTINGS_MODULE=config.settings.dev
python manage.py migrate
python manage.py runserver
Or run with Uvicorn:
uvicorn config.asgi:application --reload



# Run all tests
pytest

# Run specific test file
pytest tests/unit/repositories/test_base_repository.py
pytest tests/unit/repositories/test_user_repository.py

# Run with verbose output
pytest -v