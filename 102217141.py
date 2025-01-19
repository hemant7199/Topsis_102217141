# -*- coding: utf-8 -*-
"""102217141.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KF7-Bs161mVxxZEte-6armIwn41nWM2f
"""

import numpy as np
import pandas as pd

def create_eval_mat(mat):
    mat = mat[:, 1:]  # Remove the first column
    return mat


def create_normalised_matrix(mat, weight):
    column_squared_sum = np.zeros(mat.shape[1])  # Initialize column squared sums
    for j in range(mat.shape[1]):
        for i in range(mat.shape[0]):
            column_squared_sum[j] += mat[i][j] * mat[i][j]
        column_squared_sum[j] = np.sqrt(column_squared_sum[j])
        mat[:, j] = mat[:, j] / column_squared_sum[j]  # Normalize the matrix
    return weighted_normalised_matrix(mat, weight=np.asarray(weight))

def weighted_normalised_matrix(mat, weight):
    total_weight = np.sum(weight)
    if total_weight == 0:
        raise ValueError("The sum of weights cannot be zero.")
    weight = weight / total_weight  # Normalize weights
    weighted_normalised_matrix = mat * weight
    return weighted_normalised_matrix

def calculate_ideal_best_and_ideal_worst(weighted_normalised_mat, is_max_the_most_desired):
    ideal_best = np.zeros(weighted_normalised_mat.shape[1])
    ideal_worst = np.zeros(weighted_normalised_mat.shape[1])
    for j in range(weighted_normalised_mat.shape[1]):
        if is_max_the_most_desired[j] == 1:
            ideal_best[j] = np.max(weighted_normalised_mat[:, j])
            ideal_worst[j] = np.min(weighted_normalised_mat[:, j])
        else:
            ideal_worst[j] = np.max(weighted_normalised_mat[:, j])
            ideal_best[j] = np.min(weighted_normalised_mat[:, j])
    return euclidean_distance_from_ideal_best_and_ideal_worst_for_each_alternative(weighted_normalised_mat, ideal_best, ideal_worst)

def euclidean_distance_from_ideal_best_and_ideal_worst_for_each_alternative(mat, ideal_best, ideal_worst):
    euclidean_distance_from_ideal_best = np.zeros(mat.shape[0])
    euclidean_distance_from_ideal_worst = np.zeros(mat.shape[0])
    for i in range(mat.shape[0]):
        each_row_best = 0
        each_row_worst = 0
        for j in range(mat.shape[1]):
            each_row_best += (mat[i][j] - ideal_best[j]) ** 2
            each_row_worst += (mat[i][j] - ideal_worst[j]) ** 2
        euclidean_distance_from_ideal_best[i] = np.sqrt(each_row_best)
        euclidean_distance_from_ideal_worst[i] = np.sqrt(each_row_worst)
    return performance_score(mat, euclidean_distance_from_ideal_best, euclidean_distance_from_ideal_worst)

def performance_score(mat, euclidean_best, euclidean_worst):
    performance = np.zeros(mat.shape[0])
    for i in range(mat.shape[0]):
        performance[i] = euclidean_worst[i] / (euclidean_best[i] + euclidean_worst[i])
    return performance

# Load the uploaded dataset and define inputs

file_path = '/content/102217141-data.csv'
data = pd.read_csv(file_path)


# Define weights and impacts for the criteria
weights = [1, 1, 1, 1, 1, 1, 1]
impacts = [1, 1, 0, 1, 1, 1, 1]

# Prepare the matrix
mat = data.values
mat = create_eval_mat(mat)
weighted_normalised_matrix = create_normalised_matrix(mat, weights)
performance = calculate_ideal_best_and_ideal_worst(weighted_normalised_matrix, np.asarray(impacts))

# Calculate ranks
performance_list = list(performance)
ranks = [sorted(performance_list, reverse=True).index(x) + 1 for x in performance_list]

# Display results
results = pd.DataFrame(data, columns=['Fund Name', 'P1', 'P2', 'P3', 'P4', 'P5'])
results['Topsis Score'] = performance
results['Rank'] = ranks

print(results)