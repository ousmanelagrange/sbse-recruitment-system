from django.contrib.auth.models import AbstractUser
from django.db import models

# Modèle personnalisé pour l'utilisateur
class User(AbstractUser):

    
    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('employer', 'Employeur'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES) 
    name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    USERNAME_FIELD = 'email'  # On utilise l'email comme identifiant
    REQUIRED_FIELDS = ['username']      # Aucun autre champ requis
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# Modèle pour les profils des candidats
class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    cv = models.FileField(upload_to='cv/', blank=True, null=True)  # Stockage local des CV
    bio = models.TextField(blank=True)    
    def __str__(self):
        return f"Candidate Profile: {self.user.username}"

# Modèle pour les profils des employeurs
class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255)
    sector = models.CharField(max_length=100)
    description = models.TextField(blank=True)    
    def __str__(self):
        return f"Employer Profile: {self.user.username} - {self.company_name}"
