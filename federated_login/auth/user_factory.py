# -*- coding: utf-8 -*-
from federated_login import FL_USER_CLASS

module, func_name = FL_USER_CLASS.rsplit('.', 1)
module = __import__(module, fromlist=[module])
UserClass = getattr(module, func_name)


def user_factory(**kwargs):
    """
    Returns a new user with the given arguments.
    """
    return UserClass.objects.create(**kwargs)
