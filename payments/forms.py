from django import forms
from .models import CryptoTransfer, PayPalTransfer, BankTransfer, PrepaidTransfer, PaymentMethod


class AdminPaymentMethodForm(forms.ModelForm):
    name = forms.CharField(
        help_text="Enter the name of the payment method.",
        label="Payment Method",
        required=True,
    )

    class Meta:
        model = PaymentMethod
        fields = "__all__"


class AdminCryptoTransferForm(forms.ModelForm):
    name = forms.CharField(
        help_text="Enter your Crypto Transfer name.",
        label="Transfer Name",
        required=True,
    )
    wallet_address = forms.CharField(
        help_text="Enter the wallet address for cryptocurrency payments.",
        label="Wallet Address",
        required=True
    )

    class Meta:
        model = CryptoTransfer
        fields = "__all__"


class AdminPayPalTransferForm(forms.ModelForm):
    paypal_email = forms.CharField(
        help_text="Enter the email address associated with your PayPal account.",
        label="PayPal E-mail Address",
        required=True,
    )

    class Meta:
        model = PayPalTransfer
        fields = "__all__"


class AdminBankTransferForm(forms.ModelForm):
    bank_name = forms.CharField(
        help_text="Enter the name of your bank institution.",
        label="Bank Name",
        required=False,
    )
    iban = forms.CharField(
        help_text="Enter your IBAN.",
        label="IBAN",
        required=True,
    )
    account_number = forms.CharField(
        help_text="Enter your bank account number.",
        label="Account Number",
        required=True,
    )

    class Meta:
        model = BankTransfer
        fields = "__all__"


class AdminPrepaidTransferForm(forms.ModelForm):
    card_number = forms.CharField(
        help_text="Enter your prepaid card number for transfers.",
        label="Card Number",
        required=True,
    )

    class Meta:
        model = PrepaidTransfer
        fields = "__all__"
