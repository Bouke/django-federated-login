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

Add ``'federated_login'`` to your list of installed apps:
::

    settings.py:
    INSTALLED_APPS = (
        ...
        'federated_login',
    )

Add ``'federated_login.auth.backend.EmailBackend'`` as authentication backend:
::

    settings.py:
    AUTHENTICATION_BACKENDS = (
        'federated_login.auth.backends.EmailBackend',
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
button to this url on the regular login page.

Extra settings
==============

These are the customizable settings:

``FL_APPS_DOMAIN``
    Google Apps domain to identify against.

``FL_CREATE_USERS`` (Default: ``False``)
    Whether to create a user account when unknown e-mail address is presented.

``FL_USER_FACTORY`` (Default: ``'aba.utils.fl_user_factory'``)
    Function that is called when creating a user account.

``FL_SSO_ENDPOINT`` (Default: Google Apps)
    Override this setting to link with another OpenID identity provider.

Notes
=====

This package depends on a fork of ``python-openid`` as the current upstream
version (2.2.5) does not play well with a Google extension used by Google
Apps identity provider.

