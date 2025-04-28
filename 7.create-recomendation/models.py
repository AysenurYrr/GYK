from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Association table for Movie <-> Genre many-to-many
movie_genre = Table(
    'movie_genre', Base.metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', ForeignKey('genres.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ratings = relationship('Rating', back_populates='user')

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    imdb_rating = Column(Float)
    genres = relationship('Genre', secondary=movie_genre, back_populates='movies')
    ratings = relationship('Rating', back_populates='movie')

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    movies = relationship('Movie', secondary=movie_genre, back_populates='genres')

class Rating(Base):
    __tablename__ = 'ratings'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), primary_key=True)
    score = Column(Float, nullable=False)

    user = relationship('User', back_populates='ratings')
    movie = relationship('Movie', back_populates='ratings')