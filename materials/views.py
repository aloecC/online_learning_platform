from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.utils import logger
from materials.tasks import send_mail_after_update
from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPagination
from materials.permisions import IsModerator, IsOwner, IsRedactManager
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.models import User
from django.core.cache import cache


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = MaterialsPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'update']:
            self.permission_classes = [IsAuthenticated | IsModerator]
        elif self.action in ['create', 'destroy']:
            self.permission_classes = [IsRedactManager]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='Модераторы').exists():
                return Course.objects.all()
            else:
                return Course.objects.filter(owner=self.request.user)
        return Course.objects.none()

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        course_id = kwargs.get('pk')  # Получаем ID обновленного курса

        # Преобразуем QuerySet в список

        cache_key = f"course_notify_{course_id}"
        already_sent = cache.get(cache_key)
        if not already_sent:
            emails = list(Subscription.objects.filter(course_id=course_id).values_list('user__email', flat=True))
            users_emails_list = list(emails)
            if emails:
                send_mail_after_update.delay(course_id, users_emails_list)
                send_mail_after_update.delay(course_id, emails)
                cache.set(cache_key, True, timeout=4 * 3600)

        return response

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Удаление курса"""
        return super().destroy(request, *args, **kwargs)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsRedactManager]

    def perform_create(self, serializer):
        course_id = self.request.data.get('course')
        try:
            course = Course.objects.get(id=course_id)
            if course.owner != self.request.user:
                raise PermissionDenied("Вы не имеете прав на добавление уроков в этот курс.")
        except Course.DoesNotExist:
            raise PermissionDenied("Курс не найден.")

        # Создаем новый урок, устанавливая владельца
        new_lesson = serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Вывод информации об уроке"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class LessonListAPIView(generics.ListAPIView):
    """Вывод информации об уроках"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]
    pagination_class = MaterialsPagination


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Обновление урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            self.permission_classes = [IsModerator]
        else:
            self.permission_classes = [IsOwner]

        return super().get_permissions()

    def send_mail(self):
        """Отправка письма после обновления"""
        lesson = self.get_object()
        course_id = lesson.course_id

        cache_key = f"course_notify_{course_id}"
        already_sent = cache.get(cache_key)
        if not already_sent:
            emails = list(Subscription.objects.filter(course_id=course_id).values_list('user__email', flat=True))
            users_emails_list = list(emails)
            if emails:
                send_mail_after_update.delay(course_id, users_emails_list)
                send_mail_after_update.delay(course_id, emails)
                cache.set(cache_key, True, timeout=4 * 3600)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление урока"""
    queryset = Lesson.objects.all()

    def get_permissions(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return [IsModerator()]  # Модераторы могут удалять
        return [IsOwner()]  # Остальные могут удалять только свои


class SubscriptionView(APIView):
    """Проведение проверки подписки"""
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = request.data.get('course_id')

        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_id)

        if subs_item.exists():
            subs_item.delete()
            return Response({'detail': 'Подписка удалена'}, status=204)

        else:
            Subscription.objects.create(user=user, course=course_item)
            return Response({'detail': 'Подписка создана'}, status=201)


