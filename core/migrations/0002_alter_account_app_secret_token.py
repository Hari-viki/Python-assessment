# Generated by Django 4.1.13 on 2024-06-21 05:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="app_secret_token",
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255),
        ),
    ]
