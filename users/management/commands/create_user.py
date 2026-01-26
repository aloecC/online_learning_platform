from django.contrib.auth import get_user_model

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            username="buyer_3",
            email="buyer3@mail.com",
            first_name="buyer_3",
            last_name="buyer_3",
        )

        user.set_password("12345")

        user.is_staff = False
        user.is_superuser = False

        user.save()

        self.stdout.write(self.style.SUCCESS("Пользователь успешно создан"))