from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from tenants.TenantSerializer import TenantSerializer
from tenants.models import User

class TenantCreateView(APIView):
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
    
    