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

# Fonction pour calculer le score AHP (fonction objectif)
def calculate_ahp_score(candidate):
    """
    Calcule le score AHP d'un candidat en fonction des critères pondérés.
    Ce score représente la capacité du candidat à répondre aux exigences de l'offre d'emploi.
    """
    score = (
        candidate["java_skills"] * weights["java_skills"] +
        candidate["experience"] * weights["experience"] +
        candidate["database_skills"] * weights["database_skills"] +
        candidate["languages"] * weights["languages"] +
        candidate["references"] * weights["references"]
    )
    return score

# Calcul des scores AHP pour chaque candidat
for candidate in candidates:
    candidate["ahp_score"] = calculate_ahp_score(candidate)

# Tri des candidats par score AHP décroissant
sorted_candidates = sorted(candidates, key=lambda x: x["ahp_score"], reverse=True)

# Affichage des meilleurs candidats après AHP
print("Meilleurs candidats sélectionnés après AHP (population initiale) :")
for i, candidate in enumerate(sorted_candidates[:10], start=1):
    print(f"{i}. {candidate['name']} - Score AHP : {candidate['ahp_score']:.2f}")
    print(f"   Raison : Fortes compétences en Java ({candidate['java_skills']}), "
          f"expérience solide ({candidate['experience']}), "
          f"bonnes connaissances en bases de données ({candidate['database_skills']}).\n")

# Graphique représentatif des scores AHP
names = [candidate["name"] for candidate in sorted_candidates]
scores = [candidate["ahp_score"] for candidate in sorted_candidates]

plt.figure(figsize=(12, 6))
plt.bar(names, scores, color='skyblue')
plt.title("Scores AHP des candidats")
plt.xlabel("Candidats")
plt.ylabel("Score AHP")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Population initiale pour l'algorithme génétique
initial_population = sorted_candidates[:10]

# Paramètres de l'algorithme génétique
POPULATION_SIZE = 10  # Taille de la population
GENERATIONS = 10      # Nombre de générations
CROSSOVER_RATE = 0.8  # Probabilité de croisement
MUTATION_RATE = 0.1   # Probabilité de mutation

# Fonction fitness (basée sur le score AHP)
def fitness(individual):
    """
    La fonction fitness évalue à quel point un individu (candidat) répond aux exigences de l'offre d'emploi.
    Plus le score est élevé, plus le candidat est adapté.
    """
    return individual["ahp_score"]

# Sélection par tournoi
def tournament_selection(population, k=3):
    """
    Sélectionne un individu en comparant k candidats aléatoires.
    Le candidat avec le score fitness le plus élevé est retenu.
    """
    selected = random.sample(population, k)
    return max(selected, key=fitness)

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
    """
    attribute = random.choice(list(individual.keys()))
    if isinstance(individual[attribute], int):
        individual[attribute] += random.choice([-1, 1])
    return individual

# Algorithme génétique principal
def genetic_algorithm():
    population = initial_population
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
        current_best = max(population, key=fitness)
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
    plt.ylabel("Meilleur score AHP")
    plt.xticks(generations)
    plt.grid()
    plt.show()

    return best_individual

# Exécution de l'algorithme génétique
best_candidate = genetic_algorithm()
print("\nMeilleur candidat trouvé après l'algorithme génétique :")
print(f"Nom : {best_candidate['name']}")
print(f"Score AHP : {best_candidate['ahp_score']:.2f}")
print("Raisons :")
print(f"- Excellentes compétences en Java ({best_candidate['java_skills']}) correspondant à la priorité 1.")
print(f"- Expérience professionnelle solide ({best_candidate['experience']}) correspondant à la priorité 2.")
print(f"- Bonnes connaissances en bases de données ({best_candidate['database_skills']}) correspondant à la priorité 3.")