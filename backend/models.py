# backend/models.py
from datetime import datetime
from db import db

class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    razon_social = db.Column(db.String(160), nullable=False)
    cuit = db.Column(db.String(13), unique=True, nullable=False)
    email = db.Column(db.String(160))
    telefono = db.Column(db.String(30))
    direccion = db.Column(db.String(200))
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Cliente {self.razon_social} ({self.cuit})>"
