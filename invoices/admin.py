from django.contrib import admin
from .models import IncomeTaxRate, InvoiceFile, Invoice, InvoiceStatus
from .forms import AdminIncomeTaxRateForm, AdminInvoiceFileForm, AdminInvoiceForm, AdminInvoiceStatusForm


@admin.register(IncomeTaxRate)
class AdminIncomeTaxRate(admin.ModelAdmin):
    list_display = [
        "id",
        "rate",
    ]
    form = AdminIncomeTaxRateForm
    fieldsets = (
        (
            "Tax Rate", {
                "fields": [
                    "rate",
                ],
            },
        ),
    )


@admin.register(InvoiceFile)
class AdminInvoiceFile(admin.ModelAdmin):
    list_display = [
        "id",
        "file",
        "format",
        "size",
    ]
    form = AdminInvoiceFileForm
    fieldsets = (
        (
            "Invoice File", {
                "fields": [
                    "file",
                ],
            },
        ),
    )


@admin.register(InvoiceStatus)
class AdminInvoiceStatus(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]
    form = AdminInvoiceStatusForm
    fieldsets = (
        (
            "Status", {
                "fields": [
                    "name",
                ],
            },
        ),
    )


@admin.register(Invoice)
class AdminInvoice(admin.ModelAdmin):
    list_display = [
        "id",
        "formatted_issue_date",
        "invoice_number",
        "invoice_file",
        "payment_method",
        "formatted_seller_details",
        "formatted_buyer_details",
        "formatted_description_of_product_or_services",
        "net_amount",
        "income_tax",
        "tax_amount",
        "gross_amount",
        "formatted_payment_due_date",
        "status",
    ]
    form = AdminInvoiceForm
    fieldsets = (
        (
            "Invoice", {
                "fields": [
                    "invoice_file",
                ],
            },
        ),
        (
            "Contractors", {
                "fields": [
                    "seller_details",
                    "buyer_details",
                ],
            },
        ),
        (
            "Product or Services", {
                "fields": [
                    "description_of_product_or_services",
                ],
            },
        ),
        (
            "Tax Amount", {
                "fields": [
                    "income_tax",
                ],
            },
        ),
        (
            "Status", {
                "fields": [
                    "status",
                ],
            },
        ),
    )

    def formatted_issue_date(self, obj):
        if obj.issue_date:
            return obj.issue_date.strftime("%Y-%m-%d %H:%M:%S")

    formatted_issue_date.short_description = "Issue Date"

    def formatted_payment_due_date(self, obj):
        if obj.payment_due_date:
            return obj.payment_due_date.strftime("%Y-%m-%d")

    formatted_payment_due_date.short_description = "Payment Due Date"

    def formatted_seller_details(self, obj):
        return obj.seller_details

    formatted_seller_details.short_description = "Seller"

    def formatted_buyer_details(self, obj):
        return obj.buyer_details

    formatted_buyer_details.short_description = "Buyer"

    def formatted_description_of_product_or_services(self, obj):
        return obj.description_of_product_or_services

    formatted_description_of_product_or_services.short_description = "Product or Services"
