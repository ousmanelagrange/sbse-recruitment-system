from rest_framework import viewsets, status 
from rest_framework.permissions import IsAuthenticated, AllowAny 
from rest_framework.response import Response 
from rest_framework.decorators import action 
from rest_framework import serializers
from .models import Job, Constraint, SkillRequirement, CandidateApplication 
from .serializers import JobSerializer, ConstraintSerializer, SkillRequirementSerializer, CandidateApplicationSerializer
from .ahp import calculate_candidate_score
from users.permissions import IsEmployer, IsCandidate
from users.models import CandidateProfile, EmployerProfile, User
from django.shortcuts import get_object_or_404

# Gestion des annonces par l'employer
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer 
    permission_classes = [IsAuthenticated, IsEmployer]
    # Filtrage des offres par employeur
    
    def get_queryset(self):
        #user = User.objects.filter(id=self.request.user.id)
        #employer = EmployerProfile.objects.filter(user=user )
        # ✅ Retourner toutes les offres sans filtrage par défaut
        #return Job.objects.filter(employer=employer).order_by('-created_at')
        
        # Récupère l'utilisateur connecté (instance unique)
        user = self.request.user
         
        # Vérifie si l'utilisateur a un profil employeur
        if not hasattr(user, 'employer_profile'):
            return Job.objects.none() # Retourne un queryset vide si pas de profil employer
        employer = user.employer_profile
        
        # Filtre les offres par cet employeur
        return Job.objects.filter(employer=employer).order_by('-created_at')    
        
    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, 'employer_profile'):
            raise serializers.ValidationError({'detail': "L'utilisateur n'a pas de profil employeur associé."})

        serializer.save(employer=user.employer_profile)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Activer/Désactiver une offre"""
        job = self.get_object()
        job.is_active = not job.is_active
        job.save()
        return Response({'status': 'success', 'is_active': job.is_active})

    @action(detail=False, methods=['get'])
    def active_jobs(self, request):
        """Liste des offres actives"""
        jobs = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data)
    
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
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def applications_count(self, request, pk=None):
        """
        Retourne le nombre de candidatures pour cette offre
        """
        job = self.get_object()
        count = CandidateApplication.objects.filter(job=job).count()
        return Response({'count': count}, status=status.HTTP_200_OK)


# Affichage des différents d'emplois postés par les candidats
class JobListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]
    

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
            return Response({"details": "Offre d'emploi non fermée ou inexistante."}, status=status.HTTP_404_NOT_FOUND)
        
        # Verifier si le candidat a déjà ce job
        if CandidateApplication.objects.filter(candidate=candidate, job=job).exists():
            return Response({"detail": "Vous avez déjà postulé à cette offre."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calcul du score avec AHP 
        ahp_score = calculate_candidate_score(candidate, job)
        
        # Créer la candidature
        application = CandidateApplication.objects.create(
            candidate=candidate,
            job=job,
            ahp_score=ahp_score
        )
        
        # Mettre à jour le classement après l'ajout de la nouvelle candidature 
        self.update_rankings(job)
        
        serializer = self.get_serializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], permission_classes=[IsCandidate])    
    def my_applications(self, request):
        """
        Lister les candidature du candidat connecté
        """
        candidate = request.user.candidate_profile
        applications = CandidateApplication.objects.filter(candidate=candidate)
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsEmployer])
    def list_for_job(self, request, pk=None):
        """
        Lister toutes les candidatures pour une offre spécifique
        """
        job = get_object_or_404(Job, id=pk)
        applications = CandidateApplication.objects.filter(job=job).order_by('-ahp_score')
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)
    
    
    def update_rankings(self, job):
        """Mise à jour du classement des candidatures après une nouvelle soumission"""
        applications = CandidateApplication.objects.filter(job=job).order_by('-ahp_score')
        for rank, application in enumerate(applications, start=1):
            application.rank = rank
            application.save()   