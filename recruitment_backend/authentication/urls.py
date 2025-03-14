from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    # Route pour la génération du token (login)
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Route pour rafraîchir le token
    path('token/refresh/', CustomTokenObtainPairView.as_view(), name='token_refresh'),
]
