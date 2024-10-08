from django import forms
from .models import ContractType, Contract, Benefit, SportBenefit, HealthBenefit, InsuranceBenefit, DevelopmentBenefit, \
    JobType, EmploymentStatus, JobPosition, Currency, PaymentFrequency
from payments.models import PaymentMethod
from django.core.exceptions import ValidationError
from datetime import datetime, date
import re


class AdminCurrencyForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of currency", label="Currency Name", required=True)
    slug = forms.SlugField(required=False)

    class Meta:
        model = Currency
        fields = "__all__"


class AdminPaymentFrequencyForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of payment frequency.", label="Payment Frequency", required=True)
    slug = forms.SlugField(required=False)

    class Meta:
        model = PaymentFrequency
        fields = "__all__"


class AdminJobTypeForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of job type.", label="Job Type", required=True)
    slug = forms.SlugField(required=False)

    class Meta:
        model = JobType
        fields = "__all__"


class AdminSportBenefitForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of sport benefit.", label="Sport Benefit", required=True)
    slug = forms.SlugField(required=False)

    class Meta:
        model = SportBenefit
        fields = "__all__"


class AdminHealthBenefitForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of health benefit.", label="Benefit Name", required=True)
    slug = forms.SlugField(required=False)

    class Meta:
        model = HealthBenefit
        fields = "__all__"


class AdminInsuranceBenefitForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of insurance benefit.", label="Benefit Name", required=True)
    slug = forms.SlugField(required=False)

    class Meta:
        model = InsuranceBenefit
        fields = "__all__"


class AdminDevelopmentBenefitForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of development benefit.", label="Benefit Name",
                           required=True)
    slug = forms.SlugField(required=False)

    class Meta:
        model = DevelopmentBenefit
        fields = "__all__"


class AdminBenefitForm(forms.ModelForm):
    class Meta:
        model = Benefit
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminBenefitForm, self).__init__(*args, **kwargs)

        self.fields["sport_benefits"].help_text = "Select sports benefits."
        self.fields["sport_benefits"].label = "Sport Benefits"
        self.fields["sport_benefits"].required = False

        self.fields["health_benefits"].help_text = "Select health benefits."
        self.fields["health_benefits"].label = "Health Benefits"
        self.fields["health_benefits"].required = False

        self.fields["insurance_benefits"].help_text = "Select insurance benefits."
        self.fields["insurance_benefits"].label = "Insurance Benefits"
        self.fields["insurance_benefits"].required = False

        self.fields["development_benefits"].help_text = "Select development benefits."
        self.fields["development_benefits"].label = "Development Benefits"
        self.fields["development_benefits"].required = False


class AdminContractTypeForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of the contract type.", label="Contract Name", required=True)
    slug = forms.SlugField(required=False)

    class Meta:
        model = ContractType
        fields = "__all__"


class AdminJobPositionForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of job position.", label="Job Position", required=True)
    slug = forms.SlugField(required=False)

    class Meta:
        model = JobPosition
        fields = "__all__"


class AdminEmploymentStatusForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of employment status.", label="Status", required=True)
    slug = forms.SlugField(required=False)

    class Meta:
        model = EmploymentStatus
        fields = "__all__"


class AdminContractForm(forms.ModelForm):
    start_date = forms.DateField(help_text="Enter the start of the contract.", label="Start Date", required=True)
    end_date = forms.DateField(help_text="Enter the end of the contract.", label="End Date", required=False)
    salary = forms.DecimalField(help_text="Enter the salary.", label="Contract Salary", required=True)
    work_hours_per_week = forms.IntegerField(help_text="Enter the number of working hours per week.",
                                             label="Working Hours", required=False)
    total_invoices = forms.IntegerField(
        required=False,
    )

    class Meta:
        model = Contract
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminContractForm, self).__init__(*args, **kwargs)

        self.fields["contract_type"].help_text = "Select the type of contract."
        self.fields["contract_type"].label = "Contract Type"
        self.fields["contract_type"].required = True

        self.fields["job_type"].help_text = "Select the type of job."
        self.fields["job_type"].label = "Job Type"
        self.fields["job_type"].required = True

        self.fields["job_position"].help_text = "Select the job position"
        self.fields["job_position"].label = "Job Position"
        self.fields["job_position"].required = True

        self.fields["currency"].help_text = "Select the currency."
        self.fields["currency"].label = "Currency"
        self.fields["currency"].required = True

        self.fields["benefits"].help_text = "Select benefits."
        self.fields["benefits"].label = "Benefits"
        self.fields["benefits"].required = False

        self.fields["payment_frequency"].help_text = "Select payment frequency."
        self.fields["payment_frequency"].label = "Payment Frequency"
        self.fields["payment_frequency"].required = True

        self.fields["payment_method"].queryset = PaymentMethod.objects.all()
        self.fields["payment_method"].help_text = "Select payment method."
        self.fields["payment_method"].label = "Payment Method"
        self.fields["payment_method"].required = False

        self.fields["status"].help_text = "Select the employment status."
        self.fields["status"].label = "Status"
        self.fields["status"].required = True

        self.fields["invoices"].help_text = "Select the invoices."
        self.fields["invoices"].label = "Invoices"
        self.fields["invoices"].required = False

    def clean_end_date(self):
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")

        if end_date < start_date:
            raise ValidationError(
                message="The Start Date cannot be earlier than the End Date.",
            )

        return end_date


