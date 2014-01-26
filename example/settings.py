from django.core.urlresolvers import reverse_lazy
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_PATH, 'database.sqlite'),
    }
}

STATIC_URL = '/static/'

AUTHENTICATION_BACKENDS = (
    'federated_login.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TIME_ZONE = 'Europe/Amsterdam'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'DO NOT USE THIS KEY!'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'example.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'federated_login',

    'debug_toolbar',
)


LOGIN_URL = reverse_lazy('fl_login')
LOGIN_REDIRECT_URL = '/'

FL_APPS_DOMAIN = 'webatoom.nl'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

try:
    from .settings_private import *  # noqa
except ImportError:
    pass
