# Generated by Django 5.1 on 2024-10-07 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0003_jobposition_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobtype",
            name="slug",
            field=models.SlugField(max_length=100, null=True, unique=True),
        ),
    ]