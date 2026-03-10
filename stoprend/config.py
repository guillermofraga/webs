import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    # Add other configuration variables as needed
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']

    # Configuración de correo (Gmail)
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")