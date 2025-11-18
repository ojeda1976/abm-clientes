# backend/config.py
import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

class Config:
    # URL de conexión a PostgreSQL (se toma de .env)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Puerto en el que corre Flask
    PORT = int(os.getenv("PORT", "4000"))
