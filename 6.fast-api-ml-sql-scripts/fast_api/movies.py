from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from typing import List

router = APIRouter()

# JSON dosyasının yolu
MOVIES_FILE = "c:\\Users\\bilgisayar\\Desktop\\repositorys\\GYK\\6\\database\\movies.json"

# Film modeli
class Movie(BaseModel):
    movie_id: int
    title: str
    category_id: int
    genre_ids: List[int]
    imdb_rating: float
    release_year: int
    duration_minutes: int
    description: str

# Tüm filmleri getir
@router.get("/movies", response_model=List[Movie])
def get_movies():
    with open(MOVIES_FILE, "r") as file:
        movies = json.load(file)
    return movies

# Yeni bir film ekle
@router.post("/movies")
def add_movie(movie: Movie):
    with open(MOVIES_FILE, "r") as file:
        movies = json.load(file)
    
    # Aynı movie_id'ye sahip bir film varsa hata döndür
    for m in movies:
        if m["movie_id"] == movie.movie_id:
            raise HTTPException(status_code=400, detail="Movie with this ID already exists.")
    
    # Yeni filmi ekle
    movies.append(movie.dict())
    with open(MOVIES_FILE, "w") as file:
        json.dump(movies, file, indent=4)
    
    return {"message": "Movie added successfully"}
