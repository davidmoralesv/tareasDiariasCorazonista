from flask import Flask
from config import Config
from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'main.login'  # The route to redirect to for login

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def create_app(config_class=Config):
    """
    Application factory function.
    Initializes the Flask app, database, and extensions.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    # Register the blueprint for the main routes
    from .routes import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
