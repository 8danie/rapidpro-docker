# --- FORCE LA BASE DE DONNEES VERS LE CONTENEUR ---
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'temba',
        'USER': 'temba',
        'PASSWORD': 'tembatemba',
        'HOST': 'postgres', # ICI : On force le nom du conteneur
        'PORT': '5432',
        'CONN_MAX_AGE': 60,
        'ATOMIC_REQUESTS': True,
    }
}

# --- FORCE L'EMAIL EN MODE CONSOLE (Pas de Gmail) ---
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'server@rapidpro.local'
