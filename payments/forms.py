from django import forms
from .models import CryptoTransfer, PayPalTransfer, BankTransfer, PrepaidTransfer, PaymentMethod, CryptoCurrency, \
    Transaction
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import datetime, date
import re
from accounts.models import User


class AdminPaymentMethodForm(forms.ModelForm):
    name = forms.CharField(
        help_text="Select the payment method.",
        label="Payment Method",
        required=True,
    )

    class Meta:
        model = PaymentMethod
        fields = "__all__"


class AdminBankTransferForm(forms.ModelForm):
    bank_name = forms.CharField(
        help_text="Enter the name of your bank institution.",
        label="Bank Name",
        required=True,
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

    def __init__(self, *args, **kwargs):
        super(AdminBankTransferForm, self).__init__(*args, **kwargs)

        self.fields["user"].help_text = "Select the user."
        self.fields["user"].label = "User"
        self.fields["user"].required = True


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

    def __init__(self, *args, **kwargs):
        super(AdminPrepaidTransferForm, self).__init__(*args, **kwargs)

        self.fields["user"].help_text = "Select the user."
        self.fields["user"].label = "User"
        self.fields["user"].required = True


class AdminPayPalTransferForm(forms.ModelForm):
    paypal_email = forms.CharField(
        help_text="Enter the email address associated with your PayPal account.",
        label="PayPal E-mail Address",
        required=True,
    )

    class Meta:
        model = PayPalTransfer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminPayPalTransferForm, self).__init__(*args, **kwargs)

        self.fields["user"].help_text = "Select the user."
        self.fields["user"].label = "User"
        self.fields["user"].required = True


class AdminCryptoCurrencyForm(forms.ModelForm):
    name = forms.CharField(
        help_text="Enter the cryptocurrency.",
        label="Cryptocurrency Name",
        required=True,
    )
    code = forms.CharField(
        help_text="Enter the cryptocurrency code.",
        label="Cryptocurrency Code",
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

        self.fields["user"].help_text = "Select the user."
        self.fields["user"].label = "User"
        self.fields["user"].required = True


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


class UpdateBankTransferForm(forms.Form):
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

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)

        super(UpdateBankTransferForm, self).__init__(*args, **kwargs)

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

        if self.instance.account_number != account_number:
            if BankTransfer.objects.filter(account_number=account_number).exists():
                raise ValidationError(
                    message="This bank account number already exists; please provide a different one.",
                )

        return account_number


class UpdatePrepaidTransferForm(forms.Form):
    owner_name = forms.CharField(
        error_messages={
            "required": "Cardholder's name is required.",
        },
        required=True,
    )
    card_number = forms.CharField(
        error_messages={
            "required": "Card Number is required.",
        },
        required=True,
    )
    expiration_date = forms.CharField(
        error_messages={
            "required": "Expiration Date is required.",
        },
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)

        super(UpdatePrepaidTransferForm, self).__init__(*args, **kwargs)

    def clean_owner_name(self):
        owner_name = self.cleaned_data.get("owner_name")

        for name in owner_name.split():
            if not name.isalpha():
                raise ValidationError(
                    message="The cardholder's name must consist of letters only.",
                )

        if len(owner_name) < 2:
            raise ValidationError(
                message="The cardholder's name should contain at least 2 characters.",
            )

        if len(owner_name) > 255:
            raise ValidationError(
                message="The cardholder's name should contain a maximum of 255 characters.",
            )

        return owner_name

    def clean_card_number(self):
        card_number = self.cleaned_data.get("card_number").replace(" ", "").strip()

        if not card_number.isdigit():
            raise ValidationError(
                message="The cardholder's name must consist of digits only.",
            )

        if len(card_number) < 14:
            raise ValidationError(
                message="The card number should contain at least 14 characters.",
            )

        if len(card_number) > 16:
            raise ValidationError(
                message="The card number should contain a maximum of 16 characters.",
            )

        return card_number

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get("expiration_date")
        today = date.today()

        try:
            date_object = datetime.strptime(expiration_date, "%Y-%m-%d").date()

        except ValueError:
            raise ValidationError(
                message="Expiration Date must be in the format YYYY-MM-DD.",
            )

        if date_object < today:
            raise ValidationError(
                message="You cannot provide an inactive card; please provide an active card.",
            )

        if date_object == today:
            raise ValidationError(
                message="Your card expires today; please provide a card with a longer validity period.",
            )

        return expiration_date


