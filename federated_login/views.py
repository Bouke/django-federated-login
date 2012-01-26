import urllib

from django.conf import settings
from django.contrib import messages, auth
from django.core.exceptions import MultipleObjectsReturned, ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from openid.consumer.consumer import Consumer, SUCCESS, FAILURE, CANCEL
from openid.extensions import ax
from openid.store.memstore import MemoryStore

from federated_login import FL_SSO_ENDPOINT

__all__ = ['login', 'identity']

def create_consumer(request):
    """
    Returns an OpenID Consumer.

    As there is only one identity server, the current transactions can safely
    be stored in memory.
    """
    return Consumer(request.session.setdefault('openid', {}),
                    MemoryStore())

def login(request, **kwargs):
    """
    Redirect the user to the SSO server for authentication.
    """
    auth_req = create_consumer(request).begin(FL_SSO_ENDPOINT)

    # Google will only return required fields, so require all
    # user details we would like to receive.
    fetch_req = ax.FetchRequest()
    fetch_req.add(ax.AttrInfo('http://axschema.org/contact/email',
                              'email', required=True))
    fetch_req.add(ax.AttrInfo('http://axschema.org/namePerson/first',
                              'firstname', required=True))
    fetch_req.add(ax.AttrInfo('http://axschema.org/namePerson/last',
                              'lastname', required=True))
    auth_req.addExtension(fetch_req)

    # Build the url where the user should be returned when authenticated
    # at the SSO server. Append the future redirect to which the user
    # should be redirected after successful local authentication.
    realm = request.build_absolute_uri('/')
    return_to = request.build_absolute_uri(reverse(identity))
    future_redirect = request.GET.get(auth.REDIRECT_FIELD_NAME, '')
    if future_redirect != '':
        future_redirect = urllib.urlencode({
            auth.REDIRECT_FIELD_NAME: future_redirect})
        return_to = u'%s?%s' % (return_to, future_redirect)

    return HttpResponseRedirect(auth_req.redirectURL(realm, return_to))

@csrf_exempt
def identity(request, **kwargs):
    """
    Processes the OpenID response and tries to authenticate the inbound user.

    It uses Django's messaging framework to feed error messages to the user, in
    case of failures of cancellations.
    """
    current_url = request.build_absolute_uri()
    auth_res = create_consumer(request).complete(dict(request.REQUEST),
                                                 current_url)

    if auth_res.status == SUCCESS:
        try:
            user = auth.authenticate(openid_response=auth_res)
            if user and user.is_active:
                auth.login(request, user)

                # Determine where the user wanted to go, or fallback to a
                # pre-defined url.
                redirect_to = request.REQUEST.get(auth.REDIRECT_FIELD_NAME,
                                                  settings.LOGIN_REDIRECT_URL)
                return HttpResponseRedirect(redirect_to)
            elif user:
                messages.error(request, 'User account is not active', fail_silently=True)
            else:
                messages.error(request, 'No user record found', fail_silently=True)
        except MultipleObjectsReturned:
            messages.error(request, 'Multiple user records found', fail_silently=True)
        except ValidationError, err:
            messages.error(request, ', '.join(err.messages), fail_silently=True)
    elif auth_res.status == FAILURE:
        messages.error(request, 'Authentication failed: %s' % auth_res.message, fail_silently=True)
    elif auth_res.status == CANCEL:
        messages.error(request, 'Authentication canceled', fail_silently=True)
    else:
        raise Exception, 'Unknown OpenID result: %s' % auth_res.status

    # There was some exception, return the user to the default login page
    return HttpResponseRedirect(settings.LOGIN_URL)
