# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import numpy as np

# Define the grid search function for min_samples optimization
def grid_search_min_samples(X_scaled, eps, min_samples_range):
    best_score = -np.inf
    best_min_samples = None
    best_clusters = None

    for min_samples in min_samples_range:
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        clusters = dbscan.fit_predict(X_scaled)

        # Calculate silhouette score only if there is more than 1 cluster (excluding noise)
        if len(set(clusters)) > 1:  # Ensure there are more than one cluster
            score = silhouette_score(X_scaled, clusters)
            if score > best_score:
                best_score = score
                best_min_samples = min_samples
                best_clusters = clusters

    return best_min_samples, best_score, best_clusters