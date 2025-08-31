import unittest
import os
from datetime import date, timedelta
from app import create_app, db
from app.models import Subscription, Grade, User
from app.services import scraper_service, tts_service
from app.scheduler_jobs import send_daily_homework_job

class CoreServicesTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test environment before each test."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory DB
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Clean up the environment after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_scraper_service_no_tasks(self):
        """Test the scraper service on a date that likely has no tasks."""
        # Use a known URL and a date that should not have tasks (e.g., today)
        url = "https://csc.edu.co/ecwd_calendar/tareas-en-casa-transicion/"
        # This test is successful if it runs without error and returns None
        result = scraper_service.get_tasks_for_date(url, date.today())
        self.assertIsNone(result, "Scraper should return None for a day with no tasks.")

    def test_tts_service(self):
        """Test the text-to-speech service."""
        text = "Esta es una prueba de audio."
        filepath = tts_service.convert_text_to_audio(text)
        self.assertIsNotNone(filepath, "TTS service should return a filepath.")
        self.assertTrue(os.path.exists(filepath), "Audio file should be created on disk.")
        # Clean up the created file
        if filepath and os.path.exists(filepath):
            os.remove(filepath)

    def test_daily_homework_job_with_active_subscription(self):
        """
        Test the main homework job by creating a dummy active subscription.
        The test succeeds if the job runs to completion without raising an exception.
        """
        # 1. Create a dummy grade and subscription in the in-memory database
        grade = Grade(name="Test Grade", calendar_url="https://csc.edu.co/ecwd_calendar/tareas-en-casa-transicion/")
        db.session.add(grade)
        db.session.commit() # Commit to get the grade ID

        sub = Subscription(
            whatsapp_number="1234567890",
            customer_email="test@example.com",
            grade_id=grade.id,
            subscription_end_date=date.today() + timedelta(days=5),
            status='active'
        )
        db.session.add(sub)
        db.session.commit()

        # 2. Run the job and check for exceptions
        try:
            # We expect this to run and find no tasks for today, but it should not crash.
            send_daily_homework_job()
            self.assertTrue(True) # If we get here, the job ran without error.
        except Exception as e:
            self.fail(f"send_daily_homework_job() raised an exception unexpectedly: {e}")

if __name__ == '__main__':
    unittest.main()
