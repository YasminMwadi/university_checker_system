# Generated by Django 4.2.7 on 2023-11-08 20:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("university_checker_app", "0010_filteredtweets"),
    ]

    operations = [
        migrations.DeleteModel(
            name="FilteredTweets",
        ),
    ]
