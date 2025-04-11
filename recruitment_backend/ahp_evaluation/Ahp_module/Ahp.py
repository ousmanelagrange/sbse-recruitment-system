import random

import numpy as np


class AHP:
    """Classe AHP améliorée avec corrections et optimisations"""

    def __init__(self, pair_wise_comparison_matrix):
        self.pair_wise_comparison_matrix = pair_wise_comparison_matrix
        self.normalized_pair_wise_matrix = None
        self.criterial_weights = None
        self.criteria_weighted_sum = None
        self.lambda_i = None
        self.lambda_max = None
        self.consistency_index = None
        self.consistency_ratio = None

    def calculate_normalized_pair_wise_matrix(self):
        """Normalise la matrice de comparaison par paires"""
        column_sums = self.pair_wise_comparison_matrix.sum(axis=0)
        self.normalized_pair_wise_matrix = self.pair_wise_comparison_matrix / column_sums
        return self.normalized_pair_wise_matrix

    def calculate_criterial_weights(self):
        """Calcule les poids des critères"""
        self.criterial_weights = self.normalized_pair_wise_matrix.mean(axis=1)
        return self.criterial_weights

    def calculate_criteria_weighted_sum(self):
        """Calcule la somme pondérée des critères"""
        self.criteria_weighted_sum = (
                                             self.pair_wise_comparison_matrix @ self.criterial_weights) / self.criterial_weights
        return self.criteria_weighted_sum

    def calculate_lambda_max(self):
        """Calcule la valeur propre maximale"""
        self.lambda_max = self.criteria_weighted_sum.mean()
        return self.lambda_max

    def calculate_consistency_index(self):
        """Calcule l'indice de cohérence"""
        n = len(self.criterial_weights)
        self.consistency_index = (self.lambda_max - n) / (n - 1)
        return self.consistency_index

    def calculate_consistency_ratio(self):
        """Calcule le ratio de cohérence"""
        ri = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
        n = len(self.criterial_weights)
        self.consistency_ratio = self.consistency_index / ri[n - 1] if n <= len(ri) else 0
        return self.consistency_ratio

    def run(self):
        """Exécute l'ensemble du processus AHP"""
        self.calculate_normalized_pair_wise_matrix()
        self.calculate_criterial_weights()
        self.calculate_criteria_weighted_sum()
        self.calculate_lambda_max()
        self.calculate_consistency_index()
        self.calculate_consistency_ratio()
        return self


# Fonction pour calculer le score du meilleur candidat associé à une matrice AHP.
# Ici, on applique les poids calculés aux scores des candidats.
def candidate_score(weights, candidates):
    weighted_scores = candidates * weights  # Broadcasting : chaque critère est multiplié par son poids
    total_scores = weighted_scores.sum(axis=1)
    return total_scores.max()  # On souhaite maximiser ce score


###############################################################################
# Implémentation NSGA-II pour optimiser la matrice AHP en considérant deux objectifs
###############################################################################
def dominates(obj1, obj2):
    """
    Renvoie True si obj1 domine obj2.
    Un vecteur d'objectifs obj1 domine obj2 si :
      - Pour chaque objectif, obj1 <= obj2
      - Et il existe au moins un objectif strictement inférieur.
    """
    return all(o1 <= o2 for o1, o2 in zip(obj1, obj2)) and any(o1 < o2 for o1, o2 in zip(obj1, obj2))


def non_dominated_sort(population_objs):
    """
    Effectue le tri non-dominé de la population.
    population_objs: list of tuples (obj1, obj2) pour chaque individu.
    Retourne une liste de fronts, chaque front étant une liste d'indices.
    """
    S = [[] for _ in range(len(population_objs))]
    n = [0] * len(population_objs)
    rank = [0] * len(population_objs)
    fronts = [[]]

    for p in range(len(population_objs)):
        for q in range(len(population_objs)):
            if dominates(population_objs[p], population_objs[q]):
                S[p].append(q)
            elif dominates(population_objs[q], population_objs[p]):
                n[p] += 1
        if n[p] == 0:
            rank[p] = 0
            fronts[0].append(p)
    i = 0
    while fronts[i]:
        next_front = []
        for p in fronts[i]:
            for q in S[p]:
                n[q] -= 1
                if n[q] == 0:
                    rank[q] = i + 1
                    next_front.append(q)
        i += 1
        fronts.append(next_front)
    fronts.pop()  # retirer le dernier front vide
    return fronts


def calculate_crowding_distance(front, population_objs):
    """
    Calcule la distance de crowding pour un front donné.
    front: liste d'indices
    population_objs: liste d'objectifs pour chaque individu
    Retourne un dictionnaire {indice: distance}
    """
    distance = {i: 0 for i in front}
    num_objectives = len(population_objs[0])
    for m in range(num_objectives):
        front_sorted = sorted(front, key=lambda i: population_objs[i][m])
        distance[front_sorted[0]] = float('inf')
        distance[front_sorted[-1]] = float('inf')
        obj_min = population_objs[front_sorted[0]][m]
        obj_max = population_objs[front_sorted[-1]][m]
        if obj_max - obj_min == 0:
            continue
        for i in range(1, len(front_sorted) - 1):
            distance[front_sorted[i]] += (population_objs[front_sorted[i + 1]][m] -
                                          population_objs[front_sorted[i - 1]][m]) / (obj_max - obj_min)
    return distance


