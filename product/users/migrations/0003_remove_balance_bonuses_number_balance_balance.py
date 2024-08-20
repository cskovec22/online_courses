# Generated by Django 4.2.10 on 2024-08-20 15:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_balance_bonuses_number_balance_owner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balance',
            name='bonuses_number',
        ),
        migrations.AddField(
            model_name='balance',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество бонусов'),
            preserve_default=False,
        ),
    ]
