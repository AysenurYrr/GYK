from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from typing import List

router = APIRouter()

# JSON dosyasının yolu
GENRES_FILE = "c:\\Users\\bilgisayar\\Desktop\\repositorys\\GYK\\6\\database\\genres.json"

# Tür modeli
class Genre(BaseModel):
    genre_id: int
    name: str

# Tüm türleri getir
@router.get("/genres", response_model=List[Genre])
def get_genres():
    with open(GENRES_FILE, "r") as file:
        genres = json.load(file)
    return genres

# Yeni bir tür ekle
@router.post("/genres")
def add_genre(genre: Genre):
    with open(GENRES_FILE, "r") as file:
        genres = json.load(file)
    
    # Aynı genre_id'ye sahip bir tür varsa hata döndür
    for g in genres:
        if g["genre_id"] == genre.genre_id:
            raise HTTPException(status_code=400, detail="Genre with this ID already exists.")
    
    # Yeni türü ekle
    genres.append(genre.dict())
    with open(GENRES_FILE, "w") as file:
        json.dump(genres, file, indent=4)
    
    return {"message": "Genre added successfully"}
