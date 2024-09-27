from django import forms
from .models import ContractType, Contract, Benefit, SalaryPeriod, SalaryBenefit, SportBenefit, HealthBenefit, \
    InsuranceBenefit, DevelopmentBenefit, JobType, EmploymentStatus, JobPosition, Currency, PaymentFrequency


class AdminCurrencyForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of currency", label="Currency Name", required=True)

    class Meta:
        model = Currency
        fields = "__all__"


class AdminPaymentFrequencyForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of payment frequency.", label="Payment Frequency", required=True)

    class Meta:
        model = PaymentFrequency
        fields = "__all__"


class AdminJobTypeForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of job type.", label="Job Type", required=True)

    class Meta:
        model = JobType
        fields = "__all__"


class AdminSalaryPeriodForm(forms.ModelForm):
    name = forms.CharField(help_text="Select the salary period.", label="Period Name", required=True)

    class Meta:
        model = SalaryPeriod
        fields = "__all__"


class AdminSalaryBenefitForm(forms.ModelForm):
    date_of_award = forms.DateField(help_text="Enter date of awarded bonus.", label="Date of Award", required=True)
    amount = forms.DecimalField(help_text="Enter the amount of the salary benefit.", label="Amount", required=True)

    class Meta:
        model = SalaryBenefit
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminSalaryBenefitForm, self).__init__(*args, **kwargs)

        self.fields["period"].help_text = "Select the period of the salary benefit."
        self.fields["period"].label = "Period"
        self.fields["period"].required = True


class AdminSportBenefitForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of sport benefit.", label="Sport Benefit", required=True)

    class Meta:
        model = SportBenefit
        fields = "__all__"


class AdminHealthBenefitForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of health benefit.", label="Benefit Name", required=True)

    class Meta:
        model = HealthBenefit
        fields = "__all__"


class AdminInsuranceBenefitForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of insurance benefit.", label="Benefit Name", required=True)

    class Meta:
        model = InsuranceBenefit
        fields = "__all__"


class AdminDevelopmentBenefitForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of development benefit.", label="Benefit Name",
                           required=True)

    class Meta:
        model = DevelopmentBenefit
        fields = "__all__"


class AdminBenefitForm(forms.ModelForm):
    class Meta:
        model = Benefit
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminBenefitForm, self).__init__(*args, **kwargs)

        self.fields["job_type"].help_text = "Select the type of work."
        self.fields["job_type"].label = "Job Type"
        self.fields["job_type"].required = True

        self.fields["salary_benefits"].help_text = "Select bonus benefits."
        self.fields["salary_benefits"].label = "Bonus Benefits"
        self.fields["salary_benefits"].required = False

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

    class Meta:
        model = ContractType
        fields = "__all__"


class AdminJobPositionForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of job position.", label="Job Position", required=True)

    class Meta:
        model = JobPosition
        fields = "__all__"


class AdminEmploymentStatusForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of employment status.", label="Status", required=True)

    class Meta:
        model = EmploymentStatus
        fields = "__all__"


class AdminContractForm(forms.ModelForm):
    start_date = forms.DateField(help_text="Enter the start of the contract.", label="Start Date", required=True)
    end_date = forms.DateField(help_text="Enter the end of the contract.", label="End Date", required=False)
    salary = forms.DecimalField(help_text="Enter the salary.", label="Contract Salary", required=True)
    work_hours_per_week = forms.IntegerField(help_text="Enter the number of working hours per week.",
                                             label="Working Hours", required=False)

    class Meta:
        model = Contract
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminContractForm, self).__init__(*args, **kwargs)

        self.fields["contract_type"].help_text = "Select the type of contract."
        self.fields["contract_type"].label = "Contract Type"
        self.fields["contract_type"].required = True

        self.fields["currency"].help_text = "Select the currency."
        self.fields["currency"].label = "Currency"
        self.fields["currency"].required = True

        self.fields["benefits"].help_text = "Select benefits."
        self.fields["benefits"].label = "Benefits"
        self.fields["benefits"].required = False

        self.fields["payment_frequency"].help_text = "Select payment frequency."
        self.fields["benefits"].label = "Payment Frequency"
        self.fields["benefits"].required = True