class NSGAII_AHPOptimizer:
    """Optimiseur de matrice AHP par NSGA-II (multi-objectifs)"""

    def __init__(self, candidates_matrix, population_size=100, generations=200,
                 mutation_rate=0.3, archive_capacity=50):
        """
        Paramètres modifiés pour une meilleure exploration :
        - population_size augmentée
        - generations augmentées
        - mutation_rate augmentée
        - archive_capacity augmentée
        """
        self.population = None
        self.candidates = candidates_matrix
        self.pop_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.n_criteria = candidates_matrix.shape[1]
        self.scale = [1/9, 1/7, 1/5, 1/3, 1, 3, 5, 7, 9]
        self.archive_capacity = archive_capacity
        self.archive = []

    def _generate_individual(self):
        """Génération dirigée vers des matrices cohérentes"""
        size = self.n_criteria
        matrix = np.ones((size, size))
        hierarchy = np.random.permutation(size)  # Hiérarchie aléatoire

        for i in range(size):
            for j in range(i + 1, size):
                if hierarchy[i] > hierarchy[j]:
                    val = np.random.choice([3, 5, 7, 9])
                else:
                    val = 1 / np.random.choice([3, 5, 7, 9])
                matrix[i, j] = val
                matrix[j, i] = 1 / val
        return matrix

    def _mutate(self, individual):
        """Mutation plus exploratoire avec perturbations aléatoires"""
        mutant = individual.copy()
        for i in range(individual.shape[0]):
            for j in range(i + 1, individual.shape[1]):
                if np.random.rand() < self.mutation_rate:
                    # 30% de chance de mutation forte
                    if np.random.rand() < 0.73:
                        new_val = np.random.choice([1 / 9, 1 / 7, 9, 7])
                    else:
                        new_val = np.random.choice(self.scale)
                    mutant[i, j] = new_val
                    mutant[j, i] = 1 / new_val
        return mutant

    def _crossover(self, parent1, parent2):
        """Croisement de deux matrices"""
        child = parent1.copy()
        mask = np.random.rand(*parent1.shape) < 0.5
        child[mask] = parent2[mask]
        return child

    def _select_final_solution(self):
        """Sélection finale avec compromis personnalisé"""
        candidates = self.archive + self.population
        objs = np.array([self.evaluate_objectives(ind) for ind in candidates])

        # Normalisation des objectifs
        norm_objs = (objs - np.min(objs, axis=0)) / (np.max(objs, axis=0) - np.min(objs, axis=0) + 1e-6)

        # Score composite avec priorité sur CR
        scores = 0.6 * (1 - norm_objs[:, 0]) + 0.4 * (1 - norm_objs[:, 1])

        best_idx = np.argmax(scores)
        return candidates[best_idx], objs[best_idx]

    def evaluate_objectives(self, individual):
        """
        Calcule le vecteur d'objectifs pour une matrice.
        Objectif 1: Ratio de cohérence (à minimiser)
        Objectif 2: - score du meilleur candidat (pour maximiser ce score)
        """
        try:
            ahp = AHP(individual).run()
            obj1 = ahp.consistency_ratio  # à minimiser
            # Calculer le score du meilleur candidat associé
            weighted_scores = self.candidates * ahp.criterial_weights  # diffusion
            total_scores = weighted_scores.sum(axis=1)
            best_score = total_scores.max()
            obj2 = -best_score  # on veut maximiser le score, donc minimiser son opposé
            return (obj1, obj2)
        except Exception as e:
            return (float('inf'), float('inf'))

    def optimize(self):
        """Exécute NSGA-II pour optimiser la matrice AHP"""
        # Génération initiale
        population = [self._generate_individual() for _ in range(self.pop_size)]

        for gen in range(self.generations):
            # Évaluation des objectifs pour chaque individu
            pop_objs = [self.evaluate_objectives(ind) for ind in population]

            # Tri non-dominé
            fronts = non_dominated_sort(pop_objs)
            # Calcul des distances de crowding pour chaque front
            crowding = {}
            for front in fronts:
                distances = calculate_crowding_distance(front, pop_objs)
                for i in front:
                    crowding[i] = distances[i]

            # Sélection NSGA-II : on combine le front et la distance de crowding pour trier
            indices = list(range(len(population)))
            # Trier d'abord par rang (le front dans lequel se trouve l'individu), puis par distance de crowding décroissante
            ranks = {}
            for rank_idx, front in enumerate(fronts):
                for i in front:
                    ranks[i] = rank_idx
            sorted_indices = sorted(indices, key=lambda i: (ranks[i], -crowding[i]))
            # Sélectionner les meilleurs individus pour constituer la nouvelle population
            new_population = [population[i] for i in sorted_indices[:self.pop_size]]

            # Création d'une population d'enfants par crossover et mutation
            offspring = []
            while len(offspring) < self.pop_size:
                # Sélectionner les indices des parents d'abord
                parent_indices = np.random.choice(range(len(new_population)), 2, replace=False)
                # Puis récupérer les parents correspondants
                parent1 = new_population[parent_indices[0]]
                parent2 = new_population[parent_indices[1]]
                # Faire le croisement et la mutation
                child = self._crossover(parent1, parent2)
                child = self._mutate(child)
                offspring.append(child)
            # Nouvelle population : mélange de la population sélectionnée et des enfants
            population = new_population + offspring
            # Limiter la population à self.pop_size
            population = population[:self.pop_size]
            self.archive = self._filter_pareto_front(self.archive + population,
                                                     self.archive_capacity)

            if gen % 20 == 0 and len(self.archive) > 10:
                # Réinitialisation partielle pour éviter la stagnation
                population.extend(random.sample(self.archive, 5))
        self.population = population
        # Après évolution, retourner le meilleur individu selon une agrégation (par exemple, premier individu du front non dominé)
        # final_objs = [self.evaluate_objectives(ind) for ind in population]
        # final_fronts = non_dominated_sort(final_objs)
        # best_index = final_fronts[0][0]
        # best_matrix = population[best_index]
        # best_objectives = final_objs[best_index]
        # self.archive.extend(population)
        # self.archive = self._filter_pareto_front(self.archive)
        return self._select_final_solution()

    def _filter_pareto_front(self, pop, max_capacity=50):
        """
        Filtre les solutions pour garder un front de Pareto diversifié
        avec une capacité maximale spécifiée.

        Args:
            pop: Liste des solutions candidates
            max_capacity: Nombre maximum de solutions à conserver

        Returns:
            Liste des solutions filtrées et triées
        """
        # Évaluation des objectifs pour toutes les solutions
        pop_objs = [self.evaluate_objectives(ind) for ind in pop]

        # Tri non dominé
        fronts = non_dominated_sort(pop_objs)

        filtered = []
        current_count = 0

        # Parcours des fronts successifs
        for front in fronts:
            front_indices = front
            front_size = len(front_indices)

            # Vérifie si on peut ajouter tout le front
            if current_count + front_size <= max_capacity:
                filtered.extend([pop[i] for i in front_indices])
                current_count += front_size
            else:
                # Sélection partielle du front avec distance de crowding
                remaining = max_capacity - current_count
                crowding = calculate_crowding_distance(front_indices, pop_objs)

                # Tri par distance de crowding décroissante
                sorted_front = sorted(front_indices,
                                      key=lambda i: crowding[i],
                                      reverse=True)

                filtered.extend([pop[i] for i in sorted_front[:remaining]])
                break

        return filtered[:max_capacity]


