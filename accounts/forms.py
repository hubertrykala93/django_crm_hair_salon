from django import forms
from .models import User, Profile, ProfileImage
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.hashers import make_password


class AdminRegisterForm(forms.ModelForm):
    email = forms.CharField(
        help_text="Enter e-mail address.",
        label="Email",
        required=True
    )
    password = forms.CharField(
        help_text="Enter password.",
        label="Password", required=True,
        widget=forms.PasswordInput
    )
    is_verified = forms.BooleanField(
        help_text="Check if the user should be verified.",
        required=False
    )
    is_active = forms.BooleanField(
        help_text="Check if the user should be active.",
        required=True
    )
    is_staff = forms.BooleanField(
        help_text="Check if the user should be staff.",
        required=False
    )
    is_superuser = forms.BooleanField(
        help_text="Check if the user should be a superuser.",
        required=False
    )

    class Meta:
        model = User
        exclude = [
            "groups",
            "user_permissions",
        ]

    def save(self, commit=True):
        user = super(AdminRegisterForm, self).save(commit=False)

        if self.cleaned_data["password"]:
            user.password = make_password(password=self.cleaned_data["password"])

        if commit:
            user.save()

        return user


class AdminProfileForm(forms.ModelForm):
    firstname = forms.CharField(help_text="Enter first name.", label="First Name", required=False)
    lastname = forms.CharField(help_text="Enter last name.", label="Last Name", required=False)
    dateofbirth = forms.DateField(help_text="Enter date of birth.", label="Date of Birth", required=False)

    class Meta:
        model = Profile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminProfileForm, self).__init__(*args, **kwargs)

        self.fields["user"].help_text = "Select the user."
        self.fields["profile_image"].help_text = "Select the profile image."

        self.fields["user"].label = "User"
        self.fields["profile_image"].label = "Profile Image"

        self.fields["user"].required = True
        self.fields["profile_image"].required = False


class AdminProfileImageForm(forms.ModelForm):
    image = forms.ImageField(
        help_text="Upload a profile image.",
        label="Profile Image",
        required=False,
    )
    size = forms.IntegerField(
        required=False
    )
    width = forms.IntegerField(
        required=False
    )
    height = forms.IntegerField(
        required=False
    )
    format = forms.CharField(
        required=False,
    )
    alt = forms.CharField(
        widget=forms.Textarea,
        required=True,
    )

    class Meta:
        model = ProfileImage
        fields = [
            "created_at",
            "image",
            "size",
            "width",
            "height",
            "format",
            "alt",
        ]


class RegisterForm(forms.ModelForm):
    email = forms.CharField(
        error_messages={
            "required": "Email is required.",
        }
    )
    password = forms.CharField(
        error_messages={
            "required": "Password is required.",
        },
        widget=forms.PasswordInput,

    )
    repassword = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = ["email", "password", "repassword"]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if len(email) > 255:
            raise ValidationError(
                message="The e-mail address cannot be longer than 255 characters.",
            )

        if not re.match(pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                        string=email):
            raise ValidationError(
                message="The e-mail address format is invalid.",
            )

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                message=f"The user with the e-mail address '{email}' already exists.",
            )

        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 8:
            raise ValidationError(
                message="The password should consist of at least 8 characters.",
            )

        if len(password) > 255:
            raise ValidationError(
                message="The password cannot be longer than 255 characters.",
            )

        if not re.match(pattern="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", string=password):
            raise ValidationError(
                message="The password should contain at least one uppercase letter, one lowercase letter, one number, "
                        "and one special character.",
            )

        return password

    def clean_repassword(self):
        password = self.cleaned_data.get("password")
        repassword = self.cleaned_data.get("repassword")

        if password is not None:
            if not repassword:
                raise ValidationError(
                    message="Confirm Password is required.",
                )

            if repassword != password:
                raise ValidationError(
                    message="Confirm Password does not match.",
                )

        return repassword


class LoginForm(forms.Form):
    email = forms.CharField(
        error_messages={
            "required": "Email is required.",
        },
    )
    password = forms.CharField(
        error_messages={
            "required": "Password is required.",
        },
        widget=forms.PasswordInput,
    )
    remember = forms.BooleanField(
        required=False,
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            user = User.objects.get(email=email)

            if not user.is_verified:
                self.add_error(
                    field=None,
                    error="Your account has not been activated yet. Please activate your account to log in.",
                )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if len(email) > 255:
            raise ValidationError(
                message="The e-mail address cannot be longer than 255 characters.",
            )

        if not re.match(pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                        string=email):
            raise ValidationError(
                message="The e-mail address format is invalid.",
            )

        if not User.objects.filter(email=email).exists():
            raise ValidationError(
                message=f"A user with the email address '{email}' does not exist.",
            )

        return email

    def clean_password(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if not user.check_password(raw_password=password):
                raise ValidationError(
                    message=f"Incorrect password for the account '{email}'.",
                )

        return password


class PasswordResetForm(forms.Form):
    email = forms.CharField(
        error_messages={
            "required": "Email is required.",
        }
    )
    password = forms.CharField(
        error_messages={
            "required": "Password is required.",
        },
        widget=forms.PasswordInput,
        required=False,
    )
    repassword = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if len(email) > 255:
            raise ValidationError(
                message="The e-mail address cannot be longer than 255 characters.",
            )

        if not re.match(pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                        string=email):
            raise ValidationError(
                message="The e-mail address format is invalid.",
            )

        if not User.objects.filter(email=email).exists():
            raise ValidationError(
                message=f"A user with the email address '{email}' does not exist.",
            )

        return email
