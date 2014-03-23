from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import HomeView, ExampleSecretView

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
