from django.db import models
from django.utils.timezone import now
from uuid import uuid4


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"

    def __str__(self):
        return self.name


class BankTransfer(PaymentMethod):
    user = models.OneToOneField(to="accounts.User", on_delete=models.CASCADE, null=True)
    bank_name = models.CharField(max_length=100)
    iban = models.CharField(max_length=10)
    swift = models.CharField(max_length=20, null=True)
    account_number = models.CharField(max_length=50, unique=True, null=True)

    class Meta:
        verbose_name = "Bank Transfer"
        verbose_name_plural = "Bank Transfers"

    def __str__(self):
        return str(self.account_number)


class PrepaidTransfer(PaymentMethod):
    user = models.OneToOneField(to="accounts.User", on_delete=models.CASCADE, null=True)
    owner_name = models.CharField(max_length=255, null=True)
    card_number = models.CharField(max_length=100, unique=True, null=True)
    expiration_date = models.DateField(null=True)

    class Meta:
        verbose_name = "Prepaid Transfer"
        verbose_name_plural = "Prepaid Transfers"

    def __str__(self):
        return str(self.card_number)


class PayPalTransfer(PaymentMethod):
    user = models.OneToOneField(to="accounts.User", on_delete=models.CASCADE, null=True)
    paypal_email = models.EmailField(max_length=255, unique=True, null=True)

    class Meta:
        verbose_name = "PayPal Transfer"
        verbose_name_plural = "PayPal Transfers"

    def __str__(self):
        return str(self.paypal_email)


class CryptoCurrency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True, null=True)

    class Meta:
        verbose_name = "Crypto Currency"
        verbose_name_plural = "Crypto Currencies"

    def __str__(self):
        return self.name


class CryptoTransfer(PaymentMethod):
    user = models.OneToOneField(to="accounts.User", on_delete=models.CASCADE, null=True)
    cryptocurrency = models.ForeignKey(to=CryptoCurrency, on_delete=models.SET_NULL, null=True)
    wallet_address = models.CharField(max_length=255, unique=True, null=True)

    class Meta:
        verbose_name = "Crypto Transfer"
        verbose_name_plural = "Crypto Transfers"

    def __str__(self):
        return str(self.wallet_address)


class Transaction(models.Model):
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_id = models.UUIDField(default=uuid4, unique=True)
    user = models.ForeignKey(to="accounts.User", on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=100)
    payment_method = models.ForeignKey(to=PaymentMethod, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=(
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Failed", "Failed"),
            ("Canceled", "Canceled"),
        )
    )

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Transaction {self.transaction_id} sent to {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.description:
            self.description = f"{self.payment_method.name.split(sep=' ')[0]} Transfer to {self.payment_method.name.split(sep=' ')[-1]}"

        if not self.status:
            self.status = "Completed"

        super(Transaction, self).save(*args, **kwargs)
