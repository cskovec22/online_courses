from django.db.models.signals import post_save
from django.dispatch import receiver

from courses.models import Group
from users.models import Subscription


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.
    """

    if created:
        course = instance.course
        user = instance.subscriber

        groups = Group.objects.filter(course=course).order_by("id")

        if groups.exists():
            group_count = groups.count()
            group_index = (user.id % group_count) - 1
            group = groups[group_index]
            group.students.add(user)
