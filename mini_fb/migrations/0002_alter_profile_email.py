# Generated by Django 5.1.5 on 2025-03-05 14:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mini_fb", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="email",
            field=models.TextField(),
        ),
    ]
