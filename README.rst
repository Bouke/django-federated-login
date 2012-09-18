======================
Django Federated Login
======================

Django Federated Login provides an authentication bridge between Django
projects and OpenID-enabled identity providers. The bridge is pre-wired to be
used with a single Google Apps domain, but could be extended to be linked with
other OpenID providers also. It is different from other OpenID consumers as
this consumer only allows connecting to a pre-defined identity provider.

The provided backend matches users based on the e-mail address returned from
the identity provider. If no matching user could be found, a user account can
optionally be created.

Installation
============

Installation with ``pip``:
::

    $ pip install django-federated-login

Add ``'federated_login.auth_backend.EmailBackend'`` as authentication backend:
::

    settings.py:
    AUTHENTICATION_BACKENDS = (
        'federated_login.auth_backends.EmailBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

Provide the Google Apps domain to identify against:
::

    settings.py:
    FL_APPS_DOMAIN = 'webatoom.nl'

Register the views:
::

    urls.py:
    url(r'^federated/', include('federated_login.urls')),

Usage
=====

Point your browser to ``/federated/login/``. You might want to include a
button to this url on the regular login page. You could also use the federated
login page as the default login page, replacing the username and password login
pages. To do this, configure the ``LOGIN_`` settings:
::

    settings.py:
    LOGIN_REDIRECT_URL = '/'
    LOGIN_URL = '/federated/login/'

    urls.py:
    from federated_login import patch_admin

Settings
========

These are the customizable settings:

``FL_APPS_DOMAIN``
    Google Apps domain to identify against. Can be overriden by
    ``FL_SSO_ENDPOINT``.

``FL_USER_FACTORY`` (Default: ``'federated_login.user_factories.normal'``)
    Function that is called when creating a user account. Set to `None` to
    disable creation of new users. There is also
    ``'federated_login.user_factories.staff'`` that creates staff users and
    ``'federated_login.user_factories.superuser'`` that creates superusers.

``FL_SSO_ENDPOINT`` (Default: Google Apps)
    Override this setting to link with another OpenID identity provider. The
    ``FL_APPS_DOMAIN`` setting will have no effect when providing a custom
    ``FL_SSO_ENDPOINT``.

``FL_USER_CLASS`` (Default: ``'django.contrib.auth.models.User'``)
    Django model class to used to create and query for users.
