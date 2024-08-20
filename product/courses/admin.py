from django.contrib.admin import ModelAdmin, register

from courses.models import Course, Group, Lesson


@register(Course)
class CourseAdmin(ModelAdmin):
    """Административный класс для курса."""

    list_display = ("id", "author", "title", "price", "start_date")
    ordering = ("author", "id")


@register(Group)
class GroupAdmin(ModelAdmin):
    """Административный класс для группы."""

    list_display = ("id", "title", "course")
    ordering = ("course", "id")


@register(Lesson)
class LessonAdmin(ModelAdmin):
    """Административный класс для урока."""

    list_display = ("id", "title", "course")
    ordering = ("course", "id")
