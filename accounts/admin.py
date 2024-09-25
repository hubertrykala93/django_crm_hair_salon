from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Profile, ProfileImage, OneTimePassword, ProfileBasicInformation, ProfileContactInformation, \
    ProfileEmploymentInformation, JobPosition, EmploymentStatus, Contract, ProfilePaymentInformation, PaymentFrequency, \
    Currency, ContractType, Benefit, JobType, SalaryPeriod, SalaryBenefit, DevelopmentBenefit, InsuranceBenefit, \
    HealthBenefit, SportBenefit
from .forms import AdminRegisterForm, AdminProfileForm, AdminProfileImageForm, AdminOneTimePasswordForm, \
    AdminProfileBasicInformationForm, AdminProfileContactInformationForm, AdminProfileEmploymentInformationForm, \
    AdminJobPositionForm, AdminEmploymentStatusForm, AdminContractForm, AdminProfilePaymentInformationForm, \
    AdminPaymentFrequencyForm, AdminCurrencyForm, AdminContractTypeForm, AdminJobTypeForm, AdminSalaryPeriodForm, \
    AdminSalaryBenefitForm, AdminDevelopmentBenefitForm, AdminInsuranceBenefitForm, AdminHealthBenefitForm, \
    AdminSportBenefitForm, AdminBenefitForm
from django.contrib.sessions.models import Session

