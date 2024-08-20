from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import Balance, Subscription


def make_payment(request, course):
    """Оплата курса."""

    balance, created = Balance.objects.get_or_create(owner=request.user)

    if balance.balance >= course.price:
        balance.balance -= course.price
        balance.save()
        return True

    return False


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_staff
            or Subscription.objects.filter(
                subscriber=request.user,
                course__id=view.kwargs.get("course_id")
            ).exists()
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_staff
            or Subscription.objects.filter(
                subscriber=request.user,
                course__lessons=obj
            ).exists()
        )


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
