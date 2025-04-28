from django.db import models
from django.utils import timezone
from django.db import models
from users.models import User
"""
Modeèle de donnes pour recuillir les informations
génériques du candidat : (similaire à un cv)
"""

"""
Modèle de données pour recueillir les informations génériques du candidat.
Cela sert à construire un "profil AHP" pour le matching avec les contraintes du job.
"""

class CandidateForm(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="generic_forms"
    )
    name = models.CharField(
        max_length=255,
        help_text="Nom du critère renseigné par le candidat (ex: 'Mobilité géographique', 'Compétence Python')"
    )
    value = models.CharField(
        max_length=255,
        help_text="Valeur du critère renseigné par le candidat (ex: 'Oui', 'Non', 'Expert', 'Intermédiaire')"
    )

    weight = models.FloatField(
        default=1.0,
        help_text="Importance du critère selon le candidat (1.0 par défaut)"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.weight})"
