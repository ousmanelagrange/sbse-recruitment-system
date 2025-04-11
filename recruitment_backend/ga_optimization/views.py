from django.shortcuts import render
from jobs.models import CandidateProfile

# This module contains the genetic algorithm implementation for candidate optimization.
import random
import numpy as np
import math


def get_population_size():
    """
    Retourne le nombre total de candidats disponibles pour le job.
    """
    return CandidateProfile.objects.count()
# ---------------------------
# Paramètres et configuration
# ---------------------------

POPULATION_SIZE = get_population_size()       # Taille finale de la population et des générations suivantes


POOL_INIT = int(POPULATION_SIZE*0.5)         # Taille du pool initial pour la sélection gloutonne (ex. 5 fois POPULATION_SIZE)
GENERATIONS = 7      # Nombre maximum de générations
TOURNAMENT_SIZE = int(POPULATION_SIZE*0.2)         # Nombre de candidats dans chaque tournoi
CROSSOVER_PROB = 0.8        # Probabilité de croisement entre deux parents
MUTATION_PROB = 0.2         # Probabilité de mutation par gène dans un individu
ELITISM_COUNT = 2           # Nombre d'individus conservés dans chaque génération (élitisme)
MIN_DISTANCE = 2.0          # Distance minimale entre deux candidats pour garantir la diversité

# Critère d'arrêt basé sur la stagnation : arrêter si la meilleure fitness n'améliore pas 
AMELIORATION_SEUIL = 0.1   # 10% d'amélioration minimale relative requise
STAGNATION_LIMIT = 2  # Nombre de générations consécutives sans amélioration suffisante

#on recupere les criteres
RANGES = {
    'experience': (0, 10),
    'technique': (0, 10),
    'soft_skills': (0, 10),
    'communication': (0, 10)
}

#on recupere les criteres pour chaque jobs avec son poids AHP
POIDS_CRITERES = {
    'experience': 0.4,
    'technique': 0.3,
    'soft_skills': 0.2,
    'communication': 0.1
}

#onfixe les seuils minimaux pour chaque critere
SEUILS = {
    'experience': 7,
    'technique': 6,
    'communication': 5
}

#on fixe les penalites pour chaque critere
COEF_PENALITES = {
    'experience': 2.0,
    'technique': 1.5,
    'communication': 1.0
}

# ---------------------------
# Fonctions
# ---------------------------
def generate_candidate(generation):
    candidat = {
        'chromosome': {},
        'generation': generation
    }
    for critere, (min_val, max_val) in RANGES.items():
        candidat['chromosome'][critere] = random.uniform(min_val, max_val)
    return candidat

def fitness_advanced(candidat):
    chromosome = candidat['chromosome']
    score_global = 0.0
    penalite_totale = 0.0

    for critere, score in chromosome.items():
        poids = POIDS_CRITERES.get(critere, 0)
        score_global += score * poids
        seuil_min = SEUILS.get(critere)
        if seuil_min is not None and score < seuil_min:
            coef = COEF_PENALITES.get(critere, 1.0)
            penalite_totale += coef * (seuil_min - score)
    return score_global - penalite_totale

def distance_candidates(c1, c2):
    return math.sqrt(sum((c1['chromosome'][k] - c2['chromosome'][k])**2 for k in RANGES))

def greedy_initial_population():
    pool = [generate_candidate(0) for _ in range(POOL_INIT)]
    evaluated_pool = [(cand, fitness_advanced(cand)) for cand in pool]
    evaluated_pool.sort(key=lambda x: x[1], reverse=True)
    selected = []
    for candidate, _ in evaluated_pool:
        if len(selected) >= POPULATION_SIZE:
            break
        if all(distance_candidates(candidate, s) >= MIN_DISTANCE for s in selected):
            selected.append(candidate)
    while len(selected) < POPULATION_SIZE:
        for candidate, _ in evaluated_pool:
            if candidate not in selected:
                selected.append(candidate)
            if len(selected) >= POPULATION_SIZE:
                break
    return selected

def tournament_selection(evaluated):
    participants = random.sample(evaluated, TOURNAMENT_SIZE)
    return max(participants, key=lambda x: x[1])[0]

def two_point_fixed_crossover(p1, p2):
    child = {
        'chromosome': {},
        'generation': max(p1['generation'], p2['generation']) + 1
    }
    keys = list(RANGES.keys())
    for i, key in enumerate(keys):
        if 1 <= i < 3:
            child['chromosome'][key] = p2['chromosome'][key]
        else:
            child['chromosome'][key] = p1['chromosome'][key]
    return child

def mutate(candidate, prob, sigma=0.1):
    for critere in candidate['chromosome']:
        if random.random() < prob:
            val = candidate['chromosome'][critere]
            val += np.random.normal(0, sigma)
            min_val, max_val = RANGES[critere]
            candidate['chromosome'][critere] = max(min_val, min(max_val, val))
    return candidate

def evaluate_population(population):
    return [(cand, fitness_advanced(cand)) for cand in population]

def genetic_algorithm():
    population = greedy_initial_population()
    best_global = None
    best_global_fitness = -float("inf")
    stagnation = 0

    for generation in range(GENERATIONS):
        evaluated = evaluate_population(population)
        evaluated.sort(key=lambda x: x[1], reverse=True)

        best_fitness = evaluated[0][1]
        avg_fitness = sum(f for _, f in evaluated) / len(evaluated)
        print(f"\n📊 Génération {generation} - Meilleure fitness: {best_fitness:.2f} | Moyenne: {avg_fitness:.2f}")

        for idx, (cand, fit) in enumerate(evaluated):
            print(f"  Candidat {idx+1:2d} | Génération: {cand['generation']:3d} | Fitness: {fit:.2f} | Chromosome: {cand['chromosome']}")

        if best_fitness > best_global_fitness * (1 + AMELIORATION_SEUIL):
            best_global = evaluated[0]
            best_global_fitness = best_fitness
            stagnation = 0
        else:
            stagnation += 1

        if stagnation >= STAGNATION_LIMIT:
            print("\n⛔ Arrêt anticipé : stagnation détectée.")
            break

        elites = [cand for cand, _ in evaluated[:ELITISM_COUNT]]
        new_population = elites.copy()

        while len(new_population) < POPULATION_SIZE:
            parent1 = tournament_selection(evaluated)
            parent2 = tournament_selection(evaluated)
            if random.random() < CROSSOVER_PROB:
                enfant = two_point_fixed_crossover(parent1, parent2)
            else:
                enfant = {
                    'chromosome': parent1['chromosome'].copy(),
                    'generation': generation + 1
                }
            enfant = mutate(enfant, MUTATION_PROB)
            new_population.append(enfant)

        population = new_population

    return best_global

# if __name__ == "__main__":
#     best, fit = genetic_algorithm()
#     print("\n🏆 Meilleur candidat trouvé :")
#     print(f"Génération: {best['generation']} | Fitness: {fit:.2f} | Chromosome: {best['chromosome']}")


