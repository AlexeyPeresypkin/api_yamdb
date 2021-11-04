# Generated by Django 3.2.8 on 2021-11-01 17:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]