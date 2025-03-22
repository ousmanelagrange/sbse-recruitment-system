# filepath: /home/aureltoukam/Bureau/Master 2/SBSE/projet SBSE/sbse-recruitment-system/recruitment_backend/cv_upload/urls.py
from django.urls import path
from .views import upload_cv

urlpatterns = [
    path('upload/', upload_cv, name='upload_cv'),
]