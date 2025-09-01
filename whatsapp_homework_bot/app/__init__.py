import os
from flask import Flask
from config import Config
from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
from .scheduler_jobs import send_daily_homework_job, process_daily_renewals_job

login_manager = LoginManager()
login_manager.login_view = 'main.login'  # The route to redirect to for login

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def create_app(config_class=Config):
    """
    Application factory function.
    Initializes the Flask app and its extensions.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from .routes import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    # Register CLI commands
    from . import commands
    commands.register_commands(app)

    # Initialize and start the scheduler, ensuring it only runs in the main process
    if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        scheduler = BackgroundScheduler(daemon=True, timezone="America/Bogota")
        scheduler.add_job(
            send_daily_homework_job,
            'cron',
            hour=14,
            id='daily_homework_job',
            replace_existing=True
        )
        scheduler.add_job(
            process_daily_renewals_job,
            'cron',
            hour=1,
            id='daily_renewal_job',
            replace_existing=True
        )
        scheduler.start()
        print("--> Programador de tareas iniciado en segundo plano.")

    return app
