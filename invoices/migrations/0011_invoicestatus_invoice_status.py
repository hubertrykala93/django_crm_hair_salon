# Generated by Django 5.1 on 2024-10-01 20:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("invoices", "0010_alter_invoice_invoice_file"),
    ]

    operations = [
        migrations.CreateModel(
            name="InvoiceStatus",
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
                ("name", models.CharField(max_length=20, null=True)),
            ],
            options={
                "verbose_name": "Invoice Status",
                "verbose_name_plural": "Invoice Statuses",
            },
        ),
        migrations.AddField(
            model_name="invoice",
            name="status",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="invoices.invoicestatus",
            ),
        ),
    ]
