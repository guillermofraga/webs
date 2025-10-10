from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(256), nullable=False)

class Hotel(db.Model):
    __tablename__ = 'hoteles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(100), nullable=False)
    habitaciones = db.relationship('Habitacion', backref='hotel', lazy=True, cascade="all, delete-orphan")

class Habitacion(db.Model):
    __tablename__ = 'habitaciones'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    disponible = db.Column(db.Boolean, default=True, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hoteles.id'), nullable=False)
    reservas = db.relationship('Reserva', backref='habitacion', lazy=True, cascade="all, delete-orphan")

class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    fecha_entrada = db.Column(db.Date, nullable=False)
    fecha_salida = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), default='pendiente', nullable=False)
    habitacion_id = db.Column(db.Integer, db.ForeignKey('habitaciones.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario = db.relationship('Usuario', backref='reservas')
