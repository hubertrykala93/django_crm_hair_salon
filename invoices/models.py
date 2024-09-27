from django.db import models
from django.utils.timezone import now
from core.models import Company
from accounts.models import Profile
from payments.models import PaymentMethod


class VatRate(models.Model):
    rate = models.IntegerField(unique=True)

    class Meta:
        verbose_name = "Vat Rate"
        verbose_name_plural = "Vat Rates"

    def __str__(self):
        return str(self.rate)


class InvoiceDetails(models.Model):
    issue_date = models.DateTimeField(default=now)
    invoice_number = models.CharField(max_length=100, unique=True)
    sellers_details = models.OneToOneField(to=Company, on_delete=models.CASCADE)
    buyers_details = models.OneToOneField(to=Profile, on_delete=models.CASCADE)
    description_of_product_or_services = models.CharField(max_length=1000, unique=True)
    unit_net_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.ForeignKey(to=VatRate, on_delete=models.CASCADE)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_due_date = models.DateField()

    # payment_method = models.ForeignKey(to=PaymentMethod, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
        return self.invoice_number


class Invoice(models.Model):
    file = models.FileField(upload_to="core/invoices")
    invoice_details = models.ForeignKey(to=InvoiceDetails, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):
        return str(self.pk)
