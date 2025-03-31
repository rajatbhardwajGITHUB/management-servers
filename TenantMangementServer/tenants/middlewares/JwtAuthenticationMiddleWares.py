

from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from tenants.models import User
import jwt

class JWTAuthenticationMiddleware(MiddlewareMixin):
    
    def process_request(self, request):

        excluded_paths = ['/tenants/','/tenants/login/']
        current_path = request.path_info

        if current_path in excluded_paths:
            return None
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"error":"Authorization Header Missing or Invalid"}, status=401)
        
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user = User.objects.get(id=payload["id"])
            request.user = user
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error":"Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error":"Invalid token"}, status=401)
        except user.DoesNotExist:
            return JsonResponse({"error":"User not found"}, status=401)
        except Exception as e:
            return JsonResponse({"error":str(e)}, status=500)
    

        