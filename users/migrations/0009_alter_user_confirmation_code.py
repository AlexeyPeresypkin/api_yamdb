# Generated by Django 3.2.8 on 2021-11-01 17:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.UUIDField(default=uuid.UUID('c3b4834d-6552-4601-ba4c-4bec5caecdac'), editable=False),
        ),
    ]