from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CandidateProfile, EmployerProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CandidateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CandidateProfile
        fields = '__all__'

class EmployerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = EmployerProfile
        fields = '__all__'
