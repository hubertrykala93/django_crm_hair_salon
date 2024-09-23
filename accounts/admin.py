from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Profile, ProfileImage, OneTimePassword, ProfileBasicInformation, ProfileContactInformation, \
    ProfileEmploymentInformation, JobPosition, EmploymentStatus, Contract
from .forms import AdminRegisterForm, AdminProfileForm, AdminProfileImageForm, AdminOneTimePasswordForm, \
    AdminProfileBasicInformationForm, AdminProfileContactInformationForm, AdminProfileEmploymentInformationForm, \
    AdminJobPositionForm, AdminEmploymentStatusForm, AdminContractForm
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
            "Basic", {
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
            "Basic", {
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
        "name",
        "start_date",
        "end_date",
        "duration",
        "salary",
        "work_hours_per_week",
    ]
    form = AdminContractForm
    fieldsets = (
        (
            "Contract Name", {
                "fields": [
                    "name",
                ],
            },
        ),
        (
            "Dates", {
                "fields": [
                    "start_date",
                    "end_date",
                    "duration",
                ],
            },
        ),
        (
            "Paycheck", {
                "fields": [
                    "salary",
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
    )


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
            "Employment Information", {
                "fields": [
                    "job_position",
                    "employment_status",
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


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "formatted_basicinformation",
        "formatted_contactinformation",
        "formatted_employmentinformation",
        "get_profile_image",
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
                    "basicinformation",
                ],
            },
        ),
        (
            "Contact Information", {
                "fields": [
                    "contactinformation",
                ],
            },
        ),
        (
            "Employment Information", {
                "fields": [
                    "employmentinformation",
                ],
            },
        ),
    )

    def formatted_basicinformation(self, obj):
        if obj.basicinformation:
            return obj.basicinformation

    formatted_basicinformation.short_description = "Basic Information"

    def formatted_contactinformation(self, obj):
        if obj.contactinformation:
            return obj.contactinformation

    formatted_contactinformation.short_description = "Contact Information"

    def formatted_employmentinformation(self, obj):
        if obj.employmentinformation:
            return obj.employmentinformation

    formatted_employmentinformation.short_description = "Employment Information"

    def get_profile_image(self, obj):
        if obj.basicinformation.profile_image:
            return obj.basicinformation.profile_image

    get_profile_image.short_description = "Profile Image"


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
