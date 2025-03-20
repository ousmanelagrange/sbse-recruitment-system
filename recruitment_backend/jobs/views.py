from rest_framework import viewsets, status 
from rest_framework.permissions import IsAuthenticated, AllowAny 
from rest_framework.response import Response 
from rest_framework.decorators import action 
from rest_framework import serializers
from .models import Job, Constraint, SkillRequirement, CandidateApplication 
from .serializers import JobSerializer, ConstraintSerializer, SkillRequirementSerializer, CandidateApplicationSerializer
from .ahp import calculate_candidate_score


# Gestion des annonces par l'employer
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer 
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        # ✅ Retourner toutes les offres sans filtrage par défaut
        return Job.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        user = self.request.user
        
        # ✅ Vérifier si l'utilisateur a un profil employeur
        if not hasattr(user, 'employer_profile'):
            raise serializers.ValidationError({'detail': 'L\'utilisateur n\'a pas de profil employeur associé.'})
        
        # ✅ Créer le job
        job = serializer.save(employer=user.employer_profile)
        print(f"Job créé : {job}")
        
        # ✅ Ajouter les contraintes et compétences manuellement
        constraints_data = self.request.data.get('constraints', [])
        skills_data = self.request.data.get('skill_requirements', [])
        
        for constraint_data in constraints_data:
            Constraint.objects.create(job=job, **constraint_data)
        
        for skill_data in skills_data:
            SkillRequirement.objects.create(job=job, **skill_data)
    
    def update(self, request, *args, **kwargs):
        """
        Mise à jour d'une offre d'emploi avec suppression des anciennes contraintes et compétences
        """
        instance = self.get_object()
        
        # Suppression des anciennes contraintes et compétences avant mise à jour
        instance.constraints.all().delete()
        instance.skill_requirements.all().delete()
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Ajouter les nouvelles contraintes et compétences
        constraints_data = request.data.get('constraints', [])
        skills_data = request.data.get('skill_requirements', [])
        
        for constraint_data in constraints_data:
            Constraint.objects.create(job=instance, **constraint_data)
        
        for skill_data in skills_data:
            SkillRequirement.objects.create(job=instance, **skill_data)
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Suppression d'une offre d'emploi
        """
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def constraints(self, request, pk=None):
        """Récupérer les contraintes associées à une offre d'emploi"""
        job = self.get_object()
        constraints = Constraint.objects.filter(job=job)
        serializer = ConstraintSerializer(constraints, many=True)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def skill_requirements(self, request, pk=None):
        """Récupérer les compétences requises associées à une offre d'emploi"""
        job = self.get_object()
        skills = SkillRequirement.objects.filter(job=job)
        serializer = SkillRequirementSerializer(skills, many=True)
        return Response(serializer.data)



# Candidation à une offre par l'utilisateur
class CandateApplicationViewSet(viewsets.ModelViewSet):
    queryset = CandidateApplication.objects.all()
    serializer_class = CandidateApplicationSerializer
    permission_classes = [AllowAny]
    # Soumission d'une nouvelle candidature
    def create(self, request, *args, **kwargs):
        job_id = request.data.get('job')
        candidate = request.user.candidate_profile 
        
        try:
            job = Job.objects.get(id=job_id, status='open')
        except Job.DoesNotExist:
            return Response({"details": "Offre d'emploi non fermée."}, status=status.HTTP_404_NOT_FOUND)
        
        # Verifier si le candidat a déjà ce job
        if CandidateApplication.objects.filter(candidate=candidate, job=job).exists():
            return Response({"detail": "Vous avez déjà postulé à cette offre."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calcul du score avec AHP 
        score = calculate_candidate_score(candidate, job)
        
        # Créer la candidature
        application = CandidateApplication.objects.create(
            candidate=candidate,
            job=job,
            score=score
        )
        
        # Mettre à jour le classement après l'ajout de la nouvelle candidature 
        self.update_rankings(job)
        
        serializer = self.get_serializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])    
    def my_applications(self, request):
        """
        Lister les candidature du candidat connecté
        """
        candidate = request.user.candidate_profile
        applications = CandidateApplication.objects.filter(candidate=candidate)
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def list_for_job(self, request, pk=None):
        """
        Lister toutes les candidatures pour une offre spécifique
        """
        job = self.get_object()
        applications = CandidateApplication.objects.filter(job=job).order_by('-score')
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)
    
    
    def update_rankings(self, job):
        """Mise à jour du classement des candidatures après une nouvelle soumission"""
        applications = CandidateApplication.objects.filter(job=job).order_by('-score')
        for rank, application in enumerate(applications, start=1):
            application.rank = rank
            application.save()   