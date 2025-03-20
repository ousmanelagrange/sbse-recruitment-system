from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CandidateProfileViewSet, EmployerProfileViewSet, UserUpdateView
router = DefaultRouter()
router.register('users', UserViewSet)
router.register('candidate-profiles', CandidateProfileViewSet)
router.register('employer-profiles', EmployerProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('update-profile/', UserUpdateView.as_view(), name='update-user'),
]