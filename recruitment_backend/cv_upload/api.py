from rest_framework import serializers, viewsets
from .models import CVUpload

class CVUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVUpload
        fields = '__all__'

class CVUploadViewSet(viewsets.ModelViewSet):
    queryset = CVUpload.objects.all()
    serializer_class = CVUploadSerializer