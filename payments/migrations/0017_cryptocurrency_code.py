# Generated by Django 5.1 on 2024-09-30 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0016_alter_cryptotransfer_wallet_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="cryptocurrency",
            name="code",
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
