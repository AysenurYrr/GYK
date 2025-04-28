import pandas as pd
from sklearn.cluster import KMeans
from sqlalchemy.orm import Session
from models import User, Movie, Rating

CLUSTERS = 10


def get_recommendations(db: Session, user_id: int, k: int = 5):
    # Load ratings into DataFrame
    ratings = db.query(Rating).all()
    df = pd.DataFrame([
        {'user_id': r.user_id, 'movie_id': r.movie_id, 'score': r.score}
        for r in ratings
    ])

    # Pivot to user-item matrix
    user_item = df.pivot(index='user_id', columns='movie_id', values='score').fillna(0)

    # Cluster users
    kmeans = KMeans(n_clusters=CLUSTERS, random_state=42)
    user_item['cluster'] = kmeans.fit_predict(user_item)

    # Get target user's cluster
    cluster_label = user_item.loc[user_id, 'cluster']

    # Find users in same cluster
    cluster_users = user_item[user_item['cluster'] == cluster_label].index

    # Compute average scores for movies among cluster
    cluster_ratings = df[df['user_id'].isin(cluster_users)]
    avg_scores = cluster_ratings.groupby('movie_id')['score'].mean()

    # Exclude movies already rated by target user
    watched = set(df[df['user_id'] == user_id]['movie_id'])
    recommendations = (
        avg_scores[~avg_scores.index.isin(watched)]
        .sort_values(ascending=False)
        .head(k)
        .index.tolist()
    )

    # Fetch movie details
    movies = db.query(Movie).filter(Movie.id.in_(recommendations)).all()
    return movies