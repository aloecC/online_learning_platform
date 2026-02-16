from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True,)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    """Модель Платежей"""

    METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='payments')
    payment_date = models.DateField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name='payments')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True, related_name='payments')
    payment_amount = models.PositiveIntegerField(blank=True, null=True, verbose_name='Сумма платежа')
    payment_method = models.CharField(max_length=10, choices=METHOD_CHOICES, default="transfer", verbose_name="Способ оплаты")

    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='id сессии')
    link_payment = models.URLField(max_length=450, blank=True, null=True, verbose_name='Ссылка на оплату')
    status = models.CharField(max_length=10, default="Создан", verbose_name="Статус платежа")

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return self.payment_amount