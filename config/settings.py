import os
from pathlib import Path
import environ
import os

env = environ.Env()

if env.int('DJANGO_READ_ENV_FILE', 1):
    BASE_DIR = Path(__file__).resolve().parent.parent
    env_file = os.environ.get("DJANGO_ENV_FILE", BASE_DIR / ".env")
    environ.Env.read_env(env_file)

SECRET_KEY = env("DJANGO_SECRET_KEY", default='unsafe-default')

DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=['*'])

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'apps.analysis',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = []

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

USE_HTTPS = env.bool("USE_HTTPS", default=True)
RATE_LIMIT = env.int("RATE_LIMIT", default=100)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MONGO_HOST = env('MONGO_HOST', default='localhost')
MONGO_PORT = env('MONGO_PORT', default='27017')
MONGO_NAME = env('MONGO_NAME', default='default')
MONGO_USERNAME = env('MONGO_USERNAME', default='')
MONGO_PASSWORD = env('MONGO_PASSWORD', default='')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

STATIC_URL = '/static/'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env("TIME_ZONE", default="UTC")

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
