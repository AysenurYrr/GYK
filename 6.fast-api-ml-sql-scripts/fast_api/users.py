from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from typing import List

router = APIRouter()

# JSON dosyasının yolu
USERS_FILE = "c:\\Users\\bilgisayar\\Desktop\\repositorys\\GYK\\6\\database\\users.json"

# Kullanıcı modeli
class User(BaseModel):
    user_id: int
    username: str
    email: str
    watched_movies: List[int]

# Tüm kullanıcıları getir
@router.get("/users", response_model=List[User])
def get_users():
    with open(USERS_FILE, "r") as file:
        users = json.load(file)
    return users

# Yeni bir kullanıcı ekle
@router.post("/users")
def add_user(user: User):
    with open(USERS_FILE, "r") as file:
        users = json.load(file)
    
    # Aynı user_id'ye sahip bir kullanıcı varsa hata döndür
    for u in users:
        if u["user_id"] == user.user_id:
            raise HTTPException(status_code=400, detail="User with this ID already exists.")
    
    # Yeni kullanıcıyı ekle
    users.append(user.dict())
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)
    
    return {"message": "User added successfully"}

# Kullanıcının izlediği filmleri güncelle
@router.put("/users/{user_id}/watched_movies")
def update_watched_movies(user_id: int, watched_movies: List[int]):
    with open(USERS_FILE, "r") as file:
        users = json.load(file)
    
    # Kullanıcıyı bul
    for user in users:
        if user["user_id"] == user_id:
            user["watched_movies"] = watched_movies
            with open(USERS_FILE, "w") as file:
                json.dump(users, file, indent=4)
            return {"message": "Watched movies updated successfully"}
    
    # Kullanıcı bulunamazsa hata döndür
    raise HTTPException(status_code=404, detail="User not found")
