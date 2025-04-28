from fastapi import FastAPI
from fast_api.categories import router as categories_router
from fast_api.genres import router as genres_router
from fast_api.movies import router as movies_router
from fast_api.users import router as users_router
from fast_api.user_ratings import router as user_ratings_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is working"}

# Modülleri uygulamaya ekle
app.include_router(categories_router)
app.include_router(genres_router)
app.include_router(movies_router)
app.include_router(users_router)
app.include_router(user_ratings_router)