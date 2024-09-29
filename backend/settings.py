import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

TARGET_ENV = os.getenv('TARGET_ENV')

NOT_PROD = not TARGET_ENV.lower().startswith('prod')

SECRET_KEY = 'uzu10@1w@z!h*p-p#h)$pbc^fo6r__y-(+vg%6bucpvn4+nag_'

DEBUG = os.getenv('DEBUG', '0').lower() in ['true', 't', '1']

ALLOWED_HOSTS = [
    'myretrogamelist.azurewebsites.net',
    'localhost',
    '127.0.0.1',
]
CSRF_TRUSTED_ORIGINS = ['https://myretrogamelist.azurewebsites.net']

SECURE_SSL_REDIRECT = \
    os.getenv('SECURE_SSL_REDIRECT', '0').lower() in ['true', 't', '1']

if SECURE_SSL_REDIRECT:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myretrogamelistdb',
        'HOST': 'myretrogamelistdb.postgres.database.azure.com',
        'USER': 'admin_username',
        'PASSWORD': 'Django_no_sabado123',
        'OPTIONS': {'sslmode': 'require'},
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend',
    "whitenoise.runserver_nostatic",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC_URL = "static/"
STATIC_URL = os.environ.get('DJANGO_STATIC_URL', "/static/")
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = ('whitenoise.storage.CompressedManifestStaticFilesStorage')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = ['frontend.backends.EmailBackend', 'django.contrib.auth.backends.ModelBackend']

MEDIA_URL = 'frontend/static/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'frontend/static/media/')

SESSION_COOKIE_SECURE = True  # Only send cookies over HTTPS
CSRF_COOKIE_SECURE = True      # Only send CSRF cookies over HTTPS
CSRF_COOKIE_HTTPONLY = True     # Prevent JavaScript access to the CSRF cookie
