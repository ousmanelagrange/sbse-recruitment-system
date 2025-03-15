from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CVUploadViewSet

router = DefaultRouter()
router.register(r'cv-uploads', CVUploadViewSet)

urlpatterns = [
    path('', include(router.urls)),
]