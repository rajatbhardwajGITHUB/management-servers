from rest_framework import serializers
from .models import User

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' # Serailize all model fields