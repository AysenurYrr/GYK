from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from typing import List

router = APIRouter()

# JSON dosyasının yolu
CATEGORIES_FILE = "c:\\Users\\bilgisayar\\Desktop\\repositorys\\GYK\\6\\database\\categories.json"

# Kategori modeli
class Category(BaseModel):
    category_id: int
    name: str

# Tüm kategorileri getir
@router.get("/categories", response_model=List[Category])
def get_categories():
    with open(CATEGORIES_FILE, "r") as file:
        categories = json.load(file)
    return categories

# Yeni bir kategori ekle
@router.post("/categories")
def add_category(category: Category):
    with open(CATEGORIES_FILE, "r") as file:
        categories = json.load(file)

    # Aynı category_id'ye sahip bir kategori varsa hata döndür
    for c in categories:
        if c["category_id"] == category.category_id:
            raise HTTPException(status_code=400, detail="Category with this ID already exists.")

    # Yeni kategoriyi ekle
    categories.append(category.dict())
    with open(CATEGORIES_FILE, "w") as file:
        json.dump(categories, file, indent=4)

    return {"message": "Category added successfully"}
