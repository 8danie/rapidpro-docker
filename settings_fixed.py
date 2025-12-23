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
# 2. BASE DE DONNÉES
# =================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "temba",
        "USER": "temba",
        "PASSWORD": "tembatemba",
        "HOST": "postgres",
        "PORT": "5432",
    }
}

# =================================================
# 3. GESTION DES COMPTES (SANS INSCRIPTION)
# =================================================
# --- C'EST ICI QUE VOUS DÉSACTIVEZ L'INSCRIPTION ---
# Cela supprime le formulaire d'inscription pour le public.
# Seuls les admins peuvent créer des comptes.
ACCOUNT_ALLOW_REGISTRATION = False

# --- NE SUPPRIMEZ PAS CES LIGNES ---
# Elles sont nécessaires pour que Django démarre sans erreur,
# même si l'inscription est désactivée.
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_EMAIL_VERIFICATION = "none"

# Connexion/Déconnexion
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_ON_GET = True

# =================================================
# 4. TÂCHES CELERY (CORRECTIF DEADLOCK)
# =================================================
# IMPORTANT : On passe à False pour éviter le blocage au démarrage (DeadlockError)
# Les tâches passeront par Redis au lieu de bloquer le thread principal.
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = False

# =================================================
# 5. EMAILS & FICHIERS
# =================================================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
SEND_EMAILS = False

COMPRESS_ENABLED = False 
COMPRESS_OFFLINE = False
STATIC_URL = "/static/"

# =================================================
# 6. DIVERS
# =================================================
MAILROOM_URL = os.environ.get("MAILROOM_URL", "http://localhost:8090")
MAILROOM_AUTH_TOKEN = os.environ.get("MAILROOM_AUTH_TOKEN")

MIDDLEWARE = ("temba.middleware.ExceptionMiddleware",) + MIDDLEWARE
warnings.filterwarnings("error", r"DateTimeField .* received a naive datetime", RuntimeWarning, r"django\.db\.models\.fields")
