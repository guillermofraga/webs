from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Votacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    precio_rifa = db.Column(db.Float, nullable=False)

class Raffle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    rifa = db.Column(db.Integer, nullable=False, unique=True)
