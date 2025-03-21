from django.db import models
from users.models import EmployerProfile, CandidateProfile


class Job(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    
    employer = models.ForeignKey(
        EmployerProfile, 
        on_delete=models.CASCADE, 
        related_name='jobs'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255) #lieu de travail
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateField() # Date limite pour postuler
    published_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title 
    
"""
Ce modèle stocke les contrainte définis pour chaque offre d'emploi.
➡️ Il inclut les champs suivants :
 description → description du critère (Exemple : "J'y tiens absolument")
 type → Type du critère (hard ou soft)
 weight → Poids du critère (pour l'AHP)
 job → Relation avec l'offre d'emploi
"""

class Constraint(models.Model):
    CONSTRAINT_TYPE_CHOICES = [
        ('hard', 'Hard'),
        ('soft', 'Soft'),
    ]
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='constraints'
    )
    type = models.CharField(max_length=10, choices=CONSTRAINT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    weight = models.FloatField(default=1.0) #Poids de la contrainte dans le calcul du score (pour AHP)
    
    def __str__(self):
        return f"{self.description} - ({self.get_type_display()})"
    
"""
➡️ Ce modèle permettra de spécifier les compétences attendues pour un poste donné.
"""
class SkillRequirement(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='skill_requirements'
    )
    name = models.CharField(max_length=255)
    weight = models.FloatField() # Poids dans le calcul du score(pour AHP)
    
   
    
"""
Ce modèle représente une candidature à une offre d'emploi.
➡️ Il inclut les champs suivants :
    candidate → Lien avec le profil du candidat
    job → Lien avec l'offre d'emploi
    score → Score généré par l'AHP
    rank → Classement du candidat
    status → Statut de la candidature (pending, accepted, rejected)
"""

class CandidateApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    score = models.FloatField() #score généré par AHP
    rank = models.IntegerField(null=True, blank=True) # classement
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return f"{self.candidate.user.username} - {self.job.title}"