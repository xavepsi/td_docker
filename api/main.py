import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()

# Variables d'environnement
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "database")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app = FastAPI()

# Connexion à la base de données
engine = create_engine(DATABASE_URL, future=True)
metadata = MetaData()

# Table items
items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("description", String, nullable=True),
)

class Item(BaseModel):
    id: int
    title: str
    description: str | None = None

@app.on_event("startup")
def startup():
    """Crée les tables au démarrage"""
    try:
        with engine.begin() as conn:
            metadata.create_all(conn)
    except OperationalError:
        pass

@app.get("/status")
def status():
    """Route /status : retourne OK"""
    return {"status": "OK"}

@app.get("/items")
def get_items():
    """Route /items : retourne la liste des items"""
    try:
        with engine.connect() as conn:
            result = conn.execute(select(items)).fetchall()
            return [{"id": r[0], "title": r[1], "description": r[2]} for r in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
