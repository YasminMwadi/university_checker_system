# Generated by Django 4.2.7 on 2023-11-08 20:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("university_checker_app", "0011_delete_filteredtweets"),
    ]

    operations = [
        migrations.CreateModel(
            name="FilteredTweets",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("positive", models.TextField()),
                ("negative", models.TextField()),
                ("neutral", models.TextField()),
                ("created_at", models.DateTimeField()),
                (
                    "university_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="university_checker_app.university",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
