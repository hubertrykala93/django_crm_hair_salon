# Generated by Django 5.1 on 2024-09-28 13:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contracts", "0002_alter_contract_payment_method"),
        ("payments", "0006_paymentmethod_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contract",
            name="payment_method",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="payments.paymentmethod",
            ),
        ),
    ]