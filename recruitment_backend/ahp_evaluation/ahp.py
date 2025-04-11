import numpy as np
from ahp_evaluation.models import GenericCandidateForm
from users.models import Job, Constraint, SkillRequirement

class AHP:
    def __init__(self, job, candidate):
        """
        Initialise l'AHP avec le poste et le candidat.
        job: L'objet Job (contenant les contraintes et compétences)
        candidate: L'objet Candidate (contenant les informations sur le CV)
        """
        self.job = job
        self.candidate = candidate
        self.matrice_comparaison = self._creer_matrice_comparaison()

        # Récupération des informations du candidat via le formulaire générique
        self.form_data = GenericCandidateForm.objects.filter(candidate=self.candidate).first()

    def _creer_matrice_comparaison(self):
        """
        Crée la matrice de comparaison par paires basée sur les critères du job.
        Cette matrice doit être remplie en fonction de la comparaison des critères entre eux.
        """
        num_criteres = 3  # Exemple: 3 critères - contraintes hard, contraintes soft, compétences
        matrice_comparaison = np.ones((num_criteres, num_criteres))

        # Comparaison entre les critères (par exemple entre les types de contraintes et les compétences)
        matrice_comparaison[0, 1] = 1 / 2  # Les contraintes hard sont moins importantes que les soft (par exemple)
        matrice_comparaison[1, 0] = 2

        matrice_comparaison[0, 2] = 1 / 3  # Les contraintes hard sont moins importantes que les compétences
        matrice_comparaison[2, 0] = 3

        matrice_comparaison[1, 2] = 1  # Les contraintes soft et les compétences sont de même importance
        matrice_comparaison[2, 1] = 1

        return matrice_comparaison

    def calculer_poids_criteres(self):
        """
        Calcule les poids des critères en utilisant la matrice de comparaison.
        """
        # Normalisation de la matrice de comparaison
        matrice_normalisee = self.matrice_comparaison / self.matrice_comparaison.sum(axis=0)

        # Calcul des poids (moyenne des lignes)
        poids_criteres = matrice_normalisee.mean(axis=1)
        return poids_criteres

    def calculer_score_candidat(self):
        """
        Calcule le score global du candidat en fonction des critères et des poids.
        """
        poids_criteres = self.calculer_poids_criteres()

        # Évaluation des contraintes hard
        score_hard = self.evaluer_contraintes_hard()
        # Évaluation des contraintes soft
        score_soft = self.evaluer_contraintes_soft()
        # Évaluation des compétences
        score_competences = self.evaluer_competences()

        # Combinaison des scores en fonction des poids
        score_total = (score_hard * poids_criteres[0] +
                       score_soft * poids_criteres[1] +
                       score_competences * poids_criteres[2])

        return round(score_total * 100, 2)

    def evaluer_contraintes_hard(self):
        """
        Évalue si le candidat satisfait les contraintes hard (par exemple, expérience).
        """
        score_hard = 0
        for contrainte in self.job.constraints.filter(type='hard'):
            # On vérifie si la contrainte (comme une expérience) est présente dans le formulaire du candidat
            if contrainte.description.lower() in self.form_data.experience.lower():
                score_hard += 1
        return score_hard / len(self.job.constraints.filter(type='hard')) if self.job.constraints.filter(type='hard') else 1

    def evaluer_contraintes_soft(self):
        """
        Évalue si le candidat satisfait les contraintes soft (par exemple, compétences en communication).
        """
        score_soft = 0
        for contrainte in self.job.constraints.filter(type='soft'):
            # On vérifie si la contrainte (comme des compétences en communication) est présente dans le formulaire du candidat
            if contrainte.description.lower() in self.form_data.communication_skills:
                score_soft += 1
        return score_soft / len(self.job.constraints.filter(type='soft')) if self.job.constraints.filter(type='soft') else 1

    def evaluer_competences(self):
        """
        Évalue si le candidat possède les compétences requises pour le poste.
        """
        score_competences = 0
        for competence in self.job.skill_requirements.all():
            # On vérifie si la compétence est présente dans les données du formulaire du candidat
            if competence.name.lower() in self.form_data.skills.lower():
                score_competences += 1
        return score_competences / len(self.job.skill_requirements.all()) if self.job.skill_requirements.all() else 0

    def __str__(self):
        """
        Affiche un résumé du calcul du score du candidat.
        """
        score = self.calculer_score_candidat()
        return f"Score global du candidat: {score}%"
