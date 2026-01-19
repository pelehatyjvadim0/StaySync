from app.tasks.celery_app import celery_app
import time

@celery_app.task
def send_email(booking_dict: dict, email_to: str):
    print(f"Начинаю отправку письма для {email_to}...")
    time.sleep(5) 
    print(f"Письмо о бронировании {booking_dict['id']} успешно отправлено!")