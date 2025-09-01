import click
from .models import db, User, Grade

def register_commands(app):
    """Registers custom command-line commands for the application."""

    @app.cli.command("create-admin")
    @click.argument("username")
    @click.argument("password")
    def create_admin(username, password):
        """Creates a new admin user."""
        if User.query.filter_by(username=username).first():
            print(f"Error: El usuario '{username}' ya existe.")
            return

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"Usuario administrador '{username}' creado exitosamente.")

    @app.cli.command("seed-grades")
    def seed_grades():
        """Populates the Grade table with initial data."""
        if Grade.query.first():
            print("La tabla 'Grade' ya contiene datos.")
            return

        grades_data = [
            {"name": "Transición", "url": "https://csc.edu.co/ecwd_calendar/tareas-en-casa-transicion/"},
            {"name": "Primero", "url": "https://csc.edu.co/ecwd_calendar/tareas-en-casa-primero/"},
            {"name": "Segundo", "url": "https://csc.edu.co/ecwd_calendar/tareas-en-casa-segundo/"},
            {"name": "Tercero", "url": "https://csc.edu.co/ecwd_calendar/tareas-en-casa-tercero/"},
            {"name": "Cuarto", "url": "https://csc.edu.co/ecwd_calendar/tareas-en-casa-cuarto/"},
            {"name": "Quinto", "url": "https://csc.edu.co/ecwd_calendar/tareas-en-casa-quinto/"},
            {"name": "Sexto", "url": "https://csc.edu.co/ecwd_calendar/tareas-en-casa-sexto/"},
            {"name": "Séptimo", "url": "https://csc.edu.co/ecwd_calendar/tareas-en-casa-septimo/"},
            {"name": "Octavo", "url": "https://csc.edu.co/ecwd_calendar/tareas-en-casa-octavo/"},
            {"name": "Noveno A", "url": "https://csc.edu.co/ecwd_calendar/tareas-en-casa-noveno-a/"},
            {"name": "Noveno B", "url": "https://csc.edu.co/ecwd_calendar/9-tareas-en-casa-9b/"},
            {"name": "Décimo", "url": "https://csc.edu.co/ecwd_calendar/tareas-en-casa-decimo/"},
            {"name": "Undécimo A", "url": "https://csc.edu.co/ecwd_calendar/tareas-en-casa-undecimo-a"},
            {"name": "Undécimo B", "url": "https://csc.edu.co/ecwd_calendar/tareas-en-casa-undecimo-b/"}
        ]

        for grade_info in grades_data:
            grade = Grade(name=grade_info["name"], calendar_url=grade_info["url"])
            db.session.add(grade)

        db.session.commit()
        print("La tabla 'Grade' ha sido poblada con los datos iniciales.")
