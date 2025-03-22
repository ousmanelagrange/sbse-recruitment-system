from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CVParsingView, CVParsedDataViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="CV Parsing API",
        default_version='v1',
        description="API for parsing and storing CV data",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'cv-parsed-data', CVParsedDataViewSet)

urlpatterns = [
    path('parse/', CVParsingView.as_view(), name='cv-parse'),
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
