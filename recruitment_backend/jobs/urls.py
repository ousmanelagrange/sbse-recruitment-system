from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, CandateApplicationViewSet, JobListViewSet


router = DefaultRouter()
router.register('jobs', JobViewSet)
router.register('applications', CandateApplicationViewSet)
router.register('job_list', JobListViewSet, basename='job-list')


urlpatterns = [
    path('', include(router.urls)),
]
