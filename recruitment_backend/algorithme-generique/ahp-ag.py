import random
import matplotlib.pyplot as plt

# Étape 1 : Offre d'emploi fictive et poids AHP
weights = {
    "java_skills": 0.4,  # Compétences en Java (priorité 1)
    "experience": 0.3,   # Expérience professionnelle (priorité 2)
    "database_skills": 0.2,  # Connaissances en bases de données (priorité 3)
    "languages": 0.05,   # Langues parlées (priorité 4)
    "references": 0.05   # Références professionnelles (priorité 5)
}

# Données statiques des candidats (exemple)
candidates = [
    {"name": "Alice", "java_skills": 5, "experience": 6, "database_skills": 4, "languages": 3, "references": 4},
    {"name": "Bob", "java_skills": 4, "experience": 5, "database_skills": 3, "languages": 4, "references": 3},
    {"name": "Charlie", "java_skills": 7, "experience": 8, "database_skills": 5, "languages": 2, "references": 5},
    {"name": "David", "java_skills": 3, "experience": 4, "database_skills": 2, "languages": 5, "references": 2},
    {"name": "Eve", "java_skills": 6, "experience": 7, "database_skills": 4, "languages": 3, "references": 4},
    {"name": "Frank", "java_skills": 5, "experience": 5, "database_skills": 3, "languages": 4, "references": 3},
    {"name": "Grace", "java_skills": 8, "experience": 9, "database_skills": 6, "languages": 2, "references": 5},
    {"name": "Hannah", "java_skills": 4, "experience": 6, "database_skills": 3, "languages": 4, "references": 3},
    {"name": "Ian", "java_skills": 6, "experience": 7, "database_skills": 4, "languages": 3, "references": 4},
    {"name": "Julia", "java_skills": 5, "experience": 6, "database_skills": 3, "languages": 4, "references": 3},
    {"name": "Kevin", "java_skills": 7, "experience": 8, "database_skills": 5, "languages": 2, "references": 5},
    {"name": "Liam", "java_skills": 4, "experience": 5, "database_skills": 3, "languages": 4, "references": 3}
]

# Normalisation des valeurs entre 0 et 1
def normalize(value, min_value, max_value):
    """
    Normalise une valeur dans une plage spécifique [min_value, max_value].
    Renvoie une valeur normalisée entre 0 et 1.
    """
    return (value - min_value) / (max_value - min_value) if max_value > min_value else 0

# Fonction de satisfaction
def satisfaction_function(candidate):
    """
    Calcule le niveau de satisfaction d'un candidat.
    La satisfaction est basée sur la somme des caractéristiques pondérées.
    
    Formule utilisée :
        satisfaction = Σ (valeur_caractéristique_normalisée * poids_correspondant)
    
    Objectif : Maximiser cette valeur.
    """
    # Valeurs minimales et maximales pour chaque caractéristique
    min_max_values = {
        "java_skills": (3, 8),
        "experience": (4, 9),
        "database_skills": (2, 6),
        "languages": (2, 5),
        "references": (2, 5)
    }

    # Calcul du score normalisé pour chaque caractéristique
    normalized_scores = {
        key: normalize(candidate[key], min_max_values[key][0], min_max_values[key][1])
        for key in weights.keys()
    }

    # Satisfaction totale
    satisfaction = sum(normalized_scores[key] * weights[key] for key in weights.keys())
    return satisfaction

# Fonction de conflit
def conflict_function(candidate):
    """
    Calcule le niveau de conflit d'un candidat.
    Un conflit survient lorsque certaines caractéristiques ne respectent pas les exigences minimales.
    
    Formule utilisée :
        conflit = Σ (pénalités pour chaque critère non satisfait)
    
    Objectif : Minimiser cette valeur (idéalement proche de 0).
    """
    conflict = 0
    if candidate["java_skills"] < 4:  # Conflit pour compétences en Java insuffisantes
        conflict += 1
    if candidate["experience"] < 5:  # Conflit pour expérience insuffisante
        conflict += 1
    if candidate["database_skills"] < 3:  # Conflit pour connaissances en bases de données insuffisantes
        conflict += 1
    return conflict

# Fonction fitness modulaire et optimale
def fitness(individual):
    """
    Calcule le score fitness d'un candidat en combinant la fonction de satisfaction
    et la fonction de conflit.
    
    Formule utilisée :
        fitness = satisfaction - (conflit * facteur_pénalité)
    
    Objectif : Maximiser cette valeur.
    """
    satisfaction = satisfaction_function(individual)
    conflict = conflict_function(individual)
    penalty_factor = 0.5  # Facteur de pénalité pour les conflits
    return satisfaction - (conflict * penalty_factor)

# Calcul des scores fitness pour chaque candidat
for candidate in candidates:
    candidate["fitness_score"] = fitness(candidate)

# Tri des candidats par score fitness décroissant
sorted_candidates = sorted(candidates, key=lambda x: x["fitness_score"], reverse=True)

