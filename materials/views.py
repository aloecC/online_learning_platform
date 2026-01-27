from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.permisions import IsModerator, IsOwner, IsRedactManager
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

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
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.groups.filter(name='Moderators').exists():
            self.permission_classes = [IsModerator]
        else:
            self.permission_classes = [IsOwner]

        return super().get_permissions()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()

    def get_permissions(self):
        if self.request.user.groups.filter(name='Moderators').exists():
            return [IsModerator()]  # Модераторы могут удалять
        return [IsOwner()]  # Остальные могут удалять только свои