class UpdatePayPalTransferForm(forms.Form):
    paypal_email = forms.CharField(
        error_messages={
            "required": "Paypal email address is required.",
        },
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.instance = kwargs.pop("instance", None)

        super(UpdatePayPalTransferForm, self).__init__(*args, **kwargs)

    def clean_paypal_email(self):
        paypal_email = self.cleaned_data.get("paypal_email")

        if len(paypal_email) > 255:
            raise ValidationError(
                message="The paypal e-mail address cannot be longer than 255 characters.",
            )

        if not re.match(pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                        string=paypal_email):
            raise ValidationError(
                message="The paypal e-mail address format is invalid.",
            )

        if self.instance.paypal_email != paypal_email:
            if PayPalTransfer.objects.filter(paypal_email=paypal_email).exists():
                raise ValidationError(
                    message="This paypal e-mail already exists; please provide a different one.",
                )

        if paypal_email != self.user.email:
            if User.objects.filter(email=paypal_email).exists():
                raise ValidationError(
                    message="This email address is already in use; please provide a different one.",
                )

        return paypal_email


class UpdateCryptoTransferForm(forms.Form):
    cryptocurrency = forms.CharField(
        error_messages={
            "required": "Cryptocurrency is required.",
        },
        required=True,
    )
    wallet_address = forms.CharField(
        error_messages={
            "required": "Wallet Address is required.",
        },
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)

        super(UpdateCryptoTransferForm, self).__init__(*args, **kwargs)

    def clean_wallet_address(self):
        cryptocurrency = self.data.get("cryptocurrency", None)
        wallet_address = self.cleaned_data.get("wallet_address")

        if cryptocurrency == "BTC":
            if wallet_address.startswith("1"):
                if len(wallet_address) < 26:
                    raise ValidationError(
                        message="The Bitcoin wallet address should consist of at least 26 characters for the P2PKH network.",
                    )

                elif len(wallet_address) > 35:
                    raise ValidationError(
                        message="The Bitcoin wallet address should consist of at most 35 characters for the P2PKH network.",
                    )

            elif wallet_address.startswith("3"):
                if len(wallet_address) < 26:
                    raise ValidationError(
                        message="The Bitcoin wallet address should consist of at least 26 characters for the P2SH network.",
                    )

                elif len(wallet_address) > 35:
                    raise ValidationError(
                        message="The Bitcoin wallet address should consist of at most 35 characters for the P2SH network.",
                    )

            elif wallet_address.startswith("bc1"):
                if len(wallet_address) < 42:
                    raise ValidationError(
                        message="The Bitcoin wallet address should consist of at least 42 characters for the SegWit network.",
                    )

                elif len(wallet_address) > 62:
                    raise ValidationError(
                        message="The Bitcoin wallet address should consist of at most 62 characters for the SegWit network.",
                    )

            else:
                raise ValidationError(
                    message="Invalid wallet address. The wallet address should start with '1' for the 'P2PKH' network, '3' for the 'P2SH' network, and 'bc1' for the 'SegWit' network.",
                )

        elif cryptocurrency == "ETH":
            if len(wallet_address) == 42:
                if not wallet_address.startswith("0x"):
                    raise ValidationError(
                        message="Invalid wallet address. The wallet address for Ethereum should start with '0x'.",
                    )

            else:
                raise ValidationError(
                    message="The length of the wallet address for Ethereum must be 42 characters.",
                )

        return wallet_address


class BankTransferForm(forms.ModelForm):
    bank_name = forms.CharField(
        error_messages={
            "required": "Bank Name is required.",
        },
    )
    iban = forms.CharField(
        error_messages={
            "required": "IBAN is required.",
        },
    )
    swift = forms.CharField(
        error_messages={
            "required": "SWIFT is required.",
        },
    )
    account_number = forms.CharField(
        error_messages={
            "required": "Account Number is required.",
        }
    )

    class Meta:
        model = BankTransfer
        exclude = ["name", "user"]

    def clean_bank_name(self):
        bank_name = self.cleaned_data.get("bank_name").strip()

        if len(bank_name) < 2:
            raise ValidationError(
                message="The bank name should contain at least 2 characters.",
            )

        if len(bank_name) > 255:
            raise ValidationError(
                message="The bank name should contain a maximum of 255 characters.",
            )

        if not re.match(pattern=r'^[A-Za-z\s]+$', string=bank_name):
            raise ValidationError(
                message="The bank name should contain only letters and spaces.",
            )

        return bank_name

    def clean_iban(self):
        iban = self.cleaned_data.get("iban").strip()

        if len(iban) < 2:
            raise ValidationError(
                message="The IBAN should contain at least 2 characters.",
            )

        if len(iban) > 5:
            raise ValidationError(
                message="The IBAN should contain a maximum of 5 characters.",
            )

        if not re.match(pattern=r'^[A-Za-z\s]+$', string=iban):
            raise ValidationError(
                message="The IBAN should contain only letters.",
            )

        return iban

    def clean_swift(self):
        swift = self.cleaned_data.get("swift").strip()

        if len(swift) < 8:
            raise ValidationError(
                message="The SWIFT should contain at least 8 characters.",
            )

        if len(swift) > 11:
            raise ValidationError(
                message="The SWIFT should contain a maximum of 11 characters.",
            )

        if not re.match(pattern=r'^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$', string=swift):
            raise ValidationError(
                message="The SWIFT must consist of letters or digits only.",
            )

        return swift

    def clean_account_number(self):
        account_number = self.cleaned_data.get("account_number")

        if not account_number.replace(" ", "").isdigit():
            raise ValidationError(
                message="The account number must consist of digits only.",
            )

        if len(account_number.replace(" ", "")) < 8:
            raise ValidationError(
                message="The account number should contain at least 8 characters.",
            )

        if len(account_number.replace(" ", "")) > 30:
            raise ValidationError(
                message="The account number should contain a maximum of 30 characters.",
            )

        if BankTransfer.objects.filter(account_number=account_number).exists():
            raise ValidationError(
                message="This account number already exists; please provide a different one.",
            )

        return account_number


class PrepaidTransferForm(forms.ModelForm):
    owner_name = forms.CharField(
        error_messages={
            "required": "Cardholder's name is required.",
        },
        required=True,
    )
    card_number = forms.CharField(
        error_messages={
            "required": "Card Number is required.",
        },
        required=True,
    )
    expiration_date = forms.CharField(
        error_messages={
            "required": "Expiration Date is required.",
        },
        required=True,
    )

    class Meta:
        model = PrepaidTransfer
        exclude = ["name", "user"]

    def clean_owner_name(self):
        owner_name = self.cleaned_data.get("owner_name").strip()

        if len(owner_name) < 2:
            raise ValidationError(
                message="The cardholder's name should contain at least 2 characters.",
            )

        if len(owner_name) > 255:
            raise ValidationError(
                message="The cardholder's name should contain a maximum of 255 characters.",
            )

        if not re.match(pattern=r'^[A-Za-z\s]+$', string=owner_name):
            raise ValidationError(
                message="The cardholder's name must consist of letters only.",
            )

        return owner_name

    def clean_card_number(self):
        card_number = self.cleaned_data.get("card_number").replace(" ", "").strip()

        if not card_number.isdigit():
            raise ValidationError(
                message="The cardholder's name must consist of digits only.",
            )

        if len(card_number) < 14:
            raise ValidationError(
                message="The card number should contain at least 14 characters.",
            )

        if len(card_number) > 16:
            raise ValidationError(
                message="The card number should contain a maximum of 16 characters.",
            )

        return card_number

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get("expiration_date").strip()
        today = date.today()

        try:
            date_object = datetime.strptime(expiration_date, "%Y-%m-%d").date()

        except ValueError:
            raise ValidationError(
                message="Expiration Date must be in the format YYYY-MM-DD.",
            )

        if date_object < today:
            raise ValidationError(
                message="You cannot provide an inactive card; please provide an active card.",
            )

        if date_object == today:
            raise ValidationError(
                message="Your card expires today; please provide a card with a longer validity period.",
            )

        return expiration_date


class PayPalTransferForm(forms.ModelForm):
    paypal_email = forms.CharField(
        error_messages={
            "required": "Paypal email address is required.",
        },
    )

    class Meta:
        model = PayPalTransfer
        exclude = ["name", "user"]

    def clean_paypal_email(self):
        paypal_email = self.cleaned_data.get("paypal_email").strip()

        if len(paypal_email) > 255:
            raise ValidationError(
                message="The paypal e-mail address cannot be longer than 255 characters.",
            )

        if not re.match(
                pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                string=paypal_email
        ):
            raise ValidationError(
                message="The paypal e-mail address format is invalid.",
            )

        if PayPalTransfer.objects.filter(paypal_email=paypal_email).exists():
            raise ValidationError(
                message="This paypal email already exists; please provide a different one.",
            )

        if User.objects.filter(email=paypal_email).exists():
            raise ValidationError(
                message="This email address is already in use, please provide a different one.",
            )

        return paypal_email


class CryptoTransferForm(forms.ModelForm):
    cryptocurrency = forms.ModelChoiceField(
        error_messages={
            "required": "Cryptocurrency is required.",
        },
        queryset=CryptoCurrency.objects.none(),
    )
    wallet_address = forms.CharField(
        error_messages={
            "required": "Wallet Address is required.",
        },
    )

    class Meta:
        model = CryptoTransfer
        exclude = ["name", "user"]

    def __init__(self, *args, **kwargs):
        super(CryptoTransferForm, self).__init__(*args, **kwargs)

        self.fields["cryptocurrency"].queryset = CryptoCurrency.objects.all()

    def clean_wallet_address(self):
        cryptocurrency_id = self.data.get("cryptocurrency", None)
        wallet_address = self.cleaned_data.get("wallet_address").strip()
        cryptocurrency = CryptoCurrency.objects.get(pk=cryptocurrency_id).code

        if cryptocurrency == "BTC":
            if wallet_address.startswith("1"):
                if len(wallet_address) < 26:
                    raise ValidationError(
                        message="The Bitcoin wallet address should consist of at least 26 characters for the P2PKH network.",
                    )

                elif len(wallet_address) > 35:
                    raise ValidationError(
                        message="The Bitcoin wallet address should consist of at most 35 characters for the P2PKH network.",
                    )

            elif wallet_address.startswith("3"):
                if len(wallet_address) < 26:
                    raise ValidationError(
                        message="The Bitcoin wallet address should consist of at least 26 characters for the P2SH network.",
                    )

                elif len(wallet_address) > 35:
                    raise ValidationError(
                        message="The Bitcoin wallet address should consist of at most 35 characters for the P2SH network.",
                    )

            elif wallet_address.startswith("bc1"):
                if len(wallet_address) < 42:
                    raise ValidationError(
                        message="The Bitcoin wallet address should consist of at least 42 characters for the SegWit network.",
                    )

                elif len(wallet_address) > 62:
                    raise ValidationError(
                        message="The Bitcoin wallet address should consist of at most 62 characters for the SegWit network.",
                    )

            else:
                raise ValidationError(
                    message="Invalid wallet address. The wallet address should start with '1' for the 'P2PKH' network, '3' for the 'P2SH' network, and 'bc1' for the 'SegWit' network.",
                )

        elif cryptocurrency == "ETH":
            if len(wallet_address) == 42:
                if not wallet_address.startswith("0x"):
                    raise ValidationError(
                        message="Invalid wallet address. The wallet address for Ethereum should start with '0x'.",
                    )

            else:
                raise ValidationError(
                    message="The length of the wallet address for Ethereum must be 42 characters.",
                )

        return wallet_address
