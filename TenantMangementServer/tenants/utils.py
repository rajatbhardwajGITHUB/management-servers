import jwt
import datetime
from django.conf import settings

def generate_jwt_token(user):
    """
    Generate an access token here
    :param user: User object
    """
    # add it in a try except block
    try:
        access_payload = {
            "id":user.id,
            "email":user.email,
            "exp":datetime.datetime.utcnow() + settings.JWT_EXPIRATION_TIME, #Expiration
            "iat":datetime.datetime.utcnow(), # issued at
            "token_type":"access"
        }
        access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        print("access",access_token)
        #access_token = "bearer " + access_token
        refresh_payload = {
            "id":user.id,
            "exp":datetime.datetime.utcnow() + settings.JWT_EXPIRATION_TIME,
            "iat":datetime.datetime.utcnow(),
            "token":"refresh"
        }
        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        print("refresh",refresh_token)
        #refresh_token = "bearer " + refresh_token
        return access_token, refresh_token
    except Exception as e:
        print("Error in generating token: ", e)
        return None, None


    
    