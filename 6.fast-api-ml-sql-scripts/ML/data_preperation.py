import requests
import pandas as pd

# FastAPI'den verileri çekmek için URL'ler
BASE_URL = "http://127.0.0.1:8000"
ENDPOINTS = {
    "categories": f"{BASE_URL}/categories",
    "genres": f"{BASE_URL}/genres",
    "movies": f"{BASE_URL}/movies",
    "users": f"{BASE_URL}/users",
    "user_ratings": f"{BASE_URL}/user_ratings",
}

def fetch_data():
    """FastAPI'den verileri çek."""
    data = {}
    for key, url in ENDPOINTS.items():
        try:
            response = requests.get(url)
            response.raise_for_status()  # Hata durumunda exception fırlatır
            data[key] = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {key} data: {e}")
            data[key] = []  # Hata durumunda boş bir liste döndür
    return data

def prepare_data(data):
    """Verileri birleştir ve modeli eğitmek için hazırla."""
    try:
        # Movies ve User Ratings verilerini birleştir
        movies_df = pd.DataFrame(data["movies"])
        ratings_df = pd.DataFrame(data["user_ratings"])
        users_df = pd.DataFrame(data["users"])

        # Kullanıcıların izlediği filmleri ve puanlarını birleştir
        merged_df = ratings_df.merge(movies_df, on="movie_id", how="left")
        merged_df = merged_df.merge(users_df[["user_id", "username"]], on="user_id", how="left")

        # Gerekli sütunları seç
        prepared_df = merged_df[["user_id", "username", "movie_id", "title", "rating", "genre_ids", "imdb_rating"]]

        # Eksik verileri kontrol et ve temizle
        prepared_df = prepared_df.dropna()

        return prepared_df
    except KeyError as e:
        print(f"KeyError during data preparation: {e}")
        return pd.DataFrame()  # Hata durumunda boş bir DataFrame döndür

if __name__ == "__main__":
    # Verileri çek
    data = fetch_data()

    # Verileri hazırla
    prepared_data = prepare_data(data)

    if not prepared_data.empty:
        # Hazırlanan veriyi CSV olarak kaydet
        prepared_data.to_csv("prepared_data.csv", index=False)
        print("Data preparation completed. Saved to 'prepared_data.csv'.")
    else:
        print("Data preparation failed. No data to save.")