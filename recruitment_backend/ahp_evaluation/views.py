from rest_framework import status
from rest_framework.views import APIView
from .models import GenericCandidateForm 
from .serializers import GenericCandidateFormSerializer
from users.models import CandidateProfile
from rest_framework.response import Response

class GenericCandateForm(APIView):
    def get(self, request, *args, **kwargs):
        # Récupérer les données générique du candidat
        
        try:
            candidate_profile = CandidateProfile.objects.get(user=request.user)
            form_data = GenericCandidateForm.objects.filter(candidate_profile).first()
            
            # Si le formulaire n'existe pas encore, on le cré (première fois)
            if not form_data:
                form_data = GenericCandateForm.objects.creaet(candidate=candidate_profile)
            return Response(GenericCandidateFormSerializer(form_data))
        except CandidateProfile.DoesNotExist:
            return Response({"message": "Candidate profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, *args, **kwargs):
        # Soumettre les informations génériques pour le candidat
        candidate_profile = CandidateProfile.objects.get(user=request.user)
        serializer = GenericCandidateFormSerializer(data=request.data)
        
        if serializer.is_valid():
            form_data = serializer.save(candidate=candidate_profile)
            return Response(GenericCandidateFormSerializer(form_data).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)