class ContractForm(forms.ModelForm):
    contract_type = forms.ModelChoiceField(
        error_messages={
            "required": "Contract Type is required.",
        },
        queryset=ContractType.objects.none(),
    )
    job_type = forms.ModelChoiceField(
        error_messages={
            "required": "Job Type is required.",
        },
        queryset=JobType.objects.none(),
    )
    job_position = forms.ModelChoiceField(
        error_messages={
            "required": "Job Position is required.",
        },
        queryset=JobPosition.objects.none(),
    )
    payment_frequency = forms.ModelChoiceField(
        error_messages={
            "required": "Payment Frequency is required.",
        },
        queryset=PaymentFrequency.objects.none(),
    )
    status = forms.ModelChoiceField(
        error_messages={
            "required": "Status is required.",
        },
        queryset=EmploymentStatus.objects.none(),
    )
    work_hours_per_week = forms.IntegerField(
        error_messages={
            "invalid": "A number is required.",
            "max_value": "Work hours per week must be less than 168.",
        },
        max_value=168,
        required=False,
    )
    currency = forms.ModelChoiceField(
        error_messages={
            "required": "Currency is required.",
        },
        queryset=Currency.objects.none(),
    )
    start_date = forms.CharField(
        error_messages={
            "required": "Start Date is required.",
        },
    )
    end_date = forms.CharField(
        required=False,
    )
    salary = forms.DecimalField(
        decimal_places=2,
        max_digits=10,
        error_messages={
            "required": "Salary is required.",
            "invalid": "A number is required.",
            "max_digits": "The maximum number of digits cannot exceed 10.",
            "max_whole_digits": "The salary cannot have more than 8 digits before the decimal point.",
            "max_decimal_places": "The salary can have a maximum of 2 decimal places.",
        },
    )

    class Meta:
        model = Contract
        fields = [
            "contract_type",
            "job_type",
            "job_position",
            "start_date",
            "end_date",
            "salary",
            "currency",
            "payment_frequency",
            "work_hours_per_week",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)

        self.fields["contract_type"].queryset = ContractType.objects.all()
        self.fields["job_type"].queryset = JobType.objects.all()
        self.fields["job_position"].queryset = JobPosition.objects.all()
        self.fields["payment_frequency"].queryset = PaymentFrequency.objects.all()
        self.fields["status"].queryset = EmploymentStatus.objects.all()
        self.fields["currency"].queryset = Currency.objects.all()

    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date").strip()

        if not re.match(pattern="^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", string=start_date):
            raise ValidationError(
                message="Start Date must be in the format YYYY-MM-DD.",
            )

        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get("end_date").strip()

        if end_date:
            try:
                date_object = datetime.strptime(end_date, '%Y-%m-%d').date()

            except ValueError:
                raise ValidationError(
                    message="End Date must be in the format YYYY-MM-DD.",
                )

            if date_object <= date.today():
                raise ValidationError(
                    message="The end date cannot be less than or equal to the current date.",
                )

            if not re.match(pattern="^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", string=end_date):
                raise ValidationError(
                    message="End Date must be in the format YYYY-MM-DD.",
                )

        return end_date


class BenefitsForm(forms.ModelForm):
    sport_benefits = forms.ModelMultipleChoiceField(
        required=False,
        queryset=SportBenefit.objects.none(),
    )
    health_benefits = forms.ModelMultipleChoiceField(
        required=False,
        queryset=HealthBenefit.objects.none(),
    )
    insurance_benefits = forms.ModelMultipleChoiceField(
        required=False,
        queryset=InsuranceBenefit.objects.none(),
    )
    development_benefits = forms.ModelMultipleChoiceField(
        required=False,
        queryset=DevelopmentBenefit.objects.none(),
    )

    class Meta:
        model = Benefit
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(BenefitsForm, self).__init__(*args, **kwargs)

        self.fields["sport_benefits"].queryset = SportBenefit.objects.all()
        self.fields["health_benefits"].queryset = HealthBenefit.objects.all()
        self.fields["insurance_benefits"].queryset = InsuranceBenefit.objects.all()
        self.fields["development_benefits"].queryset = DevelopmentBenefit.objects.all()
