from federated_login import UserClass

def normal(**kwargs):
    """
    Returns a new user with the given arguments.
    """
    return UserClass.objects.create(**kwargs)

def superuser(**kwargs):
    """
    Returns a new user with the given arguments.
    """
    kwargs['is_superuser'] = True
    return UserClass.objects.create(**kwargs)
