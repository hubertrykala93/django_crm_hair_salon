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

        if start_date and end_date:
            if end_date < start_date:
                raise ValidationError(
                    message="The Start Date cannot be earlier than the End Date.",
                )

        return end_date


class BenefitsForm(forms.Form):
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

    def __init__(self, *args, **kwargs):
        super(BenefitsForm, self).__init__(*args, **kwargs)

        self.fields["sport_benefits"].queryset = SportBenefit.objects.all()
        self.fields["health_benefits"].queryset = HealthBenefit.objects.all()
        self.fields["insurance_benefits"].queryset = InsuranceBenefit.objects.all()
        self.fields["development_benefits"].queryset = DevelopmentBenefit.objects.all()
