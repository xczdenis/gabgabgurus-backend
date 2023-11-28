# Generated by Django 4.2.6 on 2023-11-09 05:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("languages", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserLanguage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("is_learning", models.BooleanField(default=False)),
                ("is_speaking", models.BooleanField(default=False)),
                (
                    "language_level",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Beginner"),
                            (1, "Elementary"),
                            (2, "Intermediate"),
                            (3, "Advanced"),
                            (4, "Proficiency"),
                            (5, "Native"),
                        ],
                        default=0,
                        verbose_name="language level",
                    ),
                ),
                (
                    "language",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_languages",
                        to="languages.language",
                    ),
                ),
            ],
        ),
    ]
