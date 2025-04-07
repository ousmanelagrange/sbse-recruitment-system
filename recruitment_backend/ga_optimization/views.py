from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CandidateApplication
from .genetic_algorithm import GeneticAlgorithm

class GAOptimizationView(APIView):
    """
    Vue API pour appliquer l'optimisation des candidatures via l'algorithme génétique.
    """
    def post(self, request, job_id):
        # Récupère toutes les candidatures pour un job donné
        applications = CandidateApplication.objects.filter(job_id=job_id, status='pending')
        
        if not applications:
            return Response({"detail": "Aucune candidature en attente pour ce poste."}, status=status.HTTP_404_NOT_FOUND)
        
        # Exécute l'algorithme génétique pour optimiser les candidatures
        ga = GeneticAlgorithm(applications)
        ga.run()

        # Retourne les candidatures optimisées avec leur score AG mis à jour
        optimized_applications = [
            {
                "candidate": app.candidate.user.username,
                "score_ahp": app.score_ahp,
                "score_ga": app.score_ga,
                "rank": app.rank,
                "status": app.status,
            }
            for app in applications
        ]

        return Response(optimized_applications, status=status.HTTP_200_OK)


from .genetic_algorithm import GeneticAlgorithm
from rest_framework import status

class OptimizeApplicationsView(APIView):
    def post(self, request, job_id):
        applications = CandidateApplication.objects.filter(job_id=job_id, status='pending')
        if not applications:
            return Response({"detail": "Aucune candidature en attente."}, status=status.HTTP_404_NOT_FOUND)

        ga = GeneticAlgorithm(applications)
        ga.run()

        return Response({"detail": "Optimisation effectuée."}, status=status.HTTP_200_OK)

class GetOptimizedApplicationsView(APIView):
    def get(self, request, job_id):
        applications = CandidateApplication.objects.filter(job_id=job_id)
        serializer = CandidateApplicationSerializer(applications, many=True)
        return Response(serializer.data)
