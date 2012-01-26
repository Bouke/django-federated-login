from django.contrib.auth.models import User

def user_factory(**kwargs):
    """
    Returns a new user with the given arguments.
    """
    return User.objects.create(**kwargs)
