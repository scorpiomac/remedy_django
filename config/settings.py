import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("REMEDY_SECRET_KEY", "change-me-in-production")
DEBUG = os.getenv("REMEDY_DEBUG", "1") == "1"
_hosts = os.getenv("REMEDY_ALLOWED_HOSTS", "localhost,127.0.0.1,217.65.144.109,remedy.tickets-place.net,www.remedy.tickets-place.net")
ALLOWED_HOSTS = [h.strip() for h in _hosts.split(",") if h.strip()]
# Toujours accepter le nom de domaine (évite 500 en accès par domaine si REMEDY_ALLOWED_HOSTS est partiel)
# Inclure avec et sans port (proxy peut envoyer Host avec :443)
for _host in (
    "remedy.tickets-place.net",
    "www.remedy.tickets-place.net",
    "remedy.tickets-place.net:443",
    "www.remedy.tickets-place.net:443",
    "remedy.tickets-place.net:80",
    "www.remedy.tickets-place.net:80",
    "remediafrica.com",
    "www.remediafrica.com",
    "remediafrica.com:443",
    "www.remediafrica.com:443",
    "remediafrica.com:80",
    "www.remediafrica.com:80",
):
    if _host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_host)
if DEBUG and "*" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.insert(0, "*")  # allow any host in dev for remote access

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "accounts",
    "claims",
]

MIDDLEWARE = [
    "config.middleware.Log500TracebackMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.remedy_user_role",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

if os.getenv("REMEDY_DB_USE_SQLITE", "").lower() in ("1", "true", "yes"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("REMEDY_DB_NAME", "remedy"),
            "USER": os.getenv("REMEDY_DB_USER", "remedy_user"),
            "PASSWORD": os.getenv("REMEDY_DB_PASSWORD", "change-me"),
            "HOST": os.getenv("REMEDY_DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("REMEDY_DB_PORT", "5432"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Africa/Dakar"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
# HTTPS (production uniquement)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email (demandes de démo, notifications)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("REMEDY_EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("REMEDY_EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("REMEDY_EMAIL_USE_TLS", "1").lower() in ("1", "true", "yes")
EMAIL_HOST_USER = os.getenv("REMEDY_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("REMEDY_EMAIL_HOST_PASSWORD", "")
_default_from = os.getenv("REMEDY_DEFAULT_FROM_EMAIL", "").strip()
DEFAULT_FROM_EMAIL = _default_from or (f"Remedi <{EMAIL_HOST_USER}>" if EMAIL_HOST_USER else "noreply@remediafrica.com")
# Adresse(s) qui reçoivent les notifications des demandes de démo (séparées par des virgules)
REMEDY_DEMO_NOTIFICATION_EMAILS = [e.strip() for e in os.getenv("REMEDY_DEMO_NOTIFICATION_EMAILS", "").split(",") if e.strip()]

# Log 500 and server errors to a file (path writable by the process running the app)
LOGS_DIR = BASE_DIR / "logs"
try:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
except OSError:
    LOGS_DIR = None
if LOGS_DIR is not None:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "error_file": {
                "level": "ERROR",
                "class": "logging.FileHandler",
                "filename": LOGS_DIR / "django_errors.log",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django.request": {
                "handlers": ["error_file"],
                "level": "ERROR",
                "propagate": False,
            },
        },
    }
else:
    LOGGING = {}
