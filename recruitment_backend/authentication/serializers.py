from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from users.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError('Email and password are required.')

        # Vérification des identifiants
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials.')

        # Vérification si le compte est actif
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        # On assigne l'utilisateur à `self.user` pour que le parent puisse l'utiliser
        attrs['user'] = user

        # ⚠️ Important : On retourne la méthode `validate` du parent pour la génération du token
        return super().validate(attrs)
