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
    # 'localhost',
]

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_HTTPONLY = True
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

# AWS settings
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_EXPIRE = 60 * 60 * 24 * 7
AWS_S3_HOST = 's3.eu-central-1.amazonaws.com'

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
AWS_HEADERS = {
    'Cache-Control': str.encode(
        'max-age=%d, s-maxage=%d, must-revalidate' % (
            AWS_QUERYSTRING_EXPIRE, AWS_QUERYSTRING_EXPIRE))
}

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s.%s/%s/" % (
    AWS_S3_HOST, AWS_STORAGE_BUCKET_NAME, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'utils.custom_storages.MediaStorage'
