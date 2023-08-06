import os
from functools import wraps


def restore_cwd(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        original_cwd = os.getcwd()
        try:
            return func(*args, **kwargs)
        finally:
            os.chdir(original_cwd)

    return wrapper


def admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        confirm_admin = os.getenv("CQ23CLI_ADMIN_CONFIRMATION", None)
        if not confirm_admin:
            print("Only admins are supposed to use this command.")
        else:
            return func(*args, **kwargs)

    return wrapper
