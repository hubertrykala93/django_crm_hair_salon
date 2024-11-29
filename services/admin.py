from django.contrib import admin
from .models import ServiceCategory, ServiceTaxRate, Service
from .forms import AdminServiceCategoryForm, AdminServiceTaxRateForm, AdminServiceForm


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


@admin.register(Service)
class AdminService(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
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
                    "gross_price",
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
            return [employee for employee in obj.employees]

    get_employees.short_description = "Providers"
