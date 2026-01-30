from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Votacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    raffle_price = db.Column(db.Float, nullable=False, unique=True)

class Raffle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    raffle = db.Column(db.Integer, nullable=False, unique=True)
