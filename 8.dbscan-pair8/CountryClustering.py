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
    SELECT c.country,
           COUNT(o.order_id) AS total_orders,
           AVG(od.unit_price * od.quantity) AS avg_order_value,
           AVG(order_size.product_count) AS avg_products_per_order
    FROM Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    JOIN order_details od ON o.order_id = od.order_id
    JOIN (
        SELECT od.order_id, COUNT(od.product_id) AS product_count
        FROM order_details od
        GROUP BY od.order_id
    ) order_size ON order_size.order_id = o.order_id
    GROUP BY c.country
    """

df = pd.read_sql_query(query, con=engine)
print(df.head()) 

X = df[['total_orders', 'avg_order_value', 'avg_products_per_order']]


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
plt.title("Supplier Performance (PCA and DBSCAN)")
plt.grid(True)
plt.colorbar(label='Cluster Number')

plt.scatter(outliers['pca1'], outliers['pca2'], color='red', s=100, edgecolor='black', label='Outliers')
plt.legend()
plt.show()

print("Outlier Suppliers:")
print(outliers)