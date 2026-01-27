from django.db import models

from config import settings


class Course(models.Model):
    '''Модель курса'''
    title = models.CharField(max_length=150, verbose_name='название курса')
    preview = models.ImageField(upload_to='photos/', blank=True, null=True)
    description = models.TextField(max_length=1500, blank=True, null=True, verbose_name='описание курса')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    '''Модель урока'''
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=150, blank=True, null=True, verbose_name='название урока')
    preview = models.ImageField(upload_to='photos/', blank=True, null=True)
    description = models.TextField(max_length=1500, blank=True, null=True, verbose_name='описание урока')
    video = models.URLField(blank=True, null=True, verbose_name='ссылка на видео')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

