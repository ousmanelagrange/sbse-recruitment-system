from rest_framework import serializers 
from .models import GenericCandidateForm 

class GenericCandidateFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericCandidateForm 
        fields = '__all__'
