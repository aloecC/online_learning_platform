from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from config import settings
from users.models import Payment, User


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (id, "user", "payment_date", "course", "lesson", "payment_amount", "payment_method")
    list_filter = ("course", "user", "payment_method", "payment_date",)  # Фильтрация
    search_fields = (
        "lesson",
        "course",
        "user",
    )  # Поиск


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["email", "username", "phone_number", "is_staff"]
    list_filter = ["is_staff", "is_active"]
    ordering = ["email"]
    search_fields = ["email", "username"]


admin.site.register(User, CustomUserAdmin)


