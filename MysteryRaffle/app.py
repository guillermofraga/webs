from flask import Flask
from config import Config
from flask_migrate import Migrate
from models import db
from routes.main import main_bp
from routes.raffle import raffle_bp

app = Flask(__name__)
app.config.from_object(Config)

#Inicializar la base de datos
try:
    db.init_app(app)
    migrate = Migrate(app, db)
except Exception as e:
    print(f"Error initializing database: {e}")

#Registrar blueprints
app.register_blueprint(main_bp)
app.register_blueprint(raffle_bp)


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"])