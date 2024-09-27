from django.contrib import admin
from .models import Contract, Benefit, SalaryPeriod, SalaryBenefit, SportBenefit, HealthBenefit, InsuranceBenefit, \
    DevelopmentBenefit, JobType, JobPosition, EmploymentStatus, ContractType, Currency, PaymentFrequency
from .forms import AdminContractForm, AdminBenefitForm, AdminSalaryPeriodForm, AdminSalaryBenefitForm, \
    AdminSportBenefitForm, AdminHealthBenefitForm, AdminInsuranceBenefitForm, AdminDevelopmentBenefitForm, \
    AdminJobTypeForm, AdminContractTypeForm, AdminEmploymentStatusForm, AdminJobPositionForm, AdminCurrencyForm, \
    AdminPaymentFrequencyForm


@admin.register(Currency)
class AdminCurrency(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
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


@admin.register(SalaryPeriod)
class AdminSalaryPeriod(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]
    form = AdminSalaryPeriodForm
    fieldsets = (
        (
            "Period Name", {
                "fields": [
                    "name",
                ],
            },
        ),
    )


@admin.register(SalaryBenefit)
class AdminSalaryBenefit(admin.ModelAdmin):
    list_display = [
        "id",
        "date_of_award",
        "amount",
        "period",
    ]
    form = AdminSalaryBenefitForm
    fieldsets = (
        (
            "Dates", {
                "fields": [
                    "date_of_award",
                ],
            },
        ),
        (
            "Amount", {
                "fields": [
                    "amount",
                ],
            },
        ),
        (
            "Period", {
                "fields": [
                    "period",
                ],
            },
        ),
    )


@admin.register(SportBenefit)
class AdminSportBenefit(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
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
        "job_type",
        "get_salary_benefits",
        "get_sport_benefits",
        "get_health_benefits",
        "get_insurance_benefits",
        "get_development_benefits",
    ]
    form = AdminBenefitForm
    fieldsets = (
        (
            "Job Type", {
                "fields": [
                    "job_type",
                ],
            },
        ),
        (
            "Salary Benefits", {
                "fields": [
                    "salary_benefits",
                ],
            },
        ),
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

    def get_salary_benefits(self, obj):
        if obj.salary_benefits:
            return ", ".join([str(b.amount) for b in obj.salary_benefits.all()])

    get_salary_benefits.short_description = "Salary Benefits"

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
    list_display = ["id", "name"]
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
    list_display = ["id", "name"]
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
        "formatted_start_date",
        "formatted_end_date",
        "salary",
        "currency",
        "payment_frequency",
        "payment_method",
        "work_hours_per_week",
        "benefits",
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
            "Benefits", {
                "fields": [
                    "benefits",
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
