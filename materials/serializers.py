from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import VideoValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор модели занятий"""

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            VideoValidator(field='video'),
            serializers.UniqueTogetherValidator(fields=['title', 'description'], queryset=Course.objects.all())
        ]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор модели курсов"""
    quantity_lesson = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(fields=['title', 'description'], queryset=Course.objects.all())
        ]

    def get_quantity_lesson(self, obj):
        quantity_lesson = obj.lessons.count()
        return quantity_lesson if quantity_lesson else None


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки"""
    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(fields=['user', 'course'], queryset=Subscription.objects.all())
        ]