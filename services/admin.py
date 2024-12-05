from django.contrib import admin
from .models import ServiceCategory, ServiceTaxRate, Service, ServiceImage
from .forms import AdminServiceCategoryForm, AdminServiceTaxRateForm, AdminServiceForm, AdminServiceImageForm


@admin.register(ServiceCategory)
class AdminServiceCategory(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
    ]
    form = AdminServiceCategoryForm
    fieldsets = (
        (
            "Category Name", {
                "fields": [
                    "name",
                ],
            },
        ),
    )


@admin.register(ServiceTaxRate)
class AdminServiceTaxRate(admin.ModelAdmin):
    list_display = [
        "id",
        "rate",
    ]
    form = AdminServiceTaxRateForm
    fieldsets = (
        (
            "Tax Rate", {
                "fields": [
                    "rate",
                ],
            },
        ),
    )

@admin.register(ServiceImage)
class AdminServiceImage(admin.ModelAdmin):
    list_display = [
        "id",
        "image",
        "size",
        "width",
        "height",
        "format",
        "alt",
    ]
    form = AdminServiceImageForm
    fieldsets = (
        (
            "Uploading", {
                "fields": [
                    "image",
                ],
            },
        ),
        (
            "Alternate Text", {
                "fields": [
                    "alt",
                ],
            },
        ),
    )
@admin.register(Service)
class AdminService(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "image",
        "slug",
        "get_employees",
        "description",
        "category",
        "duration",
        "tax_rate",
        "net_price",
        "gross_price",
        "is_active",
    ]
    form = AdminServiceForm
    fieldsets = (
        (
            "Service Information", {
                "fields": [
                    "name",
                    "description",
                    "category",
                    "duration",
                ],
            },
        ),
        (
            "Uploading", {
                "fields": [
                    "image",
                ],
            },
        ),
        (
            "Service Providers", {
                "fields": [
                    "employees",
                ],
            },
        ),
        (
            "Service Costs", {
                "fields": [
                    "net_price",
                    "tax_rate",
                ],
            },
        ),
        (
            "Service Availability", {
                "fields": [
                    "is_active",
                ],
            },
        ),
    )

    def get_employees(self, obj):
        if obj.employees:
            return [employee for employee in obj.employees.all()]

    get_employees.short_description = "Providers"
