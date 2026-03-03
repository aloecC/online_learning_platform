from django.contrib import admin

from config import settings
from materials.models import Lesson, Course


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления уроками"""
    list_display = (id, "course", "title", "preview", "description", "video")
    list_filter = ("course",)  # Фильтрация
    search_fields = (
        "course",
        "title",
        "description",
    )  # Поиск


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления курсами."""
    list_display = (id, "title", "preview", "description")
    list_filter = ("title",)  # Фильтрация
    search_fields = (
        "title",
        "description",
    )  # Поиск
