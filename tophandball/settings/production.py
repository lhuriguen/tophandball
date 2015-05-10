import os

from base import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'support@tophandball.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = 'support@tophandball.com'
SERVER_EMAIL = 'support@tophandball.com'

ALLOWED_HOSTS = [
    '.tophandball.com',  # Allow domain and subdomains
]

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

# Performance settings, need testing.
CONN_MAX_AGE = 60
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }

# Error reporting
ADMINS = (('Leti', 'admin@tophandball.com'),)
MANAGERS = ADMINS
