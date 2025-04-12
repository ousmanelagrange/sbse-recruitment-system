import numpy as np
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from drf_spectacular.utils import extend_schema


from .Ahp_module.Ahp import AHP
from .models import GenericCandidateForm
from .serializers import GenericCandidateFormSerializer, AHPComputeInputSerializer, AHPComputeOutputSerializer
from users.models import CandidateProfile


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


class GenericCandidateFormViewSet(viewsets.ModelViewSet):
    queryset = GenericCandidateForm.objects.all()
    serializer_class = GenericCandidateFormSerializer

    def get_queryset(self):
        return self.queryset.filter(candidate=self.request.user.candidateprofile)


class AHPComputeAPIView(GenericViewSet):
    """
    Calcul AHP et classement des candidats
    """

    @swagger_auto_schema(
        request_body=AHPComputeInputSerializer,
        # responses=AHPComputeOutputSerializer(many=True),
        tags=["AHP"]
    )
    @extend_schema(
        # request=AHPComputeInputSerializer,
        responses=AHPComputeOutputSerializer(many=True),
        # tags=["AHP"]
    )
    @action(detail=False, methods=["post"])
    def compute_ahp(self, request):
        # 1. Valide le payload d’entrée
        in_ser = AHPComputeInputSerializer(data=request.data)
        in_ser.is_valid(raise_exception=True)

        try:
            matrix = np.array(in_ser.validated_data['matrix'], dtype=float)
            cand_ids = in_ser.validated_data['candidate_ids']

            # 2. Récupère et trie les formulaires
            forms = list(GenericCandidateForm.objects.filter(id__in=cand_ids))
            forms.sort(key=lambda f: cand_ids.index(f.id))

            # 3. Construire la matrice des scores des candidats
            candidates = np.array([
                [
                    f.communication_skills or 0,
                    f.adaptability_skills or 0,
                ]
                for f in forms
            ], dtype=float)

        except (KeyError, ValueError):
            return Response({"detail": "Payload invalide"}, status=status.HTTP_400_BAD_REQUEST)

        # 4. Calcul AHP
        ahp = AHP(matrix).run()
        weights = ahp.criterial_weights.tolist()
        scores = (candidates * ahp.criterial_weights).sum(axis=1)

        # 5. Associer chaque score à son candidat
        candidate_results = [
            {
                "candidate_id": f.id,
                "full_name": f.full_name,
                "score": round(zscore, 4),
                "weights": weights,
                "consistency_ratio": round(ahp.consistency_ratio, 4)
            }
            for f, score in zip(forms, scores)
        ]

        # 6. Trier les candidats du meilleur au moins bon
        ranked = sorted(candidate_results, key=lambda x: x["score"], reverse=True)

        return Response(ranked, status=status.HTTP_200_OK)

