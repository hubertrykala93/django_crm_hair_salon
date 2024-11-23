from django import forms
from django.core.exceptions import ValidationError
from accounts.models import User, ProfileContactInformation
from contracts.models import ContractType, JobPosition, JobType, PaymentFrequency, Currency
import re
from datetime import date
from datetime import datetime


class EmployeeRegisterForm(forms.Form):
    email = forms.CharField(
        error_messages={
            "required": "Email is required.",
        },
    )
    firstname = forms.CharField(
        error_messages={
            "required": "Firstname is required.",
        },
    )
    lastname = forms.CharField(
        error_messages={
            "required": "Lastname is required",
        },
    )
    date_of_birth = forms.CharField(
        error_messages={
            "required": "Date of Birth is required.",
        },
    )
    phone_number = forms.CharField(
        error_messages={
            "required": "Phone Number is required.",
        },
    )
    country = forms.CharField(
        error_messages={
            "required": "Country is required",
        },
    )
    province = forms.CharField(
        error_messages={
            "required": "Province is required.",
        },
    )
    city = forms.CharField(
        error_messages={
            "required": "City is required.",
        },
    )
    postal_code = forms.CharField(
        error_messages={
            "required": "Postal Code is required.",
        },
    )
    street = forms.CharField(
        error_messages={
            "required": "Street is required.",
        },
    )
    house_number = forms.CharField(
        error_messages={
            "required": "House Number is required.",
        },
    )
    apartment_number = forms.CharField(
        required=False,
    )
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
    work_hours_per_week = forms.CharField(
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
    salary = forms.CharField(
        error_messages={
            "required": "Salary is required.",
        }
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
        email = self.cleaned_data.get("email").strip()

        if len(email) > 255:
            raise ValidationError(
                message="The e-mail address cannot be longer than 255 characters.",
            )

        if not re.match(pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                        string=email):
            raise ValidationError(
                message="The e-mail address format is invalid.",
            )

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

    def clean_firstname(self):
        firstname = self.cleaned_data.get("firstname").strip()

        if len(firstname) < 2:
            raise ValidationError(
                message="The firstname should contain at least 2 characters.",
            )

        if len(firstname) > 50:
            raise ValidationError(
                message="The firstname should contain a maximum of 50 characters.",
            )

        if not firstname.isalpha():
            raise ValidationError(
                message="The firstname should consist of letters only.",
            )

        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data.get("lastname").strip()

        if len(lastname) < 2:
            raise ValidationError(
                message="The lastname should contain at least 2 characters."
            )

        if len(lastname) > 100:
            raise ValidationError(
                message="The lastname should contain a maximum of 100 characters.",
            )

        if not lastname.isalpha():
            raise ValidationError(
                message="The lastname should consist of letters only.",
            )

        return lastname

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth").strip()

        try:
            date_object = datetime.strptime(date_of_birth, '%Y-%m-%d').date()

        except ValueError:
            raise ValidationError(
                message="Date of Birth must be in the format YYYY-MM-DD.",
            )

        if date_object >= date.today():
            raise ValidationError(
                message="The date of birth cannot be greater than or equal to the current date.",
            )

        if not re.match(pattern="^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", string=date_of_birth):
            raise ValidationError(
                message="Date must be in the format YYYY-MM-DD.",
            )

        return date_of_birth

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number").strip()

        if not re.compile(r"^\d{8,15}$").match(phone_number):
            raise ValidationError(
                message="Invalid phone number format. Please enter a valid number with the country code (e.g., 11234567890 for the USA).",
            )

        if self.instance is None:
            if ProfileContactInformation.objects.filter(phone_number=phone_number).exists():
                raise ValidationError(
                    message="This phone number is already in use; please enter a different one.",
                )

        else:
            if self.instance.phone_number != phone_number:
                if ProfileContactInformation.objects.filter(phone_number=phone_number).exists():
                    raise ValidationError(
                        message=f"This phone number is already in use; please enter a different one.",
                    )

        return phone_number

    def clean_country(self):
        country = self.cleaned_data.get("country").strip()

        if len(country) < 4:
            raise ValidationError(
                message="The country should contain at least 4 characters.",
            )

        if len(country) > 56:
            raise ValidationError(
                message="The country should contain a maximum of 56 characters.",
            )

        if not country.isalpha():
            raise ValidationError(
                message="The country should consist of letters only.",
            )

        return country

    def clean_province(self):
        province = self.cleaned_data.get("province").strip()

        if len(province) < 3:
            raise ValidationError(
                message="The province should contain at least 3 characters.",
            )

        if len(province) > 23:
            raise ValidationError(
                message="The province should contain a maximum of 23 characters.",
            )

        if not province.isalpha():
            raise ValidationError(
                message="The province should consist of letters only.",
            )

        return province

    def clean_city(self):
        city = self.cleaned_data.get("city").strip()

        if len(city) > 85:
            raise ValidationError(
                message="The city should contain a maximum of 85 characters.",
            )

        if not city.isalpha():
            raise ValidationError(
                message="The city should consist of letters only.",
            )

        return city

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get("postal_code").strip()

        if len(postal_code) < 3:
            raise ValidationError(
                message="The postal code should contain at least 3 characters.",
            )

        if len(postal_code) > 10:
            raise ValidationError(
                message="The postal code should contain a maximum of 10 characters.",
            )

        if not postal_code.isalnum():
            raise ValidationError(
                message="The postal code should consist of letters or digits only.",
            )

        return postal_code

    def clean_street(self):
        street = self.cleaned_data.get("street").strip()

        if len(street) > 58:
            raise ValidationError(
                message="The city should contain a maximum of 58 characters.",
            )

        if not street.isalpha():
            raise ValidationError(
                message="The city should consist of letters only.",
            )

        return street

    def clean_house_number(self):
        house_number = self.cleaned_data.get("house_number").strip()

        if len(house_number) > 10:
            raise ValidationError(
                message="The house number should contain a maximum of 10 characters.",
            )

        if not house_number.isalnum():
            raise ValidationError(
                message="The house number should consist of letters or digits only."
            )

        return house_number

    def clean_apartment_number(self):
        apartment_number = self.cleaned_data.get("apartment_number").strip()

        if apartment_number:
            if len(apartment_number) > 10:
                raise ValidationError(
                    message="The apartment number should contain a maximum of 10 characters.",
                )

            if not apartment_number.isalnum():
                raise ValidationError(
                    message="The apartment number should consist of letters or digits only.",
                )

        return apartment_number

    def clean_work_hours_per_week(self):
        work_hours_per_week = self.cleaned_data.get("work_hours_per_week", None)

        if work_hours_per_week:
            if not work_hours_per_week.isdigit():
                raise ValidationError(
                    message="A number is required.",
                )

            if int(work_hours_per_week) > 168:
                raise ValidationError(
                    message="Work hours per week must be less than 168.",
                )

        return work_hours_per_week

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

    def clean_salary(self):
        salary = self.cleaned_data.get("salary").strip()

        try:
            salary = float(salary)

        except ValueError:
            raise ValidationError(
                message="Enter a number.",
            )

        return salary
