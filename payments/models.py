from django.db import models


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"

    def __str__(self):
        return self.name


class CryptoTransfer(PaymentMethod):
    wallet_address = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Crypto Transfer"
        verbose_name_plural = "Crypto Transfers"

    def __str__(self):
        return self.wallet_address


class PayPalTransfer(PaymentMethod):
    paypal_email = models.EmailField(max_length=255, unique=True)

    class Meta:
        verbose_name = "PayPal Transfer"
        verbose_name_plural = "PayPal Transfers"

    def __str__(self):
        return self.paypal_email


class BankTransfer(PaymentMethod):
    bank_name = models.CharField(max_length=50)
    iban = models.CharField(max_length=10)
    account_number = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Bank Transfer"
        verbose_name_plural = "Bank Transfers"

    def __str__(self):
        return self.account_number


class PrepaidTransfer(PaymentMethod):
    card_number = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Prepaid Transfer"
        verbose_name_plural = "Prepaid Transfers"

    def __str__(self):
        return self.card_number
