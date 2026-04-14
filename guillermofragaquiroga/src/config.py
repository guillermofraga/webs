import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    # Add other configuration variables as needed
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']

    # Configuración de correo
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_RECIPIENTS = os.getenv('MAIL_RECIPIENTS')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
