import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator

# Function to find the optimal eps value for DBSCAN
def find_optimal_eps(X_scaled, min_samples=5):

    neighbors = NearestNeighbors(n_neighbors=min_samples).fit(X_scaled)
    distances, _ = neighbors.kneighbors(X_scaled)
    
    distances = np.sort(distances[:, min_samples-1])
    
    knee = KneeLocator(range(len(distances)), distances, curve="convex", direction="increasing")
    optimal_eps = distances[knee.elbow]
    
    plt.figure(figsize=(10, 6))
    plt.plot(distances)
    plt.axvline(x=knee.elbow, color='r', linestyle='--', label=f'Optimal eps: {optimal_eps:.2f}')
    plt.xlabel('Points sorted by distance')
    plt.ylabel(f'{min_samples}-th nearest neighbor distance')
    plt.title('Elbow Method for Optimal eps')
    plt.legend()
    plt.grid(True)
    plt.show()

    return optimal_eps