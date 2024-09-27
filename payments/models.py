from django.db import models


class CryptoTransfer(models.Model):
    wallet_address = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Crypto Transfer"
        verbose_name_plural = "Crypto Transfers"


class PayPalTransfer(models.Model):
    paypal_email = models.EmailField(max_length=255)

    class Meta:
        verbose_name = "PayPal Transfer"
        verbose_name_plural = "PayPal Transfers"


class BankTransfer(models.Model):
    bank_name = models.CharField(max_length=50)
    iban = models.CharField(max_length=10)
    account_number = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Bank Transfer"
        verbose_name_plural = "Bank Transfers"


class PrepaidTransfer(models.Model):
    card_number = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Prepaid Transfer"
        verbose_name_plural = "Prepaid Transfers"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
