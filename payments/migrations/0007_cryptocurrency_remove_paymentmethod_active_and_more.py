# Generated by Django 5.1 on 2024-09-29 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0006_paymentmethod_active"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cryptocurrency",
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
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "verbose_name": "Cryptocurrency",
                "verbose_name_plural": "Cryptocurrencies",
            },
        ),
        migrations.RemoveField(model_name="paymentmethod", name="active",),
        migrations.AddField(
            model_name="cryptotransfer",
            name="cryptocurrency",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="payments.cryptocurrency",
            ),
        ),
    ]
