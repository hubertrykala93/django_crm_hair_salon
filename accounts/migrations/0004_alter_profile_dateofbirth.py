# Generated by Django 4.2.16 on 2024-09-13 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_profile_dateofbirth"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="dateofbirth",
            field=models.DateField(blank=True, null=True),
        ),
    ]
