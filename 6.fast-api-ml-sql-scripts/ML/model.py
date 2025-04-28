import pandas as pd
import ast
from sklearn.cluster import KMeans

# CSV dosyasını oku
df = pd.read_csv("prepared_data.csv", converters={"genre_ids": ast.literal_eval})

# Kullanıcı-tür (genre) matrisini oluştur
def create_user_genre_matrix(df):
    rows = []
    for _, row in df.iterrows():
        for genre in row["genre_ids"]:
            rows.append({
                "user_id": row["user_id"],
                f"genre_{genre}": row["rating"]
            })
    genre_df = pd.DataFrame(rows)
    user_genre_matrix = genre_df.groupby("user_id").mean().fillna(0)
    return user_genre_matrix

# Kullanıcıları k-means ile kümele
def cluster_users(user_genre_matrix, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    user_genre_matrix["cluster"] = kmeans.fit_predict(user_genre_matrix)
    return user_genre_matrix, kmeans

# Öneri üret
def recommend_for_user(user_id, df, user_clusters, top_n=3):
    # Kullanıcı veri setinde yoksa
    if user_id not in user_clusters.index:
        print(f"Kullanıcı {user_id} hiç film izlememiş. En yüksek IMDb puanlı filmler öneriliyor.")
        all_movies = df.drop_duplicates("movie_id")
        return (
            all_movies[["movie_id", "title", "imdb_rating"]]
            .sort_values("imdb_rating", ascending=False)
            .head(top_n)
        )

    # Kümesi bul
    user_cluster = user_clusters.loc[user_id, "cluster"]
    cluster_user_ids = user_clusters[user_clusters["cluster"] == user_cluster].index.tolist()

    # Aynı kümedeki kullanıcıların verisi
    cluster_df = df[df["user_id"].isin(cluster_user_ids)]

    # Kullanıcının izlediği filmleri çıkar
    watched = set(df[df["user_id"] == user_id]["movie_id"])
    candidates = cluster_df[~cluster_df["movie_id"].isin(watched)]

    # Eğer önerilecek film yoksa fallback ver
    if candidates.empty:
        print(f"Kullanıcı {user_id} için kümesinde yeni öneri yok. En yüksek IMDb puanlı filmler öneriliyor.")
        all_movies = df.drop_duplicates("movie_id")
        return (
            all_movies[~all_movies["movie_id"].isin(watched)][["movie_id", "title", "imdb_rating"]]
            .sort_values("imdb_rating", ascending=False)
            .head(top_n)
        )

    # Ortalama puanlara göre öneri yap
    recommendations = (
        candidates.groupby(["movie_id", "title"])
        .agg({"rating": "mean", "imdb_rating": "first"})
        .sort_values("rating", ascending=False)
        .reset_index()
        .head(top_n)
    )
    return recommendations

# === Ana akış ===
if __name__ == "__main__":
    user_genre_matrix = create_user_genre_matrix(df)
    user_clusters, kmeans = cluster_users(user_genre_matrix.copy(), n_clusters=2)

    # Kullanıcı örnekleri:
    for uid in range(1, 7):  # kullanıcı 6 henüz hiç film izlememiş gibi düşün
        print(f"\n🎬 Öneriler - Kullanıcı {uid}")
        print(recommend_for_user(uid, df, user_clusters))
