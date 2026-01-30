from flask import Flask

def create_app():
    app = Flask(__name__)

    #Registrar blueprints
    from .routes.main import main_bp
    from .routes.raffle import raffle_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(raffle_bp)

    return app