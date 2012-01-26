from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('federated_login.views',
    url(r'^sign-in/$', 'login', name='fl_login'),
    url(r'^identity/$', 'identity', name='fl_identity')
)
