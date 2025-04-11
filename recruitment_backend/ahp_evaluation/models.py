from django.db import models
from users.models import CandidateProfile

"""
Modeèle de donnes pour recuillir les informations
génériques du candidat : (similaire à un cv)
"""

class GenericCandidateForm(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    # informations générales du candidat (similaire à un Cv)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    
    # Expérience professionnelle
    experience = models.TextField(blank=True, null=True) # Description des expériences
    skills = models.TextField(blank=True, null=True) #Compétences générale
    
    # Formation
    education = models.TextField(blank=True, null=True) # Parcours académique
     # Projets personnels ou professionnels
    projects = models.TextField(blank=True, null=True)  # Projets ou réalisations notables
    
    # Compétences en communication, adaptabilité, etc. (Soft skills)
    communication_skills = models.FloatField(null=True, blank=True)
    adaptability_skills = models.FloatField(null=True, blank=True)
    
    # Langues parlées
    languages = models.TextField(blank=True, null=True)  # Langues parlées et niveau
    def __str__(self):
        return f"Formulaire générique de {self.candidate.user.username}"   