from datetime import datetime, timedelta

from celery import shared_task
from users.models import User


@shared_task
def blocking_user():
    """Блокировка пользователя, если он не заходил более 31 дня."""

    users = User.objects.all()
    for user in users:

        if user.last_login is not None and (datetime.now() - user.last_login) >= timedelta(days=31):
            user.is_active = False
            user.save()
            print(f"Пользователь {user.username} был заблокирован.")
        else:
            print(f"Пользователь {user.username} активен или только что вошел в систему.")

