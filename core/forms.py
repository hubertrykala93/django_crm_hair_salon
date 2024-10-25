from django import forms
from django.core.exceptions import ValidationError
from accounts.models import User
import re


class LoginForm(forms.Form):
    email = forms.CharField(
        error_messages={
            "required": "Email is required.",
        },
    )
    password = forms.CharField(
        error_messages={
            "required": "Password is required.",
        }
    )
    remember = forms.BooleanField(
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email").strip()

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
        email = self.data.get("email").strip()
        password = self.cleaned_data.get("password")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if not user.check_password(raw_password=password):
                raise ValidationError(
                    message=f"Incorrect password for the account '{email}'.",
                )

        return password


class ContactUsForm(forms.Form):
    firstname = forms.CharField(
        error_messages={
            "required": "Firstname is required.",
        }
    )
    lastname = forms.CharField(
        error_messages={
            "required": "Lastname is required.",
        }
    )
    email = forms.CharField(
        error_messages={
            "required": "Email is required.",
        }
    )
    subject = forms.CharField(
        error_messages={
            "required": "Subject is required.",
        }
    )
    message = forms.CharField(
        error_messages={
            "required": "Message is required.",
        }
    )

    def clean_firstname(self):
        firstname = self.cleaned_data.get("firstname").strip()

        if len(firstname) < 2:
            raise ValidationError(
                message="The firstname should contain at least 2 characters.",
            )

        if len(firstname) > 50:
            raise ValidationError(
                message="The firstname should contain a maximum of 50 characters.",
            )

        if not firstname.isalpha():
            raise ValidationError(
                message="The firstname should consist of letters only.",
            )

        return firstname

    def clean_lastname(self):
        lastname = self.cleaned_data.get("lastname").strip()

        if len(lastname) < 2:
            raise ValidationError(
                message="The lastname should contain at least 2 characters."
            )

        if len(lastname) > 100:
            raise ValidationError(
                message="The lastname should contain a maximum of 100 characters.",
            )

        if not lastname.isalpha():
            raise ValidationError(
                message="The lastname should consist of letters only.",
            )

        return lastname

    def clean_email(self):
        email = self.cleaned_data.get("email").strip()

        if len(email) > 255:
            raise ValidationError(
                message="The e-mail address cannot be longer than 255 characters.",
            )

        if not re.match(pattern=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                        string=email):
            raise ValidationError(
                message="The e-mail address format is invalid.",
            )

        return email

    def clean_subject(self):
        subject = self.cleaned_data.get("subject").strip()

        if len(subject) < 10:
            raise ValidationError(
                message="The subject should contain at least 10 characters.",
            )

        if len(subject) > 50:
            raise ValidationError(
                message="The lastname should contain a maximum of 50 characters.",
            )

        return subject

    def clean_message(self):
        message = self.cleaned_data.get("message").strip()

        if len(message) < 20:
            raise ValidationError(
                message="The message should contain at least 20 characters.",
            )

        if len(message) > 500:
            raise ValidationError(
                message="The message should contain a maximum of 500 characters.",
            )

        return message
