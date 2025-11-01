from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import timedelta
from sqlalchemy import and_

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(256), nullable=False)

class Habitacion(db.Model):
    __tablename__ = 'habitacion'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    disponible = db.Column(db.Boolean, default=True, nullable=False)
    descripcion = db.Column(db.Text)
    servicios = db.Column(db.Text)