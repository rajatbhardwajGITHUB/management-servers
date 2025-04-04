import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from tenants.TenantSerializer import TenantSerializer
from tenants.models import User
import tenants.utils
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from tenants.FDAWs.UserFdaws import get_user_details_for_dashboard


class TenantCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = TenantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id=None):
        print("** Captured get request **  ",request.query_params)
        if id:
            tenants = User.objects.get(id=id)
            serialized = TenantSerializer(tenants)
            if serialized:
                return Response({"data":serialized.data, "messsage":"success"})
        tenants = User.objects.all()
        serialized = TenantSerializer(tenants, many=True)
        if serialized:
            return Response({"data":serialized.data, "message":"success"})
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email= data.get("email")
            password = data.get("password") #hashed password
            print(email,password)

            try:
                user = User.objects.get(email=email)
                print(user)
            except User.DoesNotExist:
                return JsonResponse({"error":"Invalid credentials"}, status=400)
            
            if check_password(password, user.password):
                access_token, refresh_token = tenants.utils.generate_jwt_token(user) 
                #add the token to the user in db
                print("Access Token: ", access_token)
                print("Refresh Token: ", refresh_token)
                User.objects.filter(email=email).update(access_token=access_token)
                User.objects.filter(email=email).update(refresh_token=refresh_token)
                return JsonResponse({"access_token":access_token, "refresh_token":refresh_token}, status=200)
            else:
                return JsonResponse({"error":"Invalid credentials"}, status=400)
        except Exception as e:
            return JsonResponse({"error":str(e)},status=500)

class DashboardView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self, request):
        # get all the neccessary fields form the user model
        # and return it to front end

        user_detail_list = get_user_details_for_dashboard(request);
        print(user_detail_list)
        return JsonResponse({"data":user_detail_list}, status=200)