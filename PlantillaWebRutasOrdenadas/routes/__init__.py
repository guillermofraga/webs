from flask import Flask
from config import Config
'''
Si queremos añadir base de datos, descomenta estas líneas y asegúrate de tener las dependencias necesarias en tu entorno (como Flask-Migrate y SQLAlchemy).
from flask_migrate import Migrate
from models import db
'''

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static') # Configurar carpetas de plantillas y estáticos
    app.config.from_object(Config)
    '''
    #Inicializar la base de datos
    try:
        db.init_app(app)
        migrate = Migrate(app, db)
    except Exception as e:
        print(f"Error initializing database: {e}")
    '''

    #Registrar blueprints
    from .main import main_bp
    from .uploads import uploads_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(uploads_bp)

    return app