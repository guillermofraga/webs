import uuid
from flask_sqlalchemy import SQLAlchemy

# Instancia global de SQLAlchemy (se inicializa en app.py)
db = SQLAlchemy()

class Reserva(db.Model):
    __tablename__ = "reserva"  # opcional, si quieres controlar el nombre de la tabla

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    personas = db.Column(db.Integer, nullable=False)
    codigo_unico = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
