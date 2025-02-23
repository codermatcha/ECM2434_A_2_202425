# Generated by Django 5.1.6 on 2025-02-22 19:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bingo", "0002_alter_user_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Player", "Player"),
                    ("Game Keeper", "Game Keeper"),
                    ("Developer", "Developer"),
                ],
                default="Player",
                max_length=20,
                null=True,
            ),
        ),
    ]
