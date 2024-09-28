from django import forms
from .models import CryptoTransfer, PayPalTransfer, BankTransfer, PrepaidTransfer, PaymentMethod
from django.core.exceptions import ValidationError
from accounts.models import User


class AdminPaymentMethodForm(forms.ModelForm):
    name = forms.CharField(
        help_text="Select the payment method.",
        label="Payment Method",
        required=True,
    )
    active = forms.BooleanField(
        help_text="Check if this payment method is active.",
        label="Active",
        required=False,
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


class UpdateBankTransferForm(forms.ModelForm):
    bank_name = forms.CharField(
        error_messages={
            "required": "Bank Name is required.",
        },
        required=True,
    )
    iban = forms.CharField(
        error_messages={
            "required": "IBAN is required.",
        },
        required=True,
    )
    account_number = forms.CharField(
        error_messages={
            "required": "Account Number is required.",
        },
        required=True,
    )

    class Meta:
        model = BankTransfer
        exclude = ["name"]

    def clean_bank_name(self):
        bank_name = self.cleaned_data.get("bank_name")

        if not bank_name.replace(" ", "").isalpha():
            raise ValidationError(
                message="The bank name must consist of letters only.",
            )

        if len(bank_name) < 2:
            raise ValidationError(
                message="The bank name should contain at least 2 characters.",
            )

        if len(bank_name) > 255:
            raise ValidationError(
                message="The bank name should contain a maximum of 255 characters.",
            )

        return bank_name

    def clean_iban(self):
        iban = self.cleaned_data.get("iban").strip()

        if not iban.replace(" ", "").isalpha():
            raise ValidationError(
                message="The iban must consist of letters only.",
            )

        if len(iban.replace(" ", "")) < 2:
            raise ValidationError(
                message="The iban should contain at least 2 characters.",
            )

        if len(iban.replace(" ", "")) > 10:
            raise ValidationError(
                message="The iban should contain a maximum of 10 characters.",
            )

        return iban

    def clean_account_number(self):
        account_number = self.cleaned_data.get("account_number")

        if not account_number.replace(" ", "").isdigit():
            raise ValidationError(
                message="The iban must consist of digits only.",
            )

        if len(account_number.replace(" ", "")) < 8:
            raise ValidationError(
                message="The account number should contain at least 8 characters.",
            )

        if len(account_number.replace(" ", "")) > 30:
            raise ValidationError(
                message="The account number should contain a maximum of 30 characters.",
            )

        if hasattr(self.instance.payment_method, "banktransfer"):
            if self.instance.payment_method.banktransfer.account_number != account_number:
                print("!=")
                if BankTransfer.objects.filter(account_number=account_number).exists():
                    raise ValidationError(
                        message="This bank account number already exists; please provide a different one.",
                    )

        return account_number


class UpdatePrepaidTransferForm(forms.ModelForm):
    class Meta:
        model = PrepaidTransfer
        fields = "__all__"


class UpdatePayPalTransferForm(forms.ModelForm):
    class Meta:
        model = PayPalTransfer
        fields = "__all__"


class UpdateCryptoTransferForm(forms.ModelForm):
    class Meta:
        model = CryptoTransfer
        fields = "__all__"
