from rest_framework import serializers
from jobs.models import CandidateApplication

class CandidateApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateApplication
        fields = ['candidate', 'score_ahp', 'score_ga', 'rank', 'status']
