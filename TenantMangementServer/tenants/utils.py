import jwt
import datetime
from django.conf import settings

def generate_jwt_token(user):
    """
    Generate an access token here
    """

    access_payload = {
        "id":user.id,
        "email":user.email,
        "exp":datetime.datetime.utcnow() + settings.JWT_EXPIRATION_TIME, #Expiration
        "iat":datetime.datetime.utcnow(), # issued at
        "token_type":"access"
    }
    access_token = jwt.encode(access_payload, settings.SECRET_KEYS, algorithm=settings.JWT_ALGORITHM)

    refresh_payload = {
        "id":user.id,
        "exp":datetime.datetime.utcnow() + settings.JWT_EXPIRATION_TIME,
        "iat":datetime.datetime.utcnow(),
        "token":"refresh"
    }
    refresh_token = jwt.encode(refresh_token, settings.SECRET_KEYS, algorithm=settings.JWT_ALGORITHM)

    return access_token, refresh_token