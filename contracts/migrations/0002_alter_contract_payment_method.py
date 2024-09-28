# Generated by Django 5.1 on 2024-09-27 22:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0001_initial"),
        ("payments", "0003_alter_paymentmethod_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contract",
            name="payment_method",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="contracts",
                to="payments.paymentmethod",
            ),
        ),
    ]
