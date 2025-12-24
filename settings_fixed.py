import os
import warnings
from .settings_common import *  # noqa

# =================================================
# 1. CONFIGURATION RÉSEAU & SÉCURITÉ
# =================================================
DEBUG = True
ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ("127.0.0.1", "0.0.0.0")

HOSTNAME = "100.42.186.218:81"
DOMAIN_NAME = "http://100.42.186.218:81"

SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

CSRF_TRUSTED_ORIGINS = [
    "http://100.42.186.218:81",
    "http://100.42.186.218",
    "http://localhost:81"
]

# =================================================
# 2. BASE DE DONNÉES (CORRECTION ERREUR READONLY)
# =================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "temba",
        "USER": "temba",
        "PASSWORD": "tembatemba",
        "HOST": "postgres",
        "PORT": "5432",
        "ATOMIC_REQUESTS": True, # Recommandé
    }
}

# --- LA LIGNE QUI SAUVE TOUT ---
# On dit à RapidPro d'utiliser la même base pour la lecture et l'écriture
DATABASES["readonly"] = DATABASES["default"]

# =================================================
# 3. CONFIGURATION API (REST FRAMEWORK)
# =================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 250,
    # Gestionnaire d'erreurs
    'EXCEPTION_HANDLER': 'temba.api.support.temba_exception_handler',
    # Dates
    'DATE_INPUT_FORMATS': ['iso-8601', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d'],
    'DATETIME_INPUT_FORMATS': ['iso-8601', '%Y-%m-%dT%H:%M:%S.%fZ'],
    'DATE_FORMAT': 'iso-8601',
    'DATETIME_FORMAT': 'iso-8601',
}

# =================================================
# 4. GESTION DES COMPTES
# =================================================
ACCOUNT_ALLOW_REGISTRATION = False
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

# =================================================
# 5. DIVERS
# =================================================
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
SEND_EMAILS = False

COMPRESS_ENABLED = False 
COMPRESS_OFFLINE = False
STATIC_URL = "/static/"

MAILROOM_URL = os.environ.get("MAILROOM_URL", "http://localhost:8090")
MAILROOM_AUTH_TOKEN = os.environ.get("MAILROOM_AUTH_TOKEN")
HELP_URL = None

MIDDLEWARE = ("temba.middleware.ExceptionMiddleware",) + MIDDLEWARE
warnings.filterwarnings("error", r"DateTimeField .* received a naive datetime", RuntimeWarning, r"django\.db\.models\.fields")
