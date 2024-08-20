from django.contrib.auth import get_user_model
from rest_framework import serializers

from courses.models import Course, Group, Lesson


User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            "title",
            "link",
            "course"
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            "title",
            "link",
            "course"
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    course = serializers.StringRelatedField(read_only=True)
    students_count = serializers.IntegerField(read_only=True)
    students = StudentSerializer(many=True)

    class Meta:
        model = Group
        fields = (
            "id",
            "title",
            "course",
            "students_count",
            "students"
        )


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            "title",
            "course",
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            "title",
        )


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.IntegerField(read_only=True)
    students_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "author",
            "title",
            "start_date",
            "price",
            "lessons_count",
            "lessons",
            "students_count"
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
        fields = (
            "author",
            "title",
            "start_date",
            "price",
            "is_access"
        )
