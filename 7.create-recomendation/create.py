from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from database import DATABASE_URL, Base
from models import Genre, Movie, User, Rating

# Initialize engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Sample data
genres_data = ["Action", "Comedy", "Drama", "Sci-Fi", "Horror"]
movies_data = [
    {"title": "Interstellar",  "imdb_rating": 8.6, "genres": ["Sci-Fi", "Drama"]},
    {"title": "The Dark Knight", "imdb_rating": 9.0, "genres": ["Action", "Drama"]},
    {"title": "Inception",      "imdb_rating": 8.8, "genres": ["Action", "Sci-Fi"]},
    {"title": "The Hangover",    "imdb_rating": 7.7, "genres": ["Comedy"]},
    {"title": "Get Out",        "imdb_rating": 7.7, "genres": ["Horror", "Drama"]}
]
users_data = [
    {"name": "Alice"},
    {"name": "Bob"},
    {"name": "Charlie"}
]
ratings_data = [
    # Alice ratings
    {"user": "Alice",   "movie": "Interstellar",    "score": 9.0},
    {"user": "Alice",   "movie": "The Dark Knight", "score": 8.5},
    # Bob ratings
    {"user": "Bob",     "movie": "Inception",      "score": 8.0},
    {"user": "Bob",     "movie": "The Hangover",    "score": 7.0},
    {"user": "Bob",     "movie": "Get Out",        "score": 7.5},
    # Charlie ratings
    {"user": "Charlie", "movie": "Interstellar",    "score": 8.5},
    {"user": "Charlie", "movie": "Inception",      "score": 9.0},
    {"user": "Charlie", "movie": "Get Out",        "score": 6.5}
]


def main():
    # Create tables
    Base.metadata.create_all(engine)
    print("Tables created.")

    session = SessionLocal()
    try:
        # Add genres
        genre_objs = {}
        for name in genres_data:
            g = Genre(name=name)
            session.add(g)
            session.flush()
            genre_objs[name] = g

        # Add movies
        movie_objs = {}
        for m in movies_data:
            movie = Movie(title=m["title"], imdb_rating=m["imdb_rating"])
            for gname in m["genres"]:
                movie.genres.append(genre_objs[gname])
            session.add(movie)
            session.flush()
            movie_objs[m["title"]] = movie

        # Add users
        user_objs = {}
        for u in users_data:
            user = User(name=u["name"])
            session.add(user)
            session.flush()
            user_objs[u["name"]] = user

        # Add ratings
        for r in ratings_data:
            rating = Rating(
                user_id=user_objs[r["user"]].id,
                movie_id=movie_objs[r["movie"]].id,
                score=r["score"]
            )
            session.add(rating)

        session.commit()
        print("Sample data populated.")
    except IntegrityError:
        session.rollback()
        print("Data already exists or integrity error.")
    finally:
        session.close()


if __name__ == '__main__':
    main()