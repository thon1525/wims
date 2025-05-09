"""
Django settings for wims project.
Generated by 'django-admin startproject' using Django 5.1.3.
"""

import os
from datetime import timedelta
from pathlib import Path
import environ

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Security settings

SECRET_KEY = 'django-insecure-ct&57!crf=#rp+g#z@+dt-5*8b9kjx%m4nwdo5kx2ec+s32j)3'


# DEBUG = env.bool("DEBUG", default=True)  # Load from .env
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'wims-z0uz.onrender.com']
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrftoken",
    "accept",
    "origin",
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Vite dev server (corrected port)
    "https://frontendwimssystem.vercel.app",
    "https://frontendwimssystem-horn-thorns-projects.vercel.app",
    "https://frontendwimssystem-thon1525-horn-thorns-projects.vercel.app",
    "https://frontendwimssystem-ddoqmn99m-horn-thorns-projects.vercel.app",  # New domain from image
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "https://frontendwimssystem.vercel.app",
    "https://frontendwimssystem-horn-thorns-projects.vercel.app",
    "https://frontendwimssystem-thon1525-horn-thorns-projects.vercel.app",
    "https://frontendwimssystem-ddoqmn99m-horn-thorns-projects.vercel.app",
    "https://wims-z0uz.onrender.com",
]
CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_HTTPONLY = False


# Installed apps
INSTALLED_APPS = [
 
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
       "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "drf_spectacular",
      'wims', 
       'cloudinary',
    'cloudinary_storage',
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# JWT Signing & Verification Keys
SIGNING_KEY_PATH = env("SIGNING_KEY_PATH", default=os.path.join(BASE_DIR, "private_key.pem"))
VERIFYING_KEY_PATH = env("VERIFYING_KEY_PATH", default=os.path.join(BASE_DIR, "public_key.pem"))

def read_key_file(key_path):
    """Safely reads key files, returning None if missing."""
    if os.path.exists(key_path):
        with open(key_path, "r") as key_file:
            return key_file.read().strip()
    print(f"⚠️ Warning: Missing key file {key_path}. JWT authentication may not work correctly.")
    return None

SIGNING_KEY = read_key_file(SIGNING_KEY_PATH)
VERIFYING_KEY = read_key_file(VERIFYING_KEY_PATH)

# REST Framework Settings
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework_simplejwt.authentication.JWTAuthentication",'wims.authentication.CookieJWTAuthentication',
                                          'rest_framework.authentication.TokenAuthentication',  'rest_framework.authentication.SessionAuthentication'],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated",'rest_framework.permissions.AllowAny'],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'drknmxhog',
    'API_KEY': '621945364786363',
    'API_SECRET': 'urf8V8D6YSpXYxz_xM23rcMptzI',
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Spectacular API Schema settings
SPECTACULAR_SETTINGS = {
    "TITLE": "My API",
    "DESCRIPTION": "This is the API documentation for my Django application.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}


# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
#     "ALGORITHM": "RS256",
#     "SIGNING_KEY": SIGNING_KEY,
#     "VERIFYING_KEY": VERIFYING_KEY,
#     "AUTH_HEADER_TYPES": ("Bearer",),
#     "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
#     "USER_ID_FIELD": "id",
#     "USER_ID_CLAIM": "user_id",
#     "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
#     "TOKEN_TYPE_CLAIM": "token_type",
#     "JTI_CLAIM": "jti",
#     "AUTH_COOKIE": "access_token",
#     "AUTH_COOKIE_REFRESH": "refresh_token",
#     "AUTH_COOKIE_SECURE": not DEBUG,  # True in production
#     "AUTH_COOKIE_HTTP_ONLY": True,
#     "AUTH_COOKIE_PATH": "/",
#     "AUTH_COOKIE_SAMESITE": "None",  # Consistent with frontend
# }

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "RS256",
    "SIGNING_KEY": read_key_file(SIGNING_KEY_PATH),
    "VERIFYING_KEY": read_key_file(VERIFYING_KEY_PATH),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "AUTH_COOKIE": "access_token",
    "AUTH_COOKIE_REFRESH": "refresh_token",
    "AUTH_COOKIE_SECURE": True,  # Must be True in production
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_PATH": "/",
    "AUTH_COOKIE_SAMESITE": "None",  # Required for cross-domain
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "wims_system",  # Database name
        "USER": "avnadmin",  # Aiven MySQL username
        "PASSWORD": "AVNS_OM2K1NOjEDQxx1DfpJP",  # Aiven MySQL password
        "HOST": "mysql-dc5dfda-thonhourn1525-e634.h.aivencloud.com",
        "PORT": "22014",  # Aiven MySQL port
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# URLs and WSGI
ROOT_URLCONF = "wims.urls"
WSGI_APPLICATION = "wims.wsgi.application"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',  # Set to DEBUG to see all messages
    },
}
# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')