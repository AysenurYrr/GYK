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
    SELECT s.supplier_id,
           COUNT(p.product_id) AS product_count,
           SUM(od.quantity) AS total_sales_quantity,
           AVG(od.unit_price) AS avg_price,
           AVG(sub.customer_count) AS avg_customer_count
    FROM Suppliers s
    JOIN Products p ON s.supplier_id = p.supplier_id
    JOIN order_details od ON p.product_id = od.product_id
    JOIN (
        SELECT od.product_id, COUNT(DISTINCT o.customer_id) AS customer_count
        FROM order_details od
        JOIN Orders o ON od.order_id = o.order_id
        GROUP BY od.product_id
    ) sub ON sub.product_id = p.product_id
    GROUP BY s.supplier_id
    """

df = pd.read_sql_query(query, con=engine)
print(df.head()) 

X = df[['product_count', 'total_sales_quantity', 'avg_price', 'avg_customer_count']]


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

optimal_eps = find_optimal_eps(X_scaled)


min_samples_range = range(3, 11) 
best_min_samples, best_score, best_clusters = grid_search_min_samples(X_scaled, optimal_eps, min_samples_range)
print(f"Best min_samples: {best_min_samples}")
print(f"Best silhouette score: {best_score}")


dbscan = DBSCAN(eps=optimal_eps, min_samples=best_min_samples)
df["cluster"] = dbscan.fit_predict(X_scaled)   

# PCA uygulama ve veriyi 2 bileşene indirgeme (görselleştirme için)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# PCA ile elde edilen 2 bileşeni DataFrame'e ekleme
df['pca1'] = X_pca[:, 0]
df['pca2'] = X_pca[:, 1]

# Outlierları (cluster == -1) belirleme
outliers = df[df['cluster'] == -1]

# Kümeleme sonucu görselleştirme
plt.figure(figsize=(10, 6))
plt.scatter(df['pca2'], df['pca1'], c=df['cluster'], cmap='plasma', s=60)
plt.xlabel("PCA Bileşeni 2")
plt.ylabel("PCA Bileşeni 1")
plt.title("Tedarikçi Performansı (PCA ve DBSCAN)")
plt.grid(True)
plt.colorbar(label='Cluster Number')

# Outlierları kırmızı renkte işaretleme
plt.scatter(outliers['pca1'], outliers['pca2'], color='red', s=100, edgecolor='black', label='Outliers')
plt.legend()

plt.show()

# Outlierları incelemek
print("Outlier Tedarikçiler:")
print(outliers)