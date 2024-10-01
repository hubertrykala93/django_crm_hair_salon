from django.db import models
from django.utils.timezone import now
from core.models import Company
from accounts.models import User
from payments.models import PaymentMethod
from datetime import timedelta
from decimal import Decimal
from datetime import date
import os
from django.core.files.storage import default_storage


class IncomeTaxRate(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=2, unique=True)

    class Meta:
        verbose_name = "Income Tax"
        verbose_name_plural = "Income Taxes"

    def __str__(self):
        return str(self.rate)

    def save(self, *args, **kwargs):
        if self.rate:
            self.rate = self.rate / Decimal(value="100")

        super(IncomeTaxRate, self).save(*args, **kwargs)


class InvoiceFile(models.Model):
    created_at = models.DateTimeField(default=now)
    file = models.FileField(upload_to="invoices/invoices")
    size = models.IntegerField(null=True)
    format = models.CharField(max_length=3)

    class Meta:
        verbose_name = "Invoice File"
        verbose_name_plural = "Invoices Files"

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.file:
            self.format = self.file.name.split(sep=".")[-1]
            self.size = self.file.size

        super(InvoiceFile, self).save(*args, **kwargs)


class InvoiceStatus(models.Model):
    name = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name = "Invoice Status"
        verbose_name_plural = "Invoice Statuses"

    def __str__(self):
        return self.name


class Invoice(models.Model):
    issue_date = models.DateTimeField(default=now)
    invoice_number = models.CharField(max_length=100, unique=True, null=True)
    invoice_file = models.OneToOneField(to=InvoiceFile, on_delete=models.CASCADE, null=True)
    payment_method = models.ForeignKey(to=PaymentMethod, on_delete=models.CASCADE, null=True)
    seller_details = models.ForeignKey(to=Company, on_delete=models.CASCADE, null=True)
    buyer_details = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    description_of_product_or_services = models.CharField(max_length=1000, null=True)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    income_tax = models.ForeignKey(to=IncomeTaxRate, on_delete=models.CASCADE, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_due_date = models.DateField(null=True)
    status = models.ForeignKey(to=InvoiceStatus, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
        return str(self.invoice_number)

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)

        self.gross_amount = self.buyer_details.profile.contract.salary

        if self.pk:
            if self.buyer_details.profile.contract.contract_type != "B2B":
                self.net_amount = Decimal(value=self.gross_amount / (1 + self.income_tax.rate))
                self.tax_amount = Decimal(value=self.gross_amount - self.net_amount)

        self.invoice_number = f"Invoice_{self.buyer_details.username}_{date.today().year}_{self.buyer_details.profile.contract.total_invoices + 1}"
        self.payment_method = self.buyer_details.profile.contract.payment_method
        self.payment_due_date = self.issue_date + timedelta(days=7)

        self.buyer_details.profile.contract.total_invoices += 1
        self.buyer_details.profile.contract.total_earnings_gross += self.gross_amount
        self.buyer_details.profile.contract.total_earnings_net += self.net_amount
        self.buyer_details.profile.contract.save()

        super(Invoice, self).save(*args, **kwargs)

        if self.invoice_file and self.invoice_file.file:
            original_filename = self.invoice_file.file.name
            new_filename = f"Invoice_{self.buyer_details.profile.basic_information.firstname}_{self.buyer_details.profile.basic_information.lastname}_{date.today().year}_{self.buyer_details.profile.contract.total_invoices + 1}.{self.invoice_file.format}"

            new_file_path = os.path.join("invoices/invoices", new_filename)

            if default_storage.exists(original_filename):
                default_storage.save(new_file_path, self.invoice_file.file)
                default_storage.delete(original_filename)
                self.invoice_file.file.name = new_file_path
                self.invoice_file.save()

        self.buyer_details.profile.contract.invoices.add(self)
        self.buyer_details.profile.contract.save()

        super(Invoice, self).save(*args, **kwargs)
