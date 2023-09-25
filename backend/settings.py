from django.core.management.utils import get_random_secret_key
from datetime import timedelta
from dotenv import load_dotenv
from pathlib import Path
import os

# Load env file
load_dotenv()

# Environment Variable declaration
DEBUG_ENV = os.environ.get('DEBUG')
EMAIL_PORT_ENV = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER_ENV = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD_ENV = os.environ.get('EMAIL_HOST_PASSWORD')
FRONTEND_DOMAIN_ENV = os.environ.get('FRONTEND_DOMAIN')
FRONTEND_SITE_NAME_ENV = os.environ.get('FRONTEND_SITE_NAME')
REDIRECT_URIS_ENV = os.environ.get('REDIRECT_URIS')
GOOGLE_AUTH_KEY_ENV = os.environ.get('GOOGLE_AUTH_KEY')
GOOGLE_AUTH_SECRET_KEY_ENV = os.environ.get('GOOGLE_AUTH_SECRET_KEY')

BASE_DIR = Path(__file__).resolve().parent.parent

# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if DEBUG_ENV == 'True' else False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps
    'authentication',

    # Packages
    'rest_framework',
    'djoser',
    'corsheaders',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
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

# Auth User Model
AUTH_USER_MODEL = 'authentication.User'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_DIR = BASE_DIR / 'static'
MEDIA_DIR = BASE_DIR / 'media'
MEDIA_ROOT = MEDIA_DIR
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Corsheaders
CORS_ALLOWED_ORIGINS = [
    f"{FRONTEND_DOMAIN_ENV}",
]
CSRF_COOKIE_SECURE = True if DEBUG_ENV == 'False' else False
SESSION_COOKIE_SECURE = True if DEBUG_ENV == 'False' else False 
SECURE_SSL_REDIRECT = True if DEBUG_ENV == 'False' else False
CORS_ALLOW_ALL_ORIGINS = True if DEBUG_ENV == 'True' else False

# Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "AUTH_HEADER_TYPES": ("JWT",),
}

# Email Setup
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = EMAIL_PORT_ENV
EMAIL_HOST_USER = EMAIL_HOST_USER_ENV
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD_ENV
EMAIL_USE_TLS = True
DOMAIN = FRONTEND_DOMAIN_ENV
SITE_NAME = FRONTEND_SITE_NAME_ENV


# Djoser Settings
DJOSER = {
    'LOGIN_FIELD': 'email',
    'SEND_ACTIVATION_EMAIL': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset-confirm/{uid}/{token}',
    'ACTIVATION_URL': 'users-activation/{uid}/{token}',
    'TOKEN_MODEL': None,
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': [REDIRECT_URIS_ENV],
}

# OAuth Settings
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

# Google OAuth2 Settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = GOOGLE_AUTH_KEY_ENV
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GOOGLE_AUTH_SECRET_KEY_ENV
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ['first_name', 'last_name']
SOCIAL_AUTH_RAISE_EXCEPTIONS = False