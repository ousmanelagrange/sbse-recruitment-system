import random
import numpy as np

class GeneticAlgorithm:
    def __init__(self, applications, population_size=100, generations=50, mutation_rate=0.1):
        """
        Initialise l'algorithme génétique pour optimiser les candidatures.
        """
        self.applications = applications
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = self._initial_population()

    def _initial_population(self):
        """
        Crée la population initiale des candidatures (c'est-à-dire une population d'individus) 
        basée sur les candidatures existantes.
        """
        population = []
        for _ in range(self.population_size):
            individual = [random.uniform(0, 1) for _ in range(len(self.applications))]
            population.append(individual)
        return population

    def _fitness(self, individual):
        """
        Calcule le fitness d'un individu dans la population, basé sur les scores AHP.
        """
        fitness = 0
        for idx, score in enumerate(individual):
            fitness += score * self.applications[idx].score_ahp  # Pondération par le score AHP
        return fitness

    def _select_parents(self):
        """
        Sélectionne deux parents pour la reproduction en utilisant un tournoi.
        """
        parents = random.sample(self.population, 2)
        return max(parents, key=self._fitness)

    def _crossover(self, parent1, parent2):
        """
        Croisement entre deux parents pour produire un enfant.
        """
        crossover_point = random.randint(1, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child

    def _mutate(self, individual):
        """
        Applique une mutation sur un individu avec une certaine probabilité.
        """
        if random.random() < self.mutation_rate:
            mutation_point = random.randint(0, len(individual) - 1)
            individual[mutation_point] = random.uniform(0, 1)
        return individual

    def run(self):
        """
        Exécute l'algorithme génétique.
        """
        for generation in range(self.generations):
            new_population = []
            for _ in range(self.population_size // 2):
                parent1 = self._select_parents()
                parent2 = self._select_parents()
                child1 = self._crossover(parent1, parent2)
                child2 = self._crossover(parent2, parent1)
                new_population.append(self._mutate(child1))
                new_population.append(self._mutate(child2))
            self.population = new_population

        # Applique les résultats de l'algorithme génétique aux candidatures
        for idx, individual in enumerate(self.population):
            self.applications[idx].score_ga = self._fitness(individual)
            self.applications[idx].save()

