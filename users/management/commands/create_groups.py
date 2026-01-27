from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Создает группу "Модераторы"'

    def handle(self, *args, **kwargs):
        moderators_group, created = Group.objects.get_or_create(name='Модераторы')
        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'Модераторы' успешно создана."))
        else:
            self.stdout.write(self.style.WARNING("Группа 'Модераторы' уже существует."))