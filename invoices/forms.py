from django import forms
from .models import IncomeTaxRate, InvoiceFile, Invoice, InvoiceStatus
from django.core.exceptions import ValidationError


class AdminIncomeTaxRateForm(forms.ModelForm):
    rate = forms.DecimalField(
        help_text="Enter the income tax rate.",
        label="Rate",
        required=True,
    )

    class Meta:
        model = IncomeTaxRate
        fields = "__all__"


class AdminInvoiceFileForm(forms.ModelForm):
    class Meta:
        model = InvoiceFile
        exclude = ["size"]

    def __init__(self, *args, **kwargs):
        super(AdminInvoiceFileForm, self).__init__(*args, **kwargs)

        self.fields["file"].help_text = "Upload an invoice."
        self.fields["file"].label = "Invoice"
        self.fields["file"].required = True

    def clean_file(self):
        file = self.cleaned_data.get("file")

        if file.name.split(sep=".")[-1] != "pdf":
            raise ValidationError(
                message="Unsupported file format; please upload a file in 'pdf' format.",
            )

        return file


class AdminInvoiceStatusForm(forms.ModelForm):
    name = forms.CharField(
        help_text="Select the invoice status.",
        label="Invoice Status",
        required=True,
    )

    class Meta:
        model = InvoiceStatus
        fields = "__all__"


class AdminInvoiceForm(forms.ModelForm):
    description_of_product_or_services = forms.CharField(
        help_text="Enter the name of product of services.",
        label="Product or Services",
        required=True,
    )

    class Meta:
        model = Invoice
        exclude = [
            "issue_date",
            "invoice_number",
            "payment_method",
            "gross_amount",
            "net_amount",
            "tax_amount",
            "payment_due_date",
            "quantity",
        ]

    def __init__(self, *args, **kwargs):
        super(AdminInvoiceForm, self).__init__(*args, **kwargs)

        self.fields["invoice_file"].help_text = "Upload or select an invoice."
        self.fields["invoice_file"].label = "Invoice File"
        self.fields["invoice_file"].required = True

        self.fields["seller_details"].help_text = "Select the seller."
        self.fields["seller_details"].label = "Seller"
        self.fields["seller_details"].required = True

        self.fields["buyer_details"].help_text = "Select the buyer."
        self.fields["buyer_details"].label = "Buyer"
        self.fields["buyer_details"].required = True

        self.fields["income_tax"].help_text = "Select the income tax amount."
        self.fields["income_tax"].label = "Tax Amount"
        self.fields["income_tax"].required = True
