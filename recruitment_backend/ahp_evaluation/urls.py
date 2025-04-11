# ats/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenericCandidateFormViewSet, AHPComputeAPIView

router = DefaultRouter()
router.register(r'candidate-forms', GenericCandidateFormViewSet, basename='candidate-form')
router.register(r'compute/', AHPComputeAPIView, basename='ahp-compute')

urlpatterns = [
    path('', include(router.urls)),
    # path(),
]
