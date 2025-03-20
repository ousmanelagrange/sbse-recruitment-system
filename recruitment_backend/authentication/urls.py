from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, LogoutView, RegisterView

urlpatterns = [
    # Route pour la génération du token (login)
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Route pour rafraîchir le token
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/logout/',LogoutView.as_view(), name='token_blacklist'),
    path('register/', RegisterView.as_view(), name='register'),
]
