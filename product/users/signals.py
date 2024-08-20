from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Balance, CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_balance(sender, instance, created, **kwargs):
    """Создание баланса для нового пользователя."""

    if created:
        Balance.objects.create(owner=instance)
