def calculate_candidate_score(candidate, job):
    total_score = 0
    weight_sum = 0

    # Évaluation des contraintes (Hard + Soft)
    for constraint in job.constraints.all():
        if constraint.type == 'hard':
            # Les hard skills doivent être obligatoires → Si manquante, score très faible
            value = 1 if meets_hard_criteria(candidate, constraint) else 0
        else:
            # Soft skills → Calcul en fonction du poids
            value = evaluate_soft_criteria(candidate, constraint)

        total_score += value * constraint.weight
        weight_sum += constraint.weight

    # Évaluation des compétences techniques
    for skill in job.skill_requirements.all():
        value = evaluate_skill_match(candidate, skill)
        total_score += value * skill.weight
        weight_sum += skill.weight

    if weight_sum == 0:
        return 0

    return round((total_score / weight_sum) * 100, 2)

def meets_hard_criteria(candidate, constraint):
    # Exemple : Vérification de l'expérience professionnelle dans le CV
    if constraint.description.lower() in candidate.bio.lower():
        return True
    return False

def evaluate_soft_criteria(candidate, constraint):
    # Exemple : Vérification des compétences douces (adaptabilité, communication)
    if constraint.description.lower() in candidate.bio.lower():
        return 0.8
    return 0.2

def evaluate_skill_match(candidate, skill):
    # Exemple : Vérification des compétences techniques dans le CV
    if skill.name.lower() in candidate.bio.lower():
        return 1
    return 0
