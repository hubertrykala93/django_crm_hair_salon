# Generated by Django 5.1 on 2024-09-27 14:11

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentMethod",
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
                "verbose_name": "Payment Method",
                "verbose_name_plural": "Payment Methods",
            },
        ),
        migrations.CreateModel(
            name="PaymentTerms",
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
                ("name", models.CharField(max_length=500, unique=True)),
            ],
            options={
                "verbose_name": "Payment Term",
                "verbose_name_plural": "Payment Terms",
            },
        ),
        migrations.CreateModel(
            name="VatRate",
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
                ("rate", models.IntegerField(unique=True)),
            ],
            options={"verbose_name": "Vat Rate", "verbose_name_plural": "Vat Rates",},
        ),
        migrations.CreateModel(
            name="InvoiceDetails",
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
                ("issue_date", models.DateTimeField(default=django.utils.timezone.now)),
                ("invoice_number", models.CharField(max_length=100, unique=True)),
                (
                    "description_of_product_or_services",
                    models.CharField(max_length=1000, unique=True),
                ),
                (
                    "unit_net_price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("quantity", models.IntegerField()),
                ("net_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("vat_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("gross_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("payment_due_date", models.DateField()),
                (
                    "buyers_details",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.profile",
                    ),
                ),
                (
                    "sellers_details",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="core.company"
                    ),
                ),
                (
                    "payment_method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="invoices.paymentmethod",
                    ),
                ),
                ("payment_terms", models.ManyToManyField(to="invoices.paymentterms")),
                (
                    "vat_rate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="invoices.vatrate",
                    ),
                ),
            ],
            options={"verbose_name": "Invoice", "verbose_name_plural": "Invoices",},
        ),
        migrations.CreateModel(
            name="Invoice",
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
                ("file", models.FileField(upload_to="core/invoices")),
                (
                    "invoice_details",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="invoices.invoicedetails",
                    ),
                ),
            ],
            options={"verbose_name": "Invoice", "verbose_name_plural": "Invoices",},
        ),
    ]
