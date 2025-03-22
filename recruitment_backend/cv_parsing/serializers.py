from rest_framework import serializers
from .models import CVParsedData

class CVParsedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVParsedData
        fields = ['name', 'email', 'phone', 'skills', 'experience', 'education']