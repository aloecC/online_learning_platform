from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from decimal import Decimal
from django.utils import timezone

from materials.models import Lesson, Course
from users.models import User, Payment


class Command(BaseCommand):
    help = 'Populate the Payment model with sample data using existing records'

    def handle(self, *args, **kwargs):
        try:
            user_id = 5  # ID существующего пользователя
            course_id = 3  # ID существующего курса
            lesson_id = 10  # ID существующего урока

            # Получаем существующие объекты по ID
            user = User.objects.get(id=user_id)
            course = Course.objects.get(id=course_id)
            lesson = Lesson.objects.get(id=lesson_id)

            # Создаем несколько платежей
            payments_data = [
                {
                    'user': user,
                    'payment_date': timezone.now().date(),
                    'lesson': lesson,
                    'payment_amount': Decimal('100.00'),
                    'payment_method': 'cash',
                },
                {
                    'user': user,
                    'payment_date': timezone.now().date(),
                    'course': course,
                    'payment_amount': Decimal('200.00'),
                    'payment_method': 'transfer',
                },
            ]

            for payment_data in payments_data:
                Payment.objects.create(**payment_data)

            self.stdout.write(self.style.SUCCESS('Successfully populated the Payment model with sample data'))

        except ObjectDoesNotExist as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))