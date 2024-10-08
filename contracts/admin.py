from django.contrib import admin
from .models import Contract, Benefit, SportBenefit, HealthBenefit, InsuranceBenefit, DevelopmentBenefit, JobType, \
    JobPosition, EmploymentStatus, ContractType, Currency, PaymentFrequency
from .forms import AdminContractForm, AdminBenefitForm, AdminSportBenefitForm, AdminHealthBenefitForm, \
    AdminInsuranceBenefitForm, AdminDevelopmentBenefitForm, AdminJobTypeForm, AdminContractTypeForm, \
    AdminEmploymentStatusForm, AdminJobPositionForm, AdminCurrencyForm, AdminPaymentFrequencyForm


@admin.register(Currency)
class AdminCurrency(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
    ]
    form = AdminCurrencyForm
    fieldsets = (
        (
            "Currency Name", {
                "fields": [
                    "name",
                ],
            },
        ),
    )


@admin.register(PaymentFrequency)
class AdminPaymentFrequency(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
    ]
    form = AdminPaymentFrequencyForm
    fieldsets = (
        (
            "Frequency Name", {
                "fields": [
                    "name",
                ],
            },
        ),
    )


@admin.register(JobType)
class AdminJobType(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
    ]
    form = AdminJobTypeForm
    fieldsets = (
        (
            "Job Type", {
                "fields": [
                    "name",
                ],
            },
        ),
    )


@admin.register(SportBenefit)
class AdminSportBenefit(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
    ]
    form = AdminSportBenefitForm
    fieldsets = (
        (
            "Benefit Name", {
                "fields": [
                    "name",
                ],
            },
        ),
    )


@admin.register(HealthBenefit)
class AdminHealthBenefit(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
    ]
    form = AdminHealthBenefitForm
    fieldsets = (
        (
            "Benefit Name", {
                "fields": [
                    "name",
                ],
            },
        ),
    )


@admin.register(InsuranceBenefit)
class AdminInsuranceBenefit(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
    ]
    form = AdminInsuranceBenefitForm
    fieldsets = (
        (
            "Benefit Name", {
                "fields": [
                    "name",
                ],
            },
        ),
    )


@admin.register(DevelopmentBenefit)
class AdminDevelopmentBenefit(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
    ]
    form = AdminDevelopmentBenefitForm
    fieldsets = (
        (
            "Benefit Name", {
                "fields": [
                    "name",
                ],
            },
        ),
    )


@admin.register(Benefit)
class AdminBenefit(admin.ModelAdmin):
    list_display = [
        "id",
        "get_sport_benefits",
        "get_health_benefits",
        "get_insurance_benefits",
        "get_development_benefits",
    ]
    form = AdminBenefitForm
    fieldsets = (
        (
            "Sport Benefits", {
                "fields": [
                    "sport_benefits",
                ],
            },
        ),
        (
            "Health Benefits", {
                "fields": [
                    "health_benefits",
                ],
            },
        ),
        (
            "Insurance Benefits", {
                "fields": [
                    "insurance_benefits",
                ],
            },
        ),
        (
            "Development Benefits", {
                "fields": [
                    "development_benefits",
                ],
            },
        ),
    )

    def get_sport_benefits(self, obj):
        if obj.sport_benefits:
            return ", ".join([b.name for b in obj.sport_benefits.all()])

    get_sport_benefits.short_description = "Sport Benefits"

    def get_health_benefits(self, obj):
        if obj.health_benefits:
            return ", ".join([b.name for b in obj.health_benefits.all()])

    get_health_benefits.short_description = "Health Benefits"

    def get_insurance_benefits(self, obj):
        if obj.insurance_benefits:
            return ", ".join([b.name for b in obj.insurance_benefits.all()])

    get_insurance_benefits.short_description = "Insurance Benefits"

    def get_development_benefits(self, obj):
        if obj.development_benefits:
            return ", ".join([b.name for b in obj.development_benefits.all()])

    get_development_benefits.short_description = "Development Benefits"


@admin.register(ContractType)
class AdminContractType(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
    ]
    form = AdminContractTypeForm
    fieldsets = (
        (
            "Contract Name", {
                "fields": [
                    "name"
                ],
            },
        ),
    )


@admin.register(JobPosition)
class AdminJobPosition(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    form = AdminJobPositionForm
    fieldsets = (
        (
            "Position", {
                "fields": [
                    "name",
                ],
            },
        ),
    )


@admin.register(EmploymentStatus)
class AdminEmploymentStatus(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    form = AdminEmploymentStatusForm
    fieldsets = (
        (
            "Employment Status", {
                "fields": [
                    "name",
                ],
            },
        ),
    )


@admin.register(Contract)
class AdminContract(admin.ModelAdmin):
    list_display = [
        "id",
        "contract_type",
        "job_type",
        "job_position",
        "formatted_start_date",
        "formatted_end_date",
        "formatted_time_remaining",
        "salary",
        "currency",
        "payment_frequency",
        "payment_method",
        "work_hours_per_week",
        "benefits",
        "status",
        "get_invoices",
        "total_invoices",
        "formatted_total_earnings_gross",
        "formatted_total_earnings_net",
    ]
    form = AdminContractForm
    fieldsets = (
        (
            "Contract Type", {
                "fields": [
                    "contract_type",
                ],
            },
        ),
        (
            "Job Type", {
                "fields": [
                    "job_type",
                ],
            },
        ),
        (
            "Position", {
                "fields": [
                    "job_position",
                ],
            },
        ),
        (
            "Dates", {
                "fields": [
                    "start_date",
                    "end_date",
                ],
            },
        ),
        (
            "Paycheck", {
                "fields": [
                    "salary",
                    "currency",
                    "payment_frequency",
                    "payment_method",
                ],
            },
        ),
        (
            "Working Hours", {
                "fields": [
                    "work_hours_per_week",
                ],
            },
        ),
        (
            "Employment Status", {
                "fields": [
                    "status",
                ],
            },
        ),
        (
            "Benefits", {
                "fields": [
                    "benefits",
                ],
            },
        ),
        (
            "Invoices", {
                "fields": [
                    "invoices",
                ],
            },
        ),
    )

    def formatted_start_date(self, obj):
        if obj.start_date:
            return obj.start_date.strftime("%Y-%m-%d")

    formatted_start_date.short_description = "Start Date"

    def formatted_end_date(self, obj):
        if obj.end_date:
            return obj.end_date.strftime("%Y-%m-%d")

    formatted_end_date.short_description = "End Date"

    def formatted_time_remaining(self, obj):
        if obj.time_remaining:
            return f"{obj.time_remaining.days} days" if obj.time_remaining.days != 1 else f"{obj.time_remaining.days} day"

    formatted_time_remaining.short_description = "Time Remaining"

    def formatted_total_earnings_gross(self, obj):
        return obj.total_earnings_gross

    formatted_total_earnings_gross.short_description = "Gross Earnings"

    def formatted_total_earnings_net(self, obj):
        return obj.total_earnings_net

    formatted_total_earnings_net.short_description = "Net Earnings"

    def get_invoices(self, obj):
        if obj.invoices:
            return len([invoice for invoice in obj.invoices.all()])

    get_invoices.short_description = "Invoices"
