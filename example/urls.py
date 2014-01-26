from django.conf.urls import patterns, include, url

from django.contrib import admin
from example.views import HomeView, ExampleSecretView
import federated_login

from federated_login import patch_admin

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(
        regex=r'^$',
        view=HomeView.as_view(),
        name='home',
    ),
    url(
        regex=r'^account/logout/$',
        view='django.contrib.auth.views.logout',
        name='logout',
    ),
    url(
        regex=r'^secret/$',
        view=ExampleSecretView.as_view(),
        name='secret',
    ),
    url(r'^federated/', include('federated_login.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
