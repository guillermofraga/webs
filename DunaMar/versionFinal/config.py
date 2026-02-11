import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True         # solo se envía por HTTPS
    SESSION_COOKIE_HTTPONLY = True       # no accesible por JavaScript
    SESSION_COOKIE_SAMESITE = 'Lax'      # evita envío cruzado en formularios externos

    # Configuración de correo (Gmail)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # Correo del administrador para recibir copias de confirmaciones
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
