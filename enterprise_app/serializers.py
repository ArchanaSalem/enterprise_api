from rest_framework import serializers
from .models import Enterprise

class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ['id', 'name', 'location', 'industry', 'is_active']
