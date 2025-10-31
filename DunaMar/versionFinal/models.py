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
    reservas = db.relationship('Reserva', backref='usuario', lazy=True, cascade="all, delete-orphan")

class Habitacion(db.Model):
    __tablename__ = 'habitacion'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    disponible = db.Column(db.Boolean, default=True, nullable=False)
    reservas = db.relationship('Reserva', backref='habitacion', lazy=True, cascade="all, delete-orphan")
    descripcion = db.Column(db.Text)
    servicios = db.Column(db.Text)

class Reserva(db.Model):
    __tablename__ = 'reserva'
    id = db.Column(db.Integer, primary_key=True)
    fecha_entrada = db.Column(db.Date, nullable=False)   # inclusive
    fecha_salida = db.Column(db.Date, nullable=False)    # exclusive semantics: guest leaves this date
    estado = db.Column(db.String(20), default='pendiente', nullable=False)
    habitacion_id = db.Column(db.Integer, db.ForeignKey('habitacion.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def occupied_nights(self):
        """
        Devuelve una lista de strings YYYY-MM-DD con las noches ocupadas
        por esta reserva usando la convención semiclosed [entrada, salida),
        es decir, incluye fecha_entrada y todas las noches hasta fecha_salida - 1.
        """
        noches = []
        fecha = self.fecha_entrada
        while fecha < self.fecha_salida:
            noches.append(fecha.isoformat())
            fecha = fecha + timedelta(days=1)
        return noches

    @classmethod
    def overlaps(cls, habitacion_id, fecha_entrada, fecha_salida):
        """
        Comprueba si existe alguna reserva confirmada que solape con el intervalo
        [fecha_entrada, fecha_salida) usando la condición semiclosed:
        existe conflicto si Reserva.fecha_entrada < fecha_salida AND Reserva.fecha_salida > fecha_entrada
        Devuelve True si hay conflicto, False si está libre.
        """
        conflicto = cls.query.filter(
            cls.habitacion_id == habitacion_id,
            cls.estado == 'confirmada',
            and_(
                cls.fecha_entrada < fecha_salida,
                cls.fecha_salida > fecha_entrada
            )
        ).first()
        return conflicto is not None

    def __repr__(self):
        return f"<Reserva id={self.id} habitacion={self.habitacion_id} entrada={self.fecha_entrada} salida={self.fecha_salida} estado={self.estado}>"