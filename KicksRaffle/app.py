from app import create_app
from config import Config
from flask_migrate import Migrate
from models import db

app = create_app()
app.config.from_object(Config)
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"])