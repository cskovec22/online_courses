from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import (IsStudentOrIsAdmin,
                                make_payment,
                                ReadOnlyOrIsAdmin)
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get("course_id"))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get("course_id"))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get("course_id"))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get("course_id"))
        return course.groups.prefetch_related("students").annotate(
            students_count=Count("students")
        )


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы."""

    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CourseSerializer
        return CreateCourseSerializer

    def get_queryset(self):
        queryset = Course.objects.prefetch_related("lessons").annotate(
            lessons_count=Count("lessons", distinct=True),
            students_count=Count("subscriptions", distinct=True),
        )

        if self.request.user.is_authenticated:
            queryset = queryset.exclude(
                subscriptions__subscriber=self.request.user
            )

        if not self.request.user.is_staff:
            queryset = queryset.filter(is_access=True)

        return queryset

    @action(
        methods=["post"],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""

        user = request.user
        course = get_object_or_404(Course, pk=pk)

        if Subscription.objects.filter(
            subscriber=user,
            course=course
           ).exists():
            Response(
                {
                    "message": (
                        "Вы уже приобрели этот курс."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        data = {"student": user, "course": course}
        serializer = SubscriptionSerializer(data=data)

        if serializer.is_valid():
            if make_payment(request, course):
                return Response(
                    {
                        "message": (
                            "Оплата прошла успешно, "
                            "Вы подписались на курс."
                        )
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"error": "Недостаточно средств для оплаты."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
