from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User


def get_jwt_token(user: User) -> RefreshToken:
    return RefreshToken.for_user(user)
