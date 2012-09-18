from federated_login import UserClass

def __create(**kwargs):
    user = UserClass(**kwargs)
    user.set_unusable_password()
    user.save()
    return user

def normal(**kwargs):
    """
    Creates a normal user
    """
    return __create(**kwargs)

def staff(**kwargs):
    """
    Creates a staff user
    """
    kwargs['is_staff'] = True
    return __create(**kwargs)

def superuser(**kwargs):
    """
    Creates a superuser
    """
    kwargs['is_staff'] = True
    kwargs['is_superuser'] = True
    return __create(**kwargs)
