# Generated by Django 5.1.6 on 2025-03-22 07:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0006_course_amount_course_duration"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("event_date", models.DateField()),
            ],
        ),
    ]
