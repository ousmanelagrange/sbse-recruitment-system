from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import CandidateProfile, EmployerProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # Champs supplémentaires pour le profil candidat
    cv = serializers.FileField(required=False)
    bio = serializers.CharField(required=False)

    # Champs supplémentaires pour le profil employeur
    company_name = serializers.CharField(required=False)
    sector = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username','name', 'email', 'password', 'role', 'phone_number', 'cv', 'bio', 'company_name', 'sector', 'description']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extraire les données spécifiques au profil
        cv = validated_data.pop('cv', None)
        bio = validated_data.pop('bio', '')
        company_name = validated_data.pop('company_name', '')
        sector = validated_data.pop('sector', '')
        description = validated_data.pop('description', '')

        # Création de l'utilisateur
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            phone_number=validated_data.get('phone_number', '')
        )

        # Si le rôle est candidat, création du profil candidat
        if user.role == 'candidate':
            CandidateProfile.objects.create(
                user=user,
                cv=cv,
                bio=bio
            )

        # Si le rôle est employeur, création du profil employeur
        elif user.role == 'employer':
            EmployerProfile.objects.create(
                user=user,
                company_name=company_name,
                sector=sector,
                description=description
            )

        return user

class CandidateProfileSerializer(serializers.ModelSerializer):
    cv = serializers.FileField(required=False, allow_null=True)
    class Meta:
        model = CandidateProfile
        fields = ['cv', 'bio']  
# Sérializer avec les données de l'utilisateur et du profil candidat
class UserWithCandidateProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    cv = serializers.FileField(required=False, allow_null=True)
    class Meta:
        model = CandidateProfile
        fields = '__all__' 

class EmployerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'sector', 'description']
class UserWithEmployerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = EmployerProfile
        fields = '__all__'


# Serializers pour permettre la mise à jour des informations 
class UserUpdateSerializer(serializers.ModelSerializer):
    cv = serializers.FileField(required=False, allow_null=True) 
    bio = serializers.CharField(required=False, allow_blank=True)
    company_name = serializers.CharField(required=False, allow_blank=True)
    sector = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = User
        fields = ['username','name', 'email', 'phone_number', 'role', 'cv', 'bio', 'company_name', 'sector', 'description']
        extra_kwargs = {
            'email' : {'read_only': True},
            'role' : {'read_only': True}
        }
        
        def update(self, instance, validated_data):
            # Mise à jour des champs du modèle User
            instance.username = validated_data.get('username', instance.username)
            instance.phone_number = validated_data.get('phone_number', instance.phone_number)
            instance.save()
            
            # Mise à jour des chmps en fonction du rôle 
            if instance.role == 'candidate':
                candidate_profile = instance.candidate_profile
                candidate_profile.bio = validated_data.get('bio', candidate_profile.bio)
                candidate_profile.cv = validated_data.get('cv', candidate_profile.cv)
                candidate_profile.save()
                
            elif instance.role == 'employer':
                employer_profile = instance.employer_profile
                employer_profile.company_name = validated_data.get('company_name', employer_profile.company_name)
                employer_profile.sector = validated_data.get('sector', employer_profile.sector)
                employer_profile.description = validated_data.get('description', employer_profile.description)
                employer_profile.save()
                
            return instance