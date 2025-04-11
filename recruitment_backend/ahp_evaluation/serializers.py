from rest_framework import serializers 
from .models import GenericCandidateForm 

class GenericCandidateFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericCandidateForm 
        fields = '__all__'


class AHPComputeOutputSerializer(serializers.Serializer):
    """
    Pour chaque candidat :
    {
      "candidate_id": 1,
      "weights": [w1, w2, ...],
      "consistency_ratio": 0.07
    }
    """
    candidate_id = serializers.IntegerField()
    weights = serializers.ListField(child=serializers.FloatField())
    consistency_ratio = serializers.FloatField()


class AHPComputeInputSerializer(serializers.Serializer):
    """
    Serializer pour la requête POST à /ahp/compute/
    {
      "matrix": [[...], [...], ...],
      "candidate_ids": [1, 2, 3, ...]
    }
    """
    matrix = serializers.ListField(
        child=serializers.ListField(
            child=serializers.FloatField(),
            allow_empty=False
        ),
        allow_empty=False
    )
    candidate_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )