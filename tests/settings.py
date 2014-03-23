from django.core.urlresolvers import reverse_lazy
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = (
    'federated_login.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SECRET_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'tests.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'federated_login',
    'tests',
)


LOGIN_URL = reverse_lazy('fl_login')
LOGIN_REDIRECT_URL = '/'

FL_APPS_DOMAIN = 'webatoom.nl'
FL_PATCH_ADMIN = False

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
