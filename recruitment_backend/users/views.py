
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserWithCandidateProfileSerializer, UserWithEmployerProfileSerializer, UserSerializer, UserUpdateSerializer
from rest_framework import generics, status, viewsets
from .models import User, CandidateProfile, EmployerProfile



# Vue pour la mise à jour d'un utilisateur
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        user = self.get_object() 
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vue administrateur des utilisateurs
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class CandidateProfileViewSet(viewsets.ModelViewSet):
    queryset = CandidateProfile.objects.all()
    serializer_class = UserWithCandidateProfileSerializer
    permission_classes = [AllowAny]
    
class EmployerProfileViewSet(viewsets.ModelViewSet):
    queryset = EmployerProfile.objects.all()
    serializer_class = UserWithEmployerProfileSerializer
    permission_classes = [AllowAny]