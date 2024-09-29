from django import forms
from .models import CryptoTransfer, PayPalTransfer, BankTransfer, PrepaidTransfer, PaymentMethod, CryptoCurrency, \
    Transaction
from django.core.exceptions import ValidationError


class AdminPaymentMethodForm(forms.ModelForm):
    name = forms.CharField(
        help_text="Select the payment method.",
        label="Payment Method",
        required=True,
    )

    class Meta:
        model = PaymentMethod
        fields = "__all__"


class AdminCryptoCurrencyForm(forms.ModelForm):
    name = forms.CharField(
        help_text="Enter the crypto currency.",
        label="Crypto Currency Name",
        required=True,
    )

    class Meta:
        model = CryptoCurrency
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

    def __init__(self, *args, **kwargs):
        super(AdminCryptoTransferForm, self).__init__(*args, **kwargs)

        self.fields["cryptocurrency"].help_text = "Select your cryptocurrency."
        self.fields["cryptocurrency"].label = "Cryptocurrency"
        self.fields["cryptocurrency"].required = True


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
    swift = forms.CharField(
        help_text="Enter your SWIFT.",
        label="SWIFT",
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
    owner_name = forms.CharField(
        help_text="Enter the card owner full name.",
        label="Owner",
        required=True,
    )
    card_number = forms.CharField(
        help_text="Enter your prepaid card number for transfers.",
        label="Card Number",
        required=True,
    )
    expiration_date = forms.DateField(
        help_text="Enter the expiration date.",
        label="Expiration Date",
        required=True,
    )

    class Meta:
        model = PrepaidTransfer
        fields = "__all__"


class AdminTransactionForm(forms.ModelForm):
    description = forms.CharField(
        help_text="Enter the transaction description.",
        label="Description",
        required=False,
    )
    amount = forms.IntegerField(
        help_text="Enter the amount.",
        label="Amount",
        required=True
    )

    class Meta:
        model = Transaction
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminTransactionForm, self).__init__(*args, **kwargs)

        self.fields["user"].help_text = "Select the user."
        self.fields["payment_method"].help_text = "Select the payment method."

        self.fields["user"].label = "User"
        self.fields["payment_method"].label = "Payment Method"


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
    swift = forms.CharField(
        error_messages={
            "required": "SWIFT is required.",
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
                message="The IBAN must consist of letters only.",
            )

        if len(iban.replace(" ", "")) < 2:
            raise ValidationError(
                message="The IBAN should contain at least 2 characters.",
            )

        if len(iban.replace(" ", "")) > 10:
            raise ValidationError(
                message="The IBAN should contain a maximum of 10 characters.",
            )

        return iban

    def clean_swift(self):
        swift = self.cleaned_data.get("swift").strip()

        if not swift.replace(" ", "").isalnum():
            raise ValidationError(
                message="The SWIFT must consist of letters or digits only.",
            )

        if len(swift.replace(" ", "")) < 8:
            raise ValidationError(
                message="The SWIFT should contain at least 8 characters.",
            )

        if len(swift.replace(" ", "")) > 11:
            raise ValidationError(
                message="The SWIFT should contain a maximum of 11 characters.",
            )

        return swift


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
