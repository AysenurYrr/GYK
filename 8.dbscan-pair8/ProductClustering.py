# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from FindOptimalEPS import find_optimal_eps
from Database import engine
from sklearn.metrics import silhouette_score
from GridSearch import grid_search_min_samples
from sklearn.decomposition import PCA
# SQL query to fetch product sales data


query = """
SELECT 
    p.product_id,
    AVG(od.unit_price) AS avg_price,
    COUNT(od.order_id) AS sales_count,
    AVG(od.quantity) AS avg_quantity_per_order,
    COUNT(DISTINCT o.customer_id) AS customer_count
FROM products p
JOIN order_details od ON p.product_id = od.product_id
JOIN orders o ON o.order_id = od.order_id
GROUP BY p.product_id
"""

df = pd.read_sql_query(query, con=engine)
print(df.head()) 

X = df[["avg_price", "sales_count", "avg_quantity_per_order", "customer_count"]]


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

optimal_eps = find_optimal_eps(X_scaled)


min_samples_range = range(3, 11) 
best_min_samples, best_score, best_clusters = grid_search_min_samples(X_scaled, optimal_eps, min_samples_range)
print(f"Best min_samples: {best_min_samples}")
print(f"Best silhouette score: {best_score}")


dbscan = DBSCAN(eps=optimal_eps, min_samples=best_min_samples)
df["cluster"] = dbscan.fit_predict(X_scaled)  


# PCA application and reducing data to 2 components (for visualization)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

df['pca1'] = X_pca[:, 0]
df['pca2'] = X_pca[:, 1]

outliers = df[df['cluster'] == -1]

plt.figure(figsize=(10, 6))
plt.scatter(df['pca2'], df['pca1'], c=df['cluster'], cmap='plasma', s=60)
plt.xlabel("PCA Component 2")
plt.ylabel("PCA Component 1")
plt.title("Product Performance (PCA and DBSCAN)")
plt.grid(True)
plt.colorbar(label='Cluster Number')

plt.scatter(outliers['pca1'], outliers['pca2'], color='red', s=100, edgecolor='black', label='Outliers')
plt.legend()
plt.show()

print("Outlier Suppliers:")
print(outliers)

   


