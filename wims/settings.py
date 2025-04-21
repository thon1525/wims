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
SECRET_KEY = env("SECRET_KEY", default="django-insecure-ct&57!crf=#rp+g#z@+dt-5*8b9kjx%m4nwdo5kx2ec+s32j)3")
DEBUG = env.bool("DEBUG", default=True)  # Set to False in production

# Allowed hosts for the application
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "wims-z0uz.onrender.com",  # Render deployment domain
]

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = ["content-type", "authorization", "cookie"]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Vite dev server
    "https://frontendwimssystem.vercel.app",
    "https://frontendwimssystem-git-main-horn-thorns-projects.vercel.app",
    "https://frontendwimssystem-bgpd58gcp-horn-thorns-projects.vercel.app",
    "https://frontendwimssystem-qdhpj45z7u-horn-thorns-projects.vercel.app",
]

# CSRF Configuration
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "https://frontendwimssystem.vercel.app",
    "https://frontendwimssystem-git-main-horn-thorns-projects.vercel.app",
    "https://frontendwimssystem-bgpd58gcp-horn-thorns-projects.vercel.app",
    "https://frontendwimssystem-qdhpj45z7u-horn-thorns-projects.vercel.app",
    "https://wims-z0uz.onrender.com",  # Backend domain
]
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = "None"  # Required for cross-origin requests
CSRF_COOKIE_SECURE = not DEBUG  # Secure in production
SESSION_COOKIE_SECURE = not DEBUG  # Secure in production
SESSION_COOKIE_SAMESITE = "None"  # Required for cross-origin cookies

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
    "wims",  # Your custom app
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Must be before CommonMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# JWT Signing & Verification Keys for RS256
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
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # Header-based JWT
        "wims.authentication.CookieJWTAuthentication",  # Custom cookie-based JWT
        "rest_framework.authentication.TokenAuthentication",  # Optional
        "rest_framework.authentication.SessionAuthentication",  # Optional
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",  # Allow unauthenticated access by default
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Spectacular API Schema settings
SPECTACULAR_SETTINGS = {
    "TITLE": "WIMS API",
    "DESCRIPTION": "API documentation for the WIMS Django application.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# Simple JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "RS256",  # Requires private_key.pem and public_key.pem
    "SIGNING_KEY": SIGNING_KEY,
    "VERIFYING_KEY": VERIFYING_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "AUTH_COOKIE": "access_token",  # Cookie name for access token
    "AUTH_COOKIE_REFRESH": "refresh_token",  # Cookie name for refresh token
    "AUTH_COOKIE_SECURE": not DEBUG,  # Secure in production
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_PATH": "/",
    "AUTH_COOKIE_SAMESITE": "None",  # Required for cross-origin cookies
}

# Database Configuration (Aiven MySQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME", default="wims_system"),
        "USER": env("DB_USER", default="avnadmin"),
        "PASSWORD": env("DB_PASSWORD", default="AVNS_OM2K1NOjEDQxx1DfpJP"),
        "HOST": env("DB_HOST", default="mysql-dc5dfda-thonhourn1525-e634.h.aivencloud.com"),
        "PORT": env("DB_PORT", default="22014"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Security Headers
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

# Logging Configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",  # Useful for troubleshooting
    },
}

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static and Media Files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"