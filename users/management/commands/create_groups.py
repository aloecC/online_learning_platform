from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создает группу "Модераторы"'

    def handle(self, *args, **kwargs):
        moderators_group, created = Group.objects.get_or_create(name="Модераторы")
        if created:
            self.stdout.write(
                self.style.SUCCESS("Группа 'Модераторы' успешно создана.")
            )
        else:
            self.stdout.write(self.style.WARNING("Группа 'Модераторы' уже существует."))
