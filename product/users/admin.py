from django.contrib.admin import ModelAdmin, register, TabularInline

from users.models import Balance, CustomUser, Subscription


@register(Balance)
class BalanceAdmin(ModelAdmin):
    """Административный класс для баланса пользователя."""

    list_display = ("id", "owner", "balance")


class BalanceInline(TabularInline):
    model = Balance


class SubscriptionInline(TabularInline):
    model = Subscription


@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    """Административный класс для кастомного пользователя."""

    list_display = ("id", "first_name", "last_name", "email")
    inlines = [BalanceInline, SubscriptionInline]


@register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    """Административный класс для подписок."""

    list_display = ("id", "course", "subscriber")
    ordering = ("course", "subscriber")
