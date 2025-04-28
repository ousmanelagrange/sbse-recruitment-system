from rest_framework import serializers
from .models import CandidateForm

class CandidateFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateForm
        fields = ['user', 'name', 'value', 'weight', 'created_at']
        read_only_fields = ['created_at', 'user']

    def create(self, validated_data):
        # Ajoute l'utilisateur extrait du contexte (request.user) avant de sauvegarder
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
