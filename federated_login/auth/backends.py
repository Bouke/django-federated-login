from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from openid.extensions import ax
from federated_login import FL_CREATE_USERS, FL_USER_FACTORY

__all__ = ['EmailBackend']

class EmailBackend(object):
    """
    Authenticate users based on a remotely verified e-mail address.

    Combined with SSO and white listed domain names, only a subset of the
    remote users will be allowed to login. Optionally it can create a new
    user if the e-mail address is verified but not listed.
    """
    def authenticate(self, openid_response, **kwargs):
        try:
            fetch_res = ax.FetchResponse.fromSuccessResponse(openid_response)
            email = fetch_res.getSingle('http://axschema.org/contact/email')
        except AttributeError:
            raise ValidationError, 'Did not receive email from the provider'

        try:
            return User.objects.get(email=email)
        except User.DoesNotExist, err:
            if not FL_CREATE_USERS:
                raise err

        return create_user(email=email,
                           first_name=fetch_res.getSingle('http://axschema.org/namePerson/first'),
                           last_name=fetch_res.getSingle('http://axschema.org/namePerson/last'))

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def create_user(first_name, last_name, **kwargs):
    """
    Generates a username from the first and last name and returns the user
    created by called user factory.
    """
    username = '%s.%s' % (first_name[0].lower(), last_name.lower())
    suffix = 1
    while User.objects.filter(username=username).count() > 0:
        username = '%s.%s.%s' % (first_name[0].lower(), last_name.lower(),
                                 suffix)
        suffix += 1

    module, func_name = FL_USER_FACTORY.rsplit('.', 1)
    module = __import__(module, fromlist=[module])
    return getattr(module, func_name)(username=username, first_name=first_name,
                                      last_name=last_name, **kwargs)
