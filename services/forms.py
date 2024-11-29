from django import forms
from .models import Service, ServiceCategory, ServiceTaxRate
from accounts.models import User


class AdminServiceCategoryForm(forms.ModelForm):
    name = forms.CharField(help_text="Enter the name of service category", label="Name", required=True)
    slug = forms.SlugField(required=False)

    class Meta:
        model = ServiceCategory
        fields = "__all__"


class AdminServiceTaxRateForm(forms.ModelForm):
    rate = forms.DecimalField(help_text="Enter the tax rate.", label="Tax Rate", required=False)

    class Meta:
        model = ServiceTaxRate
        fields = "__all__"


class AdminServiceForm(forms.ModelForm):
    name = forms.CharField(help_text="Provide the name of this service", label="Name", required=True)
    slug = forms.SlugField(required=False)
    description = forms.CharField(help_text="Provide the description of this service.", label="Description",
                                  required=True, widget=forms.Textarea)
    duration = forms.IntegerField(help_text="Provide the duration of this service.", label="Duration", required=True)
    net_price = forms.DecimalField(help_text="Provide the net price of this service.", label="Net Price",
                                   required=False, decimal_places=2, max_digits=5)
    gross_price = forms.DecimalField(help_text="Provie the gross price of this service.", label="Gross Price",
                                     required=False)
    is_active = forms.BooleanField(help_text="Select whether this service is active.", label="Active", required=True)

    class Meta:
        model = Service
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminServiceForm, self).__init__(*args, **kwargs)

        self.fields["employees"].help_text = "Select the employees providing this service."
        self.fields["employees"].label = "Employees"
        self.fields["employees"].required = True

        self.fields["category"].help_text = "Select a category for this service."
        self.fields["category"].label = "Category"
        self.fields["category"].required = True

        self.fields["tax_rate"].help_text = "Select a tax rate for this service."
        self.fields["tax_rate"].label = "Tax Rate"
        self.fields["tax_rate"].required = True
