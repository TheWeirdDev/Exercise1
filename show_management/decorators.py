from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from .models import User

def mentor_or_admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    decorator = user_passes_test(
        lambda u: u.role == User.MENTOR or u.role == User.ADMIN,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return decorator(function)
    return decorator
