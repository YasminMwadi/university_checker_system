# Generated by Django 4.2.7 on 2023-11-08 21:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("university_checker_app", "0014_delete_test"),
    ]

    operations = [
        migrations.AlterField(
            model_name="filteredtweets",
            name="negative",
            field=models.TextField(default="", null=True),
        ),
        migrations.AlterField(
            model_name="filteredtweets",
            name="neutral",
            field=models.TextField(default="", null=True),
        ),
        migrations.AlterField(
            model_name="filteredtweets",
            name="positive",
            field=models.TextField(default="", null=True),
        ),
    ]
