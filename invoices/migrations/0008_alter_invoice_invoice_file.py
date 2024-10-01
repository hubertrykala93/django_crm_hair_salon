# Generated by Django 5.1 on 2024-10-01 18:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoices", "0007_alter_invoice_invoice_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="invoice_file",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="invoice_file",
                to="invoices.invoicefile",
            ),
        ),
    ]
