from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from accounts.models import User, ProfileContactInformation
from contracts.models import ContractType, JobPosition, JobType, PaymentFrequency, Currency
from datetime import date


class EmployeeRegisterForm(forms.Form):
    email = forms.CharField(
        min_length=5,
        max_length=255,
        help_text="It must contain at least 5 characters and no more than 255 characters.",
        strip=True,
        validators=[
            RegexValidator(
                regex=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                message="The e-mail address format is invalid.",
            ),
        ],
        error_messages={
            "required": "Email is required.",
            "min_length": "The e-mail address cannot be longer than 255 characters.",
            "max_length": "The e-mail address cannot be shorter than 5 characters.",
        },
    )
    firstname = forms.CharField(
        min_length=2,
        max_length=50,
        help_text="It must contain only letters and be between 2 and 50 characters long.",
        strip=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z]+$",
                message="The firstname should consist of letters only.",
            ),
        ],
        error_messages={
            "required": "Firstname is required.",
            "min_length": "The firstname should contain at least 2 characters.",
            "max_length": "The firstname should contain a maximum of 50 characters.",
        },
    )
    lastname = forms.CharField(
        min_length=2,
        max_length=100,
        help_text="It must contain only letters and be between 2 and 100 characters long.",
        strip=True,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z]+$",
                message="The lastname should consist of letters only.",
            ),
        ],
        error_messages={
            "required": "Lastname is required",
            "min_length": "The lastname should contain at least 2 characters.",
            "max_length": "The lastname should contain a maximum of 50 characters.",
        },
    )
    date_of_birth = forms.DateField(
        help_text="It must be in the format YYYY-MM-DD, cannot be earlier than 1990-01-01, "
                  "and cannot be later than the current date.",
        validators=[
            MinValueValidator(
                limit_value=date(year=1900, month=1, day=1),
                message="The date of birth cannot be earlier than 1990-01-01.",
            ),
            MaxValueValidator(
                limit_value=date.today(),
                message="The date of birth cannot be greater than or equal to the current date.",
            ),
        ],
        input_formats=[
            "%Y-%m-%d"
        ],
        error_messages={
            "required": "Date of Birth is required.",
            "invalid": "The date of birth must be in the format YYYY-MM-DD and must be a valid calendar date.",
        },
    )
    phone_number = forms.CharField(
        min_length=8,
        max_length=15,
        help_text="It must contain only digits and be between 8 and 15 characters long.",
        strip=True,
        validators=[
            RegexValidator(
                regex=r"^\d{8,15}$",
                message="Invalid phone number format. "
                        "Please enter a valid number with the country code (e.g., 11234567890 for the USA).",
            ),
        ],
        error_messages={
            "required": "Phone Number is required.",
            "min_length": "The phone number should contain at least 8 characters.",
            "max_length": "The phone number should contain a maximum of 15 characters.",
        },
    )
    country = forms.CharField(
        min_length=4,
        max_length=56,
        help_text="It must contain only letters and be between 4 and 56 characters long.",
        strip=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z\s]+$",
                message="The country should consist of letters only.",
            ),
        ],
        error_messages={
            "required": "Country is required",
            "min_length": "The country should contain at least 4 characters.",
            "max_length": "The country should contain a maximum of 56 characters.",
        },
    )
    province = forms.CharField(
        min_length=3,
        max_length=23,
        help_text="It must contain only letters and be between 3 and 23 characters long.",
        strip=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z\s]+$",
                message="The province should consist of letters only.",
            ),
        ],
        error_messages={
            "required": "Province is required.",
            "min_length": "The province should contain at least 3 characters.",
            "max_length": "The province should contain a maximum of 23 characters.",
        },
    )
    city = forms.CharField(
        min_length=1,
        max_length=85,
        help_text="It must contain only letters and be between 1 and 85 characters long.",
        strip=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z\s]+$",
                message="The city should consist of letters only.",
            ),
        ],
        error_messages={
            "required": "City is required.",
            "min_length": "The city should contain at least 1 character.",
            "max_length": "The city should contain a maximum of 85 characters.",
        },
    )
    postal_code = forms.CharField(
        min_length=3,
        max_length=10,
        help_text="It must contain only digits and/or letters and be between 3 and 10 characters long.",
        strip=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9]+$",
                message="The postal code should consist of letters or digits only.",
            ),
        ],
        error_messages={
            "required": "Postal Code is required.",
            "min_length": "The postal code should contain at least 3 characters.",
            "max_length": "The postal code should contain a maximum of 10 characters.",
        },
    )
    street = forms.CharField(
        min_length=1,
        max_length=58,
        help_text="It must contain only letters and be between 1 and 58 characters long.",
        strip=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z\s]+$",
                message="The street should consist of letters only.",
            ),
        ],
        error_messages={
            "required": "Street is required.",
            "min_length": "The street should contain at least 1 characters.",
            "max_length": "The street should contain a maximum of 58 characters.",
        },
    )
    house_number = forms.CharField(
        min_length=1,
        max_length=10,
        help_text="It must contain only digits and/or letters and be between 1 and 10 characters long.",
        strip=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9]+$",
                message="The house number should consist of letters or digits only.",
            ),
        ],
        error_messages={
            "required": "House Number is required.",
            "min_length": "The house number should contain at least 1 characters.",
            "max_length": "The house number should contain a maximum of 10 characters.",
        },
    )
    apartment_number = forms.CharField(
        required=False,
        min_length=1,
        max_length=10,
        help_text="It must contain only digits and/or letters and be between 1 and 10 characters long.",
        strip=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9]+$",
                message="The apartment number should consist of letters or digits only.",
            ),
        ],
        error_messages={
            "min_length": "The apartment number should contain at least 1 characters.",
            "max_length": "The apartment number should contain a maximum of 10 characters.",
        },
    )
    contract_type = forms.ModelChoiceField(
        queryset=ContractType.objects.none(),
        help_text="Select one item from the list.",
        error_messages={
            "required": "Contract Type is required.",
        },
    )
    job_type = forms.ModelChoiceField(
        queryset=JobType.objects.none(),
        help_text="Select one item from the list.",
        error_messages={
            "required": "Job Type is required.",
        },
    )
    job_position = forms.ModelChoiceField(
        queryset=JobPosition.objects.none(),
        help_text="Select one item from the list.",
        error_messages={
            "required": "Job Position is required.",
        },
    )
    payment_frequency = forms.ModelChoiceField(
        queryset=PaymentFrequency.objects.none(),
        help_text="Select one item from the list.",
        error_messages={
            "required": "Payment Frequency is required.",
        },
    )
    work_hours_per_week = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=168,
        help_text="It must contain only digits and be between 0 and 168 inclusive.",
        error_messages={
            "max_value": "Work hours per week must be less than 168.",
            "invalid": "The work hours per week should consist of digits only.",
        },
    )
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.none(),
        help_text="Select one item from the list.",
        error_messages={
            "required": "Currency is required.",
        },
    )
    start_date = forms.DateField(
        help_text="It must be in the format YYYY-MM-DD, cannot be earlier than 1990-01-01, "
                  "and cannot be later than 2100-01-01.",
        validators=[
            MinValueValidator(
                limit_value=date(year=1900, month=1, day=1),
                message="The start date cannot be earlier than 1990-01-01.",
            ),
            MaxValueValidator(
                limit_value=date(year=2100, month=1, day=1),
                message="The start date cannot be greater than 2100-01-01.",
            ),
        ],
        input_formats=[
            "%Y-%m-%d"
        ],
        error_messages={
            "required": "Start Date is required.",
            "invalid": "The start date must be in the format YYYY-MM-DD and must be a valid calendar date.",
        },
    )
    end_date = forms.DateField(
        required=False,
        help_text="It must be in the format YYYY-MM-DD, cannot be earlier than current date, "
                  "and cannot be later than 2100-01-01.",
        validators=[
            MinValueValidator(
                limit_value=date.today(),
                message="The end date cannot be earlier than current date.",
            ),
            MaxValueValidator(
                limit_value=date(year=2100, month=1, day=1),
                message="The end date cannot be greater than 2100-01-01.",
            ),
        ],
        input_formats=[
            "%Y-%m-%d"
        ],
        error_messages={
            "invalid": "The end date must be in the format YYYY-MM-DD and must be a valid calendar date.",
        },
    )
    salary = forms.DecimalField(
        required=True,
        min_value=0,
        max_digits=7,
        decimal_places=2,
        help_text="It must contain a maximum of 7 digits, with 2 decimal places after the decimal point.",
        error_messages={
            "required": "Salary is required.",
            "invalid": "The salary should consist of digits or decimal numbers only.",
        },
    )
    bank_name = forms.CharField(
        min_length=3,
        max_length=35,
        help_text="It must contain only letters and be between 3 and 35 characters long.",
        strip=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z\s]+$",
                message="The bank name should consist of letters only.",
            ),
        ],
        error_messages={
            "required": "Bank Name is required.",
            "min_length": "The bank name should contain at least 3 characters.",
            "max_length": "The bank name should contain a maximum of 35 characters.",
        },
    )
    iban = forms.CharField(
        min_length=2,
        max_length=2,
        help_text="It must consist of only letters and be 2 characters long.",
        strip=True,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z]+$",
                message="The IBAN should consist of letters only.",
            ),
        ],
        error_messages={
            "required": "IBAN is required.",
            "min_length": "The IBAN should contain at least 2 characters.",
            "max_length": "The IBAN should contain a maximum of 2 characters.",
        },
    )
    swift = forms.CharField(
        min_length=8,
        max_length=11,
        help_text="It must contain only digits and/or letters and be between 8 and 11 characters long.",
        strip=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9]+$",
                message="The SWIFT should consist of letters or digits only.",
            ),
        ],
        error_messages={
            "required": "SWIFT is required.",
            "min_length": "The SWIFT should contain at least 8 characters.",
            "max_length": "The SWIFT should contain a maximum of 11 characters.",
        },
    )
    account_number = forms.CharField(
        min_length=4,
        max_length=24,
        help_text="It must contain only digits, be between 4 and 24 characters long, and consist of digits only.",
        strip=True,
        validators=[
            RegexValidator(
                regex=r"^\d+$",
                message="The account number should contain only digits.",
            ),
        ],
        error_messages={
            "required": "Account Number is required.",
            "min_length": "The account number should contain at least 4 characters.",
            "max_length": "The account number should contain a maximum of 24 characters.",
        },
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)

        super(EmployeeRegisterForm, self).__init__(*args, **kwargs)

        self.fields["contract_type"].queryset = ContractType.objects.all()
        self.fields["job_type"].queryset = JobType.objects.all()
        self.fields["job_position"].queryset = JobPosition.objects.all()
        self.fields["payment_frequency"].queryset = PaymentFrequency.objects.all()
        self.fields["currency"].queryset = Currency.objects.all()

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if self.instance is None:
            if User.objects.filter(email=email).exists():
                raise ValidationError(
                    message=f"The user with the e-mail address '{email}' already exists.",
                )

        else:
            if self.instance.email != email:
                if User.objects.filter(email=email).exists():
                    raise ValidationError(
                        message=f"The user with the e-mail address '{email}' already exists.",
                    )

        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        if self.instance is None:
            if ProfileContactInformation.objects.filter(phone_number=phone_number).exists():
                raise ValidationError(
                    message="This phone number is already in use; please enter a different one.",
                )

        else:
            if self.instance.profile.contact_information.phone_number != phone_number:
                if ProfileContactInformation.objects.filter(phone_number=phone_number).exists():
                    raise ValidationError(
                        message=f"This phone number is already in use; please enter a different one.",
                    )

        return phone_number
