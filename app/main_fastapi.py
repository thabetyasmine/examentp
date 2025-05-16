from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import models, schemas
from sqlalchemy import func
from sqlalchemy.orm import joinedload
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatGroq
from langchain.schema import HumanMessage
from fastapi import FastAPI
from pydantic import BaseModel
from groq_chat import ask_groq  # Assure-toi que ce chemin est correct
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from database import get_db
import models
from schemas import SummaryRequest, SummaryResponse
from groq_summary import generate_movie_summary


# Création des tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dépendance pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/movies/", response_model=schemas.MoviePublic)
def create_movie(movie_data: schemas.MovieBase, db: Session = Depends(get_db)):
    # 1. Créer le film
    db_movie = models.Movie(
        title=movie_data.title,
        year=movie_data.year,
        director=movie_data.director
    )
    db.add(db_movie)
    db.commit()        # On valide pour générer l’ID auto-incrémenté
    db.refresh(db_movie)  # On met à jour l'objet avec l'ID généré

    # 2. Créer les acteurs associés
    for actor in movie_data.actors:
        db_actor = models.Actor(
            actor_name=actor.actor_name,
            movie_id=db_movie.id
        )
        db.add(db_actor)

    db.commit()  # Enregistrer les acteurs

    # 3. Récupération complète avec acteurs pour la réponse
    db.refresh(db_movie)
    return db_movie
@app.get("/movies/random/", response_model=schemas.MoviePublic)
def get_random_movie(db: Session = Depends(get_db)):
    # Utiliser joinedload pour charger aussi les acteurs en une seule requête
    movie = db.query(models.Movie)\
              .options(joinedload(models.Movie.actors))\
              .order_by(func.random())\
              .first()

    if not movie:
        raise HTTPException(status_code=404, detail="Aucun film trouvé.")
    
    return movie
load_dotenv()

# Récupérer la clé API
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialiser le modèle ChatGroq
chat = ChatGroq(api_key=groq_api_key, model_name="mixtral-8x7b-32768")

# Exemple d’utilisation
def ask_groq(prompt: str):
    messages = [HumanMessage(content=prompt)]
    response = chat(messages)
    return response.content
app = FastAPI()
app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/groq/")
def chat_with_groq(req: PromptRequest):
    result = ask_groq(req.prompt)
    return {"response": result}
@app.post("/generate_summary/", response_model=SummaryResponse)
def generate_summary(request: SummaryRequest, db: Session = Depends(get_db)):
    movie = db.query(models.Movies).options(joinedload(models.Movies.actors)).filter(models.Movies.id == request.movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    actor_names = [actor.actor_name for actor in movie.actors]

    summary = generate_movie_summary(
        title=movie.title,
        year=movie.year,
        director=movie.director,
        actor_names=actor_names
    )

    return SummaryResponse(summary_text=summary)