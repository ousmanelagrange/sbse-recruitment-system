from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, CandateApplicationViewSet

router = DefaultRouter()
router.register('jobs', JobViewSet)
router.register('applications', CandateApplicationViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
