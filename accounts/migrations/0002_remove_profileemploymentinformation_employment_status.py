# Generated by Django 5.1 on 2024-10-01 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profileemploymentinformation", name="employment_status",
        ),
    ]
