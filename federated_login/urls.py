from django.conf.urls import patterns, url
from federated_login.views import identity, login

urlpatterns = patterns(
    '',
    url(r'^login/$', login, name='fl_login'),
    url(r'^identity/$', identity, name='fl_identity')
)
