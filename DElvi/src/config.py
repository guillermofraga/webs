import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY_DELVI")  # Clave secreta para la aplicación Flask

    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_DELVI")
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
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"] # Convertir a booleano, Obtiene el valor la variable de entorno, la convierte en minúsculas y comprueba si el valor esta en la lista ["true", "1"], si esta en la lista devuelve True, si no devuelve False. 
