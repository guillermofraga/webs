import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")

    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de correo (Gmail)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # Correo del administrador para recibir copias de confirmaciones
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

    # Configuración de depuración
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"]