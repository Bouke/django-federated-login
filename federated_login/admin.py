from django.conf import settings
from django.contrib.admin import AdminSite
from django.shortcuts import redirect

from .utils import monkeypatch_method


def patch_admin():
    @monkeypatch_method(AdminSite)
    def login(self, request, extra_context=None):
        """
        Redirects to the site login for the given HttpRequest
        """
        return redirect(str(settings.LOGIN_URL))


def unpatch_admin():
    setattr(AdminSite, 'login', original_login)


original_login = AdminSite.login
if getattr(settings, 'FL_PATCH_ADMIN', True):
    patch_admin()
