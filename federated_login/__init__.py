from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

__all__ = ['FL_SSO_ENDPOINT', 'auth_backends', 'urls', 'views', 'UserClass',
           'UserFactory', 'user_factories']

# Determine endpoint for authenticating against
if hasattr(settings, 'FL_SSO_ENDPOINT'):
    FL_SSO_ENDPOINT = getattr(settings, 'FL_SSO_ENDPOINT')
elif hasattr(settings, 'FL_APPS_DOMAIN'):
    FL_SSO_ENDPOINT = ''.join(['https://www.google.com/accounts/o8/site-xrds?hd=',
                               getattr(settings, 'FL_APPS_DOMAIN')])
else:
    raise ImproperlyConfigured('FL_SSO_ENDPOINT or FL_APPS_DOMAIN not set')

def get_class(name):
    if name:
        module, func_name = name.rsplit('.', 1)
        module = __import__(module, fromlist=[module])
        return getattr(module, func_name)

UserClass = get_class(getattr(settings, 'FL_USER_CLASS',
    'django.contrib.auth.models.User'))

UserFactory = get_class(getattr(settings, 'FL_USER_FACTORY',
    'federated_login.user_factories.normal'))
