from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, Profile, ProfileImage
from .forms import AdminRegisterForm, AdminProfileForm, AdminProfileImageForm
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


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "firstname",
        "lastname",
        "profile_image",
        "user_type",
        "dateofbirth",
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
                    "firstname",
                    "lastname",
                    "dateofbirth",
                ],
            },
        ),
        (
            "Role", {
                "fields": [
                    "user_type",
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

    def formatted_dateofbirth(self, obj):
        if obj.dateofbirth:
            return obj.dateofbirth.strftime("%Y-%m-%d")

    formatted_dateofbirth.short_description = "Date Of Birth"


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
