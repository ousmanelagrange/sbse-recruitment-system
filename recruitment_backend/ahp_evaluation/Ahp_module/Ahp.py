import random
#
import numpy as np

class AHP:
    def __init__(self, pair_wise_comparison_matrix):
        self.pair_wise_comparison_matrix = pair_wise_comparison_matrix
        self.normalized_pair_wise_matrix = None
        self.criterial_weights = None
        self.criteria_weighted_sum = None
        self.lambda_max = None
        self.consistency_index = None
        self.consistency_ratio = None

    def calculate_normalized_pair_wise_matrix(self):
        col_sums = self.pair_wise_comparison_matrix.sum(axis=0)
        self.normalized_pair_wise_matrix = self.pair_wise_comparison_matrix / col_sums
        return self.normalized_pair_wise_matrix

    def calculate_criterial_weights(self):
        self.criterial_weights = self.normalized_pair_wise_matrix.mean(axis=1)
        return self.criterial_weights

    def calculate_criteria_weighted_sum(self):
        self.criteria_weighted_sum = (
            self.pair_wise_comparison_matrix @ self.criterial_weights
        ) / self.criterial_weights
        return self.criteria_weighted_sum

    def calculate_lambda_max(self):
        self.lambda_max = self.criteria_weighted_sum.mean()
        return self.lambda_max

    def calculate_consistency_index(self):
        n = len(self.criterial_weights)
        self.consistency_index = (self.lambda_max - n) / (n - 1)
        return self.consistency_index

    def calculate_consistency_ratio(self):
        ri = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
        n = len(self.criterial_weights)
        if n - 1 < len(ri):
            self.consistency_ratio = self.consistency_index / ri[n - 1]
        else:
            self.consistency_ratio = None
        return self.consistency_ratio

    def run(self):
        self.calculate_normalized_pair_wise_matrix()
        self.calculate_criterial_weights()
        self.calculate_criteria_weighted_sum()
        self.calculate_lambda_max()
        self.calculate_consistency_index()
        self.calculate_consistency_ratio()
        return self


def candidate_score(weights, candidates):
    weighted = candidates * weights
    return weighted.sum(axis=1)
