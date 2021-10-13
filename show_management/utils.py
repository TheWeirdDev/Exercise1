from .models import User

def is_mentor(user: User):
    return user.role == User.MENTOR

def is_admin(user: User):
    return user.role == User.ADMIN
