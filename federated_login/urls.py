from django.conf.urls.defaults import patterns, url
from django.conf import settings

urlpatterns = patterns('federated_login.views',
    url(r'^%s$' % settings.LOGIN_URL.lstrip('/'), 'login', name='fl_login'),
    url(r'^identity/$', 'identity', name='fl_identity')
)