admin.site.unregister(Group)


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = [
        "id",
        "formatted_date_joined",
        "formatted_last_login",
        "username",
        "password",
        "email",
        "is_verified",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    form = AdminRegisterForm
    fieldsets = (
        (
            "General", {
                "fields": [
                    "email",
                    "password",
                ],
            },
        ),
        (
            "Permissions", {
                "fields": [
                    "is_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ],
            },
        ),
    )

    def formatted_date_joined(self, obj):
        if obj.date_joined:
            return obj.date_joined.strftime("%Y-%m-%d %H:%M:%S")

    formatted_date_joined.short_description = "Date Joined"

    def formatted_last_login(self, obj):
        if obj.last_login:
            return obj.last_login.strftime("%Y-%m-%d %H:%M:%S")

    formatted_last_login.short_description = "Last Login"


@admin.register(OneTimePassword)
class AdminOneTimePassword(admin.ModelAdmin):
    list_display = [
        "id",
        "formatted_created_at",
        "user",
        "password",
    ]
    form = AdminOneTimePasswordForm
    fieldsets = (
        (
            "Related User", {
                "fields": [
                    "user",
                ],
            },
        ),
    )

    def formatted_created_at(self, obj):
        if obj.created_at:
            return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    formatted_created_at.short_description = "Created At"


@admin.register(ProfileBasicInformation)
class AdminProfileBasicInformation(admin.ModelAdmin):
    list_display = [
        "id",
        "get_firstname",
        "get_lastname",
        "biography",
        "formatted_date_of_birth",
        "formatted_profile_image",
    ]
    form = AdminProfileBasicInformationForm
    fieldsets = (
        (
            "Basic Information", {
                "fields": [
                    "firstname",
                    "lastname",
                    "biography",
                    "date_of_birth",
                ],
            },
        ),
        (
            "Uploading", {
                "fields": [
                    "profile_image",
                ],
            },
        ),
    )

    def get_firstname(self, obj):
        if obj.firstname:
            return obj.firstname

    get_firstname.short_description = "First Name"

    def get_lastname(self, obj):
        if obj.lastname:
            return obj.lastname

    get_lastname.short_description = "Last Name"

    def formatted_date_of_birth(self, obj):
        if obj.date_of_birth:
            return obj.date_of_birth.strftime("%Y-%m-%d")

    formatted_date_of_birth.short_description = "Date Of Birth"

    def formatted_profile_image(self, obj):
        if obj.profile_image:
            return obj.profile_image

    formatted_profile_image.short_description = "Profile Image"


@admin.register(ProfileContactInformation)
class AdminProfileContactInformation(admin.ModelAdmin):
    list_display = [
        "id",
        "get_phone_number",
        "country",
        "province",
        "city",
        "postal_code",
        "street",
        "get_house_number",
        "get_apartment_number",
    ]
    form = AdminProfileContactInformationForm
    fieldsets = (
        (
            "Contact Information", {
                "fields": [
                    "phone_number",
                    "country",
                    "province",
                    "city",
                    "postal_code",
                    "street",
                    "house_number",
                    "apartment_number",
                ],
            },
        ),
    )

    def get_phone_number(self, obj):
        if obj.phone_number:
            return obj.phone_number

    get_phone_number.short_description = "Phone Number"

    def get_house_number(self, obj):
        if obj.house_number:
            return obj.house_number

    get_house_number.short_description = "House Number"

    def get_apartment_number(self, obj):
        if obj.apartment_number:
            return obj.apartment_number

    get_apartment_number.short_description = "Apartment Number"


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


@admin.register(Contract)
class AdminContract(admin.ModelAdmin):
    list_display = [
        "id",
        "contract_type",
        "formatted_start_date",
        "formatted_end_date",
        "salary",
        "currency",
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
            return ", ".join([benefit for benefit in obj.salary_benefits.all()])

    get_salary_benefits.short_description = "Salary Benefits"

    def get_sport_benefits(self, obj):
        if obj.sport_benefits:
            return ", ".join([benefit for benefit in obj.sport_benefits.all()])

    get_sport_benefits.short_description = "Sport Benefits"

    def get_health_benefits(self, obj):
        if obj.health_benefits:
            return ", ".join([benefit for benefit in obj.health_benefits.all()])

    get_health_benefits.short_description = "Health Benefits"

    def get_insurance_benefits(self, obj):
        if obj.insurance_benefits:
            return ", ".join([benefit for benefit in obj.insurance_benefits.all()])

    get_insurance_benefits.short_description = "Insurance Benefits"

    def get_development_benefits(self, obj):
        if obj.development_benefits:
            return ", ".join([benefit for benefit in obj.development_benefits.all()])

    get_development_benefits.short_description = "Development Benefits"


@admin.register(ProfileEmploymentInformation)
class AdminProfileEmploymentInformation(admin.ModelAdmin):
    list_display = [
        "id",
        "get_job_position",
        "get_employment_status",
        "contract",
    ]
    form = AdminProfileEmploymentInformationForm
    fieldsets = (
        (
            "Job Position", {
                "fields": [
                    "job_position",
                ],
            },
        ),
        (
            "Employment Status", {
                "fields": [
                    "employment_status",
                ],
            },
        ),
        (
            "Contract", {
                "fields": [
                    "contract",
                ],
            },
        ),
    )

    def get_job_position(self, obj):
        if obj.job_position:
            return obj.job_position

    get_job_position.short_description = "Job Position"

    def get_employment_status(self, obj):
        if obj.employment_status:
            return obj.employment_status

    get_employment_status.short_description = "Employment Status"


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


@admin.register(ProfilePaymentInformation)
class AdminProfilePaymentInformation(admin.ModelAdmin):
    list_display = [
        "id",
        "iban",
        "account_number",
        "payment_frequency",
    ]
    form = AdminProfilePaymentInformationForm
    fieldsets = (
        (
            "International", {
                "fields": [
                    "iban",
                ],
            },
        ),
        (
            "Account Number", {
                "fields": [
                    "account_number",
                ],
            },
        ),
        (
            "Payment Frequency", {
                "fields": [
                    "payment_frequency",
                ],
            },
        ),
    )


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "basic_information",
        "contact_information",
        "employment_information",
        "payment_information",
    ]
    form = AdminProfileForm
    fieldsets = (
        (
            "Related User", {
                "fields": [
                    "user",
                ],
            },
        ),
        (
            "Basic Information", {
                "fields": [
                    "basic_information",
                ],
            },
        ),
        (
            "Contact Information", {
                "fields": [
                    "contact_information",
                ],
            },
        ),
        (
            "Employment Information", {
                "fields": [
                    "employment_information",
                ],
            },
        ),
        (
            "Payment Information", {
                "fields": [
                    "payment_information",
                ],
            },
        ),
    )


@admin.register(ProfileImage)
class AdminProfileImage(admin.ModelAdmin):
    list_display = [
        "id",
        "formatted_created_at",
        "formatted_updated_at",
        "image",
        "size",
        "width",
        "height",
        "format",
        "alt",
    ]
    form = AdminProfileImageForm
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

    def formatted_created_at(self, obj):
        if obj.created_at:
            return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    formatted_created_at.short_description = "Created At"

    def formatted_updated_at(self, obj):
        if obj.updated_at:
            return obj.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    formatted_updated_at.short_description = "Updated At"


@admin.register(Session)
class AdminSession(admin.ModelAdmin):
    list_display = [
        "session_key",
        "decoded_data",
        "expire_date",
    ]

    def decoded_data(self, obj):
        return obj.get_decoded()

    decoded_data.short_description = "Session Data"
