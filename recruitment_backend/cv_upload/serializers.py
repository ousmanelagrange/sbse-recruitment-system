from rest_framework import serializers
from .models import CVUpload

class CVUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVUpload
        fields = ['name', 'email', 'cv_file']