###############################################################################
# Exemple d'utilisation
###############################################################################
def generate_candidates(num_candidates):
    """Génère une matrice de scores aléatoires pour num_candidates candidats (6 critères)"""
    return np.random.randint(1, 11, size=(num_candidates, 6))


def get_best_candidates(optimized_matrix, candidates_scores, top_n=5):
    """
    Retourne les meilleurs candidats classés en utilisant la matrice optimisée

    Args:
        optimized_matrix (np.array): Matrice AHP optimisée
        candidates_scores (np.array): Matrice des scores des candidats
        top_n (int): Nombre de candidats à retourner

    Returns:
        list: Liste triée des indices des candidats (meilleur en premier)
    """
    ahp = AHP(optimized_matrix).run()
    weights = ahp.criterial_weights

    # Calcul des scores pondérés
    weighted_scores = candidates_scores * weights
    total_scores = weighted_scores.sum(axis=1)

    # Tri des indices par score décroissant
    sorted_indices = np.argsort(total_scores)[::-1]

    return sorted_indices[:top_n]


# Configuration des données
import numpy as np

if __name__ == "__main__":
    # Génération de 200 candidats
    candidates_scores = generate_candidates(20)
    print("Exemple des 10 premiers candidats:")
    print(candidates_scores[:10])

    # Création de l'optimiseur NSGA-II
    optimizer = NSGAII_AHPOptimizer(
        candidates_matrix=candidates_scores,
        population_size=100,
        generations=40,
        mutation_rate=0.3,
        archive_capacity=100
    )

    # Exécution de l'optimisation
    best_matrix, best_objectives = optimizer.optimize()
    print("\n=== Résultats NSGA-II ===")
    print(f"Meilleure matrice trouvée (CR = {best_objectives[0]:.3f}, Score candidat = {-best_objectives[1]:.3f}):")
    print(best_matrix.round(3))

    # Récupération du meilleur candidat
    final_best_index = get_best_candidates(best_matrix, candidates_scores, 50)

    # Affichage détaillé
    print("\n=== Résultats Finaux ===")
    print(f"- Meilleur candidat index: {final_best_index}")
    # Add 1 to display the ID
    print(f"- Meilleur candidat ID: {[i + 1 for i in final_best_index]}")

    # Détails des calculs
    ahp = AHP(best_matrix).run()
