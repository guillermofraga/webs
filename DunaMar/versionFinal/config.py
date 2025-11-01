import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True         # solo se envía por HTTPS
    SESSION_COOKIE_HTTPONLY = True       # no accesible por JavaScript
    SESSION_COOKIE_SAMESITE = 'Lax'      # evita envío cruzado en formularios externos