# Affichage des meilleurs candidats après calcul du fitness
print("Meilleurs candidats sélectionnés après calcul du fitness (population initiale) :")
for i, candidate in enumerate(sorted_candidates[:10], start=1):
    print(f"{i}. {candidate['name']} - Score Fitness : {candidate['fitness_score']:.2f}")
    print(f"   Raison : Fortes compétences en Java ({candidate['java_skills']}), "
          f"expérience solide ({candidate['experience']}), "
          f"bonnes connaissances en bases de données ({candidate['database_skills']}).\n")

# Graphique représentatif des scores fitness
names = [candidate["name"] for candidate in sorted_candidates]
scores = [candidate["fitness_score"] for candidate in sorted_candidates]

plt.figure(figsize=(12, 6))
plt.bar(names, scores, color='skyblue')
plt.title("Scores Fitness des candidats")
plt.xlabel("Candidats")
plt.ylabel("Score Fitness")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Population initiale pour l'algorithme génétique
initial_population = sorted_candidates[:10]

# Paramètres de l'algorithme génétique
POPULATION_SIZE = 15  # Augmentation de la taille de la population pour plus de diversité
GENERATIONS = 20      # Augmentation du nombre de générations pour mieux converger
CROSSOVER_RATE = 0.8  # Probabilité de croisement
MUTATION_RATE = 0.2   # Augmentation légère de la probabilité de mutation

# Sélection par tournoi
def tournament_selection(population, k=3):
    """
    Sélectionne un individu en comparant k candidats aléatoires.
    Le candidat avec le score fitness le plus élevé est retenu.
    """
    selected = random.sample(population, k)
    return max(selected, key=lambda x: fitness(x))

# Croisement à un point
def single_point_crossover(parent1, parent2):
    """
    Combine les caractéristiques de deux parents pour créer deux enfants.
    Un point de croisement est choisi aléatoirement.
    """
    point = random.randint(1, len(parent1) - 1)
    child1 = {**parent1, **{key: parent2[key] for key in list(parent2.keys())[point:]}}
    child2 = {**parent2, **{key: parent1[key] for key in list(parent1.keys())[point:]}}
    return child1, child2

# Mutation
def mutate(individual):
    """
    Modifie aléatoirement une caractéristique d'un individu pour introduire de la diversité.
    Les modifications sont limitées pour éviter des valeurs invalides.
    """
    attribute = random.choice(list(individual.keys()))
    if isinstance(individual[attribute], int):
        individual[attribute] += random.choice([-1, 1])
        # Assure que les valeurs restent dans des plages valides
        if attribute == "java_skills":
            individual[attribute] = max(1, min(10, individual[attribute]))
        elif attribute == "experience":
            individual[attribute] = max(1, min(10, individual[attribute]))
        elif attribute == "database_skills":
            individual[attribute] = max(1, min(10, individual[attribute]))
        elif attribute == "languages":
            individual[attribute] = max(1, min(5, individual[attribute]))
        elif attribute == "references":
            individual[attribute] = max(1, min(5, individual[attribute]))
    return individual

# Algorithme génétique principal
def genetic_algorithm():
    population = l_population
    best_individual = None
    best_fitness = float('-inf')
    best_per_generation = []  # Pour suivre le meilleur individu de chaque génération

    for generation in range(GENERATIONS):
        new_population = []

        while len(new_population) < POPULATION_SIZE:
            # Sélection par tournoi
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)

            # Croisement
            if random.random() < CROSSOVER_RATE:
                child1, child2 = single_point_crossover(parent1, parent2)
                new_population.extend([child1, child2])
            else:
                new_population.extend([parent1, parent2])

            # Mutation
            for individual in new_population:
                if random.random() < MUTATION_RATE:
                    mutate(individual)

        # Mise à jour de la population
        population = new_population

        # Suivi du meilleur individu de cette génération
        current_best = max(population, key=lambda x: fitness(x))
        if fitness(current_best) > best_fitness:
            best_individual = current_best
            best_fitness = fitness(current_best)

        best_per_generation.append((generation + 1, best_individual["name"], best_fitness))
        print(f"Génération {generation + 1} : Meilleur candidat = {best_individual['name']} (Score = {best_fitness:.2f})")

    # Graphique des meilleurs scores par génération
    generations, names, scores = zip(*best_per_generation)
    plt.figure(figsize=(10, 6))
    plt.plot(generations, scores, marker='o', color='b')
    plt.title("Évolution du meilleur score par génération")
    plt.xlabel("Génération")
    plt.ylabel("Meilleur score Fitness")
    plt.xticks(generations)
    plt.grid()
    plt.show()

    return best_individual

# Exécution de l'algorithme génétique
best_candidate = genetic_algorithm()
print("\nMeilleur candidat trouvé après l'algorithme génétique :")
print(f"Nom : {best_candidate['name']}")
print(f"Score Fitness : {best_candidate['fitness_score']:.2f}")
print("Raisons :")
print(f"- Excellentes compétences en Java ({best_candidate['java_skills']}) correspondant à la priorité 1.")
print(f"- Expérience professionnelle solide ({best_candidate['experience']}) correspondant à la priorité 2.")
print(f"- Bonnes connaissances en bases de données ({best_candidate['database_skills']}) correspondant à la priorité 3.")