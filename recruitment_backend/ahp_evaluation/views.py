from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CandidateForm
from .serializers import CandidateFormSerializer

class CandidateFormViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Lister tous les critères du candidat connecté.
        """
        queryset = CandidateForm.objects.filter(user=request.user)
        serializer = CandidateFormSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Créer plusieurs critères pour le candidat connecté.
        """
        data = request.data

        if not isinstance(data, list):
            return Response(
                {"error": "Les données doivent être une liste de critères."},
                status=status.HTTP_400_BAD_REQUEST
            )

        created_items = []
        for item in data:
            serializer = CandidateFormSerializer(data=item, context={'request': request})
            if serializer.is_valid():
                serializer.save()  # user est automatiquement attribué via le sérialiseur
                created_items.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_items, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """
        Supprimer un critère spécifique.
        """
        try:
            candidate_form = CandidateForm.objects.get(pk=pk, user=request.user)
            candidate_form.delete()
            return Response({"success": "Critère supprimé."}, status=status.HTTP_204_NO_CONTENT)
        except CandidateForm.DoesNotExist:
            return Response({"error": "Critère introuvable."}, status=status.HTTP_404_NOT_FOUND)
