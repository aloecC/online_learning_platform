import datetime

from celery import shared_task
from django.core.mail import send_mail



@shared_task
def send_mail_after_update(course_id, users_email):
    """Отправка письма при изменениях на курсе"""
    for user_email in users_email:
        subject = 'Курс обновлен'
        message = f'Курс с ID {course_id} был обновлен.'
        send_mail(subject, message, 'from@example.com', [user_email])
        print(f'Письмо отправлено на {user_email}')


