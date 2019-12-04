from functools import wraps

from flask import redirect, url_for
from flask_login import current_user


def general_manager_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        """部長・管理者権限判定"""
        if current_user.role == 2 or current_user.role == 3:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('home.index'))
    return inner

def admin_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        """管理者権限判定"""
        if current_user.role == 3:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('home.index'))
    return inner