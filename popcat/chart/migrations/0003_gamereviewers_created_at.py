# Generated by Django 4.2.11 on 2024-04-17 06:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("chart", "0002_game_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="gamereviewers",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]