from app import create_app, db
from app.models import User, Grade, Subscription

# The app instance is created by the factory function in __init__.py
app = create_app()

@app.shell_context_processor
def make_shell_context():
    """
    Makes database models available in the `flask shell` context
    without needing to be imported manually.
    """
    return {'db': db, 'User': User, 'Grade': Grade, 'Subscription': Subscription}

if __name__ == '__main__':
    # The Flask development server is now run via the 'flask run' command.
    # The application and its extensions (including the scheduler) are
    # configured and created via the app factory.
    # To run in production, a WSGI server like Gunicorn or Waitress should be used.
    # Example for development:
    # > set FLASK_APP=whatsapp_homework_bot/run.py
    # > flask run
    print("To run the application, use the 'flask run' command.")
    print("Example for Windows CMD:")
    print("set FLASK_APP=whatsapp_homework_bot/run.py")
    print("flask run")
