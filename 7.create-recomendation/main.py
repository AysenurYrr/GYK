from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
import models
from recommendation import get_recommendations

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/recommendations/{user_id}")
async def recommend(user_id: int, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    movies = get_recommendations(db, user_id)
    return [{
        'movie_id': m.id,
        'title': m.title,
        'imdb_rating': m.imdb_rating,
        'genres': [g.name for g in m.genres]
    } for m in movies]