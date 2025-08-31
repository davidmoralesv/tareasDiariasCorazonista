from datetime import date, timedelta
from .models import Subscription, db
from .services import scraper_service, tts_service, whatsapp_service, wompi_service
from .utils import is_work_day
from . import create_app

def send_daily_homework_job():
    """
    The main scheduled job to find and send homework.
    This function is designed to be run within a Flask application context
    to have access to the database.
    """
    app = create_app()
    with app.app_context():
        print("--- [HOMEWORK JOB START] ---")

        today = date.today()
        if not is_work_day(today):
            print("--- [HOMEWORK JOB END] Today is not a working day. ---")
            return

        active_subscriptions = Subscription.query.filter_by(status='active').all()
        if not active_subscriptions:
            print("--- [HOMEWORK JOB END] No active subscriptions found. ---")
            return

        print(f"Found {len(active_subscriptions)} active subscription(s) for homework.")

        for sub in active_subscriptions:
            print(f"Processing homework for subscription {sub.id}...")
            homework_text = scraper_service.get_tasks_for_date(sub.grade.calendar_url, today)

            if not homework_text:
                print(f"No homework found for grade {sub.grade.name}. Skipping.")
                continue

            speech_text = homework_text.replace('*', '').replace('**', '')
            audio_file = tts_service.convert_text_to_audio(speech_text)

            if audio_file:
                whatsapp_service.send_homework_notification(
                    whatsapp_number=sub.whatsapp_number,
                    homework_text=homework_text,
                    audio_filepath=audio_file
                )
                print(f"Homework notification sent for subscription {sub.id}.")
            else:
                print(f"Failed to create audio file for subscription {sub.id}. Skipping notification.")

        print("--- [HOMEWORK JOB END] ---")


def process_daily_renewals_job():
    """
    Finds subscriptions that are expiring soon and attempts to renew them.
    """
    app = create_app()
    with app.app_context():
        print("--- [RENEWAL JOB START] ---")

        # Find active subscriptions that expire within the next 24 hours
        # and have a payment source token.
        tomorrow = date.today() + timedelta(days=1)

        subs_to_renew = Subscription.query.filter(
            Subscription.status == 'active',
            Subscription.subscription_end_date <= tomorrow,
            Subscription.wompi_payment_source_id.isnot(None)
        ).all()

        if not subs_to_renew:
            print("--- [RENEWAL JOB END] No subscriptions to renew today. ---")
            return

        print(f"Found {len(subs_to_renew)} subscription(s) to renew.")

        # In a real app, this price would come from the database or a config file.
        # For simulation, we'll use a fixed price of 10,000 COP.
        renewal_amount_cents = 10000 * 100

        for sub in subs_to_renew:
            print(f"Attempting renewal for subscription {sub.id}...")
            wompi_service.create_renewal_transaction(
                subscription_id=sub.id,
                amount_in_cents=renewal_amount_cents,
                payment_source_id=sub.wompi_payment_source_id
            )

        print("--- [RENEWAL JOB END] ---")
