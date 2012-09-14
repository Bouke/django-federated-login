from openid.extensions import ax
from django.core.exceptions import ValidationError
from federated_login import UserClass, UserFactory

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
            raise ValidationError('Did not receive email from the provider')

        try:
            return UserClass.objects.get(email=email)
        except UserClass.DoesNotExist:
            pass

        if UserFactory:
            first_name = fetch_res.getSingle('http://axschema.org/namePerson/first')
            last_name = fetch_res.getSingle('http://axschema.org/namePerson/last')

            return create_user(email=email,
                               first_name=first_name,
                               last_name=last_name)

    def get_user(self, user_id):
        try:
            return UserClass.objects.get(pk=user_id)
        except UserClass.DoesNotExist:
            return None


def create_user(first_name, last_name, **kwargs):
    """
    Generates a username from the first and last name and returns the user
    created by called user factory.
    """
    username = '%s.%s' % (first_name[0].lower(), last_name.lower())
    suffix = 1
    while UserClass.objects.filter(username=username).count() > 0:
        username = '%s.%s.%s' % (first_name[0].lower(), last_name.lower(),
                                 suffix)
        suffix += 1
    return UserFactory(username=username, first_name=first_name,
                       last_name=last_name, **kwargs)
