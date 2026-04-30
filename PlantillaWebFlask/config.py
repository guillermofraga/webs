import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    # Add other configuration variables as needed
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']