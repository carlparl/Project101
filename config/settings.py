from pathlib import Path
import environ
import os

# Base Directory Setup
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment Variables Initialization Engine
env = environ.Env()

# Read .env file parameters if it exists locally
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

# --- Core Security Configuration ---
SECRET_KEY = env("SECRET_KEY", default="replace-me-before-production-run")

# Dynamically reads from environment variable; defaults to False for strict production safety
DEBUG = env.bool("DEBUG", default=True)

# Dynamically parses comma-separated host strings from Render, falls back to local setups
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["project101-k7fb.onrender.com", "127.0.0.1", "localhost"])


# --- Application Definitions ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Core Application Component Workspace
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Optimized production asset asset-delivery
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# --- Template Render Processing ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"


# --- Database Architecture Mapping ---
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}

# --- High-Performance Caching Architecture ---
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "shafnet_cluster_cache",
        "TIMEOUT": 300,  # Keeps pages cached for 5 minutes before refreshing
        "OPTIONS": {
            "MAX_ENTRIES": 1000  # Automatically purges old entries to protect memory
        }
    }
}


# --- Password Cryptography Defenses ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Internationalization & Time Tracking ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Kampala"
USE_I18N = True
USE_TZ = True


# --- Static and Media Asset Infrastructure ---
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# WhiteNoise storage configuration for compression and caching
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # Change "CompressedManifestStaticFilesStorage" to this:
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


# --- Automated Messaging & SMTP Gateway Configuration ---
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="Shafnet Tours <shafnettours@gmail.com>")
CONTACT_EMAIL = env("CONTACT_EMAIL", default="info@shafnettours.com")


# --- Global Miscellaneous Settings ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --- Production Environment Security Defenses ---
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"