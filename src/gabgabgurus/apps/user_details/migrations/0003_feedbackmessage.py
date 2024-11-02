# Generated by Django 5.0 on 2024-11-02 07:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_details", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeedbackMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=250, verbose_name="name")),
                ("email", models.CharField(max_length=250, verbose_name="email")),
                ("text", models.CharField(max_length=250, verbose_name="text")),
                ("processed", models.BooleanField(default=False, verbose_name="processed")),
            ],
            options={
                "verbose_name": "FeedbackMessage",
                "verbose_name_plural": "FeedbackMessages",
                "ordering": ("name",),
            },
        ),
    ]