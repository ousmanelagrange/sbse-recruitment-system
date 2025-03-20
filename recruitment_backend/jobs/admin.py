from django.contrib import admin
from .models import  CandidateApplication, Constraint, SkillRequirement, Job 
admin.site.register(CandidateApplication)
admin.site.register(Constraint)
admin.site.register(SkillRequirement)
admin.site.register(Job)

