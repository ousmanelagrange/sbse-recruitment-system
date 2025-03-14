from django.contrib import admin
from .models import CandidateProfile, EmployerProfile, User 

admin.site.register(CandidateProfile)
admin.site.register(EmployerProfile)
admin.site.register(User)