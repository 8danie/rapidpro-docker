# force_console_email.py
from django.core.mail.backends.console import EmailBackend

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
SEND_EMAILS = False
