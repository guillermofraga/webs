import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root@localhost/dunamar')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY','duna-mar-2025-7,3;Wclha9v.6qZDTS1-clave-segura')
    N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL',"https://automatizaciones-n8n.sctfuk.easypanel.host/webhook-test/emailConfirmacion")