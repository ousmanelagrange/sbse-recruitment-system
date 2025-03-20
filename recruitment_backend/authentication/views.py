from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenBlacklistView
from users.serializers import UserSerializer, CandidateProfileSerializer, EmployerProfileSerializer
from rest_framework.permissions import AllowAny 
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
# Obtenir un token
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'access': response.data['access'],
            'refresh': response.data['refresh'],
            'message': 'Authentication successful'
        }, status=status.HTTP_200_OK)

# Rafraîchir un token
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({
            'access': response.data['access'],
            'message': 'Token refreshed successfully'
        }, status=status.HTTP_200_OK)

# Blacklister un token afin de se déconnecter
class LogoutView(TokenBlacklistView):
    pass


# View pour l'inscription d'un utilisateur 
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        # Instancie le serializer avec les données 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  
        user = serializer.save()
        
        # Génération des tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Construction de la réponse avec les données du profil 
        if user.role == 'candidate':
            profile_data = CandidateProfileSerializer(user.candidate_profile).data
        elif user.role == 'employer':
            profile_data = EmployerProfileSerializer(user.employer_profile).data
        else:
            profile_data = {}
        # Retourner les données de l'utilisateur créé 
        data = {
            'user' : {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'phone_number': user.phone_number
                },
            'profile': profile_data,
            'tokens': {
                'access': access_token,
                'refresh': refresh_token
               }
            }
        return Response(data, status=status.HTTP_201_CREATED)
