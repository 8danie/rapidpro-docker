# Ce fichier écrase la configuration de settings_common.py
from django.core.mail.backends.console import EmailBackend

# On force le backend "Console" (affiche les emails dans les logs Docker)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# On met des valeurs bidons pour être sûr qu'il ne tente pas de joindre Gmail
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False

# On désactive l'envoi réel par sécurité
SEND_EMAILS = False
