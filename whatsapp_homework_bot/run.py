import click
from app import create_app, db
from app.models import User, Grade, Subscription

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """
    Makes database models available in the `flask shell` context
    without needing to be imported manually.
    """
    return {'db': db, 'User': User, 'Grade': Grade, 'Subscription': Subscription}

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


if __name__ == '__main__':
    from apscheduler.schedulers.background import BackgroundScheduler
    from app.scheduler_jobs import send_daily_homework_job, process_daily_renewals_job

    # Initialize and start the scheduler
    scheduler = BackgroundScheduler(daemon=True, timezone="America/Bogota")

    # Schedule the daily homework job for 2 PM
    scheduler.add_job(
        send_daily_homework_job,
        'cron',
        hour=14,
        minute=0,
        id='daily_homework_job',
        replace_existing=True
    )

    # Schedule the daily renewal job for 1 AM
    scheduler.add_job(
        process_daily_renewals_job,
        'cron',
        hour=1,
        minute=0,
        id='daily_renewal_job',
        replace_existing=True
    )

    scheduler.start()
    print("--> Tarea de envío de tareas programada para las 2:00 PM (Hora de Colombia).")
    print("--> Tarea de proceso de renovaciones programada para la 1:00 AM (Hora de Colombia).")

    # Run the Flask web server
    # use_reloader=False is important to prevent the scheduler from being initialized twice.
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
