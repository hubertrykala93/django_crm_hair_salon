from django import forms
from .models import User, Profile, ProfileImage, OneTimePassword, ProfileBasicInformation, ProfileContactInformation, \
    ProfileEmploymentInformation
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


class AdminOneTimePasswordForm(forms.ModelForm):
    class Meta:
        model = OneTimePassword
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminOneTimePasswordForm, self).__init__(*args, **kwargs)

        self.fields["user"].help_text = "Select the user."
        self.fields["user"].label = "User"
        self.fields["user"].required = True


class AdminProfileBasicInformationForm(forms.ModelForm):
    firstname = forms.CharField(help_text="Enter first name.", label="First Name", required=False)
    lastname = forms.CharField(help_text="Enter last name.", label="Last Name", required=False)
    dateofbirth = forms.DateField(help_text="Enter date of birth.", label="Date of Birth", required=False)
    biography = forms.CharField(help_text="Enter biography.", label="Biography", required=False, widget=forms.Textarea)

    class Meta:
        model = ProfileBasicInformation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminProfileBasicInformationForm, self).__init__(*args, **kwargs)

        self.fields["profileimage"].help_text = "Select the profile image."
        self.fields["profileimage"].label = "Profile Image"
        self.fields["profileimage"].required = False


class AdminProfileContactInformationForm(forms.ModelForm):
    phonenumber = forms.CharField(help_text="Enter phone number.", label="Phone Number", required=False)
    country = forms.CharField(help_text="Enter country.", label="Country", required=False)
    province = forms.CharField(help_text="Enter province.", label="Province", required=False)
    city = forms.CharField(help_text="Enter city.", label="City", required=False)
    street = forms.CharField(help_text="Enter street.", label="Street", required=False)
    housenumber = forms.CharField(help_text="Enter house number.", label="House Number", required=False)
    apartmentnumber = forms.CharField(help_text="Enter apartment number.", label="Apartment Number", required=False)

    class Meta:
        model = ProfileContactInformation
        fields = "__all__"


class AdminProfileEmploymentInformationForm(forms.ModelForm):
    dateofemployment = forms.DateField(help_text="Enter date of employment (YYYY-MM-DD).", label="Date of Employment",
                                       required=True)

    class Meta:
        model = ProfileEmploymentInformation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminProfileEmploymentInformationForm, self).__init__(*args, **kwargs)

        self.fields["usertype"].help_text = "Select user type."
        self.fields["employmentstatus"].help_text = "Select employment status."

        self.fields["usertype"].label = "User Type"
        self.fields["employmentstatus"].label = "Employment Status"

        self.fields["usertype"].required = True
        self.fields["employmentstatus"].required = True


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminProfileForm, self).__init__(*args, **kwargs)

        self.fields["user"].help_text = "Select the user."
        self.fields["user"].label = "User"
        self.fields["user"].required = True

        self.fields["basicinformation"].help_text = "Select the basic information for this user."
        self.fields["basicinformation"].label = "Basic Information"
        self.fields["basicinformation"].required = True

        self.fields["contactinformation"].help_text = "Select the contact information for this user."
        self.fields["contactinformation"].label = "Contact Information"
        self.fields["contactinformation"].required = True

        self.fields["employmentinformation"].help_text = "Select the employment information for this user."
        self.fields["employmentinformation"].label = "Employment Information"
        self.fields["employmentinformation"].required = True


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
    mobile = forms.CharField(
        required=False,
    )
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

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")

        if "email" and "mobile" in self.data:
            if not mobile:
                raise ValidationError(
                    message="Phone Number is required.",
                )

            if not re.compile(r"^\d{8,15}$").match(mobile):
                raise ValidationError(
                    message="Invalid phone number format. Please enter a valid number with the country code (e.g., 11234567890 for the USA).",
                )

        return mobile


def clean_email(self):
    email = self.cleaned_data.get("email")

    if not email:
        raise ValidationError(
            message="Email is required.",
        )

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

    if User.objects.filter(email=email).exists() and not User.objects.get(email=email).is_verified:
        raise ValidationError(
            message=f"Your account has not been verified yet. To reset the password, you must first verify your account.",
        )

    return email


class OneTimePasswordForm(forms.Form):
    email = forms.CharField(
        required=False,
    )
    password = forms.CharField(
        error_messages={
            "required": "One Time Password is required.",
        },
        required=True,
    )

    def clean_password(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        try:
            user = User.objects.get(email=email)
            otp = OneTimePassword.objects.get(user=user)

        except User.DoesNotExist:
            raise ValidationError(
                message=f"A user with the email address '{email}' does not exist.",
            )

        except OneTimePassword.DoesNotExist:
            raise ValidationError(
                message=f"The One Time Password for the user '{email}' does not exist."
            )

        otp = OneTimePassword.objects.get(user=user).password

        if otp != password:
            raise ValidationError(
                message=f"Incorrect One Time Password for the user '{email}'. Please try again.",
            )

        return password


class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(
        error_messages={
            "required": "Password is required.",
        },
        required=True,
        widget=forms.PasswordInput
    )
    repassword = forms.CharField(
        error_messages={
            "required": "Confirm Password is required.",
        },
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "password",
        ]

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
