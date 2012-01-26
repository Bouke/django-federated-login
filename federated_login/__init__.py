from django.conf import settings

__all__ = ['FL_APPS_DOMAIN', 'FL_SSO_ENDPOINT', 'FL_CREATE_USERS',
           'FL_USER_FACTORY', 'auth', 'urls', 'views']

# The Google Apps account through which you want to establish single sign-on.
FL_APPS_DOMAIN = getattr(settings, 'FL_APPS_DOMAIN', 'webatoom.nl')

default_endpoint = ''.join(['https://www.google.com/accounts/o8/site-xrds?hd=',
                            FL_APPS_DOMAIN])
# The endpoint
FL_SSO_ENDPOINT = getattr(settings, 'FL_SSO_ENDPOINT', default_endpoint)

# Whether new user accounts should be created for unknown logins. Optionally
# set FL_USER_FACTORY to modify the users being created.
FL_CREATE_USERS = getattr(settings, 'FL_CREATE_USERS', False)

# If FL_CREATE_USERS set to True, provide a user factory to override the
# default behaviour when creating new user accounts.
# @todo look if signals can provide the same flexibility
FL_USER_FACTORY = getattr(settings, 'FL_USER_FACTORY',
                          'federated_login.auth.user_factory')
