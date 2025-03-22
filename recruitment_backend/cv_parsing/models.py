from django.db import models
from django.utils import timezone

# Create your models here.
class CVParsedData(models.Model):
    """Model to store parsed CV data"""
    name = models.CharField(max_length=255, help_text="Full name of the candidate")
    email = models.EmailField(help_text="Email address of the candidate")
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Contact phone number")
    skills = models.TextField(blank=True, null=True, help_text="List of candidate skills")
    experience = models.TextField(blank=True, null=True, help_text="Work experience details")
    education = models.TextField(blank=True, null=True, help_text="Education history")
    resume_text = models.TextField(blank=True, null=True, help_text="Full text content of the CV")
    created_at = models.DateTimeField(default=timezone.now, help_text="When the CV was parsed")
    
    class Meta:
        verbose_name = "CV Parsed Data"
        verbose_name_plural = "CV Parsed Data"
    
    def __str__(self):
        return f"{self.name} - {self.email}"
