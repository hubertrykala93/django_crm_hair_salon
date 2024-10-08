# Generated by Django 5.1 on 2024-10-08 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0004_jobtype_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="employmentstatus",
            name="slug",
            field=models.SlugField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="paymentfrequency",
            name="slug",
            field=models.SlugField(max_length=100, null=True, unique=True),
        ),
    ]
