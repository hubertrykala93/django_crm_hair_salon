from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Profile, ProfileImage, OneTimePassword, ProfileBasicInformation, ProfileContactInformation
from .forms import AdminRegisterForm, AdminProfileForm, AdminProfileImageForm, AdminOneTimePasswordForm, \
    AdminProfileBasicInformationForm, AdminProfileContactInformationForm
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


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "basic_information",
        "contact_information",
        "contract",
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
            "Contract", {
                "fields": [
                    "contract",
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
