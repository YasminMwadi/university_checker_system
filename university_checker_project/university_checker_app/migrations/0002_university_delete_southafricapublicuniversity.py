# Generated by Django 4.2.6 on 2023-11-03 19:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("university_checker_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="university",
            fields=[
                ("university_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("location", models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name="SouthAfricaPublicUniversity",
        ),
    ]