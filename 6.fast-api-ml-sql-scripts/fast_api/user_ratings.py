from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from typing import List

router = APIRouter()

# JSON dosyasının yolu
USER_RATINGS_FILE = "c:\\Users\\bilgisayar\\Desktop\\repositorys\\GYK\\6\\database\\user_ratings.json"

# Puan modeli
class Rating(BaseModel):
    user_id: int
    movie_id: int
    rating: float

# Tüm puanları getir
@router.get("/ratings", response_model=List[Rating])
def get_ratings():
    with open(USER_RATINGS_FILE, "r") as file:
        ratings = json.load(file)
    return ratings

# Yeni bir puan ekle
@router.post("/ratings")
def add_rating(rating: Rating):
    with open(USER_RATINGS_FILE, "r") as file:
        ratings = json.load(file)

    # Aynı kullanıcı ve film için zaten bir puan varsa hata döndür
    for r in ratings:
        if r["user_id"] == rating.user_id and r["movie_id"] == rating.movie_id:
            raise HTTPException(status_code=400, detail="Rating already exists for this user and movie.")
    
    # Yeni puanı ekle
    ratings.append(rating.dict())
    with open(USER_RATINGS_FILE, "w") as file:
        json.dump(ratings, file, indent=4)
    
    return {"message": "Rating added successfully"}
