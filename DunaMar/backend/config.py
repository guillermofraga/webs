import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/dunamar'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'duna-mar-2025-7,3;(Wclha9v.6qZDTS1-clave-segura'