# Generated by Django 3.2.8 on 2021-11-01 17:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.UUIDField(default=uuid.UUID('4fd9797e-9ea2-4a41-bf96-b081b11756aa'), editable=False),
        ),
    ]
