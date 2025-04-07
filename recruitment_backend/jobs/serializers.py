from rest_framework import serializers 
from .models import Job, Constraint, SkillRequirement, CandidateApplication 

# Serializer pour les contraintes
class ConstraintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constraint
        fields = '__all__'
        read_only_fields = ['job'] 

# Serializer pour les Compétences
class SkillRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillRequirement 
        fields = '__all__'
        read_only_fields = ['job'] 

# Serializer pour une offre d'emploi 
class JobSerializer(serializers.ModelSerializer):
    constraints = ConstraintSerializer(many=True, required=False)
    skill_requirements = SkillRequirementSerializer(many=True, required=False)
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['employer', 'created_at', 'updated_at', 'published_at']

    def create(self, validated_data):
        # Extraire les contraintes et compétences
        constraints_data = validated_data.pop('constraints', [])
        skill_requirements_data = validated_data.pop('skill_requirements', [])
        
        # Créer le job
        job = Job.objects.create(**validated_data)
        
        # Créer les contraintes si elles n'existent pas déjà
        for constraint_data in constraints_data:
            if not Constraint.objects.filter(job=job, description=constraint_data['description']).exists():
                Constraint.objects.create(job=job, **constraint_data)
        
        # Créer les compétences si elles n'existent pas déjà
        for skill_data in skill_requirements_data:
            if not SkillRequirement.objects.filter(job=job, name=skill_data['name']).exists():
                SkillRequirement.objects.create(job=job, **skill_data)
        
        return job

    
    def update(self, instance, validated_data):
        # Extraire les données des contraintes et compétences
        constraints_data = validated_data.pop('constraints', [])
        skill_requirements_data = validated_data.pop('skill_requirements', [])
        
        # ✅ Mettre à jour les champs de l'offre
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # ✅ Supprimer et recréer les contraintes et compétences
        instance.constraints.all().delete()
        instance.skill_requirements.all().delete()
        for constraint_data in constraints_data:
            Constraint.objects.create(job=instance, **constraint_data)
        for skill_data in skill_requirements_data:
            SkillRequirement.objects.create(job=instance, **skill_data)
        
        return instance
    

# Serializer pour une candidature 
class CandidateApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateApplication 
        fields = '__all__'
        read_only_fields = ['ahp_score', 'ag_score', 'rank', 'created_at']
