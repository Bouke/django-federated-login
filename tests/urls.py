from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^federated/', include('federated_login.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
