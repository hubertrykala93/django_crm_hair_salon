import os
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from accounts.models import User
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .forms import LoginForm, ContactUsForm


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
def index(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data.get("email"))

            except User.DoesNotExist:
                form.add_error(
                    field="email",
                    error=f"A user with the email address '{form.cleaned_data.get('email')}' does not exist.",
                )

            if not user.is_active:
                messages.info(
                    request=request,
                    message=f"Your account is inactive. If you were registered by an administrator, check your inbox and follow the steps provided in the email. If not, please <strong><a href='{request.build_absolute_uri(reverse(viewname='contact-us'))}'>contact</a></strong> the administrator directly.",
                )

                return redirect(to="index")

            if not user.check_password(raw_password=request.POST["password"]):
                form.add_error(
                    field="password",
                    error=f"Incorrect password for the account '{form.cleaned_data.get('email')}'.",
                )

            auth_user = authenticate(
                username=User.objects.get(email=form.cleaned_data.get("email")).username,
                password=request.POST["password"],
            )

            if auth_user is not None:
                if "remember" in request.POST:
                    request.session["user_id"] = auth_user.id
                    request.session.set_expiry(value=1000000)
                    request.session.modified = True

                login(
                    request=request,
                    user=auth_user,
                )

                required_basic_fields = (
                        auth_user.profile.basic_information.firstname is not None and
                        auth_user.profile.basic_information.lastname is not None and
                        auth_user.profile.basic_information.date_of_birth is not None
                )

                required_contact_fields = (
                        auth_user.profile.contact_information.phone_number is not None and
                        auth_user.profile.contact_information.country is not None and
                        auth_user.profile.contact_information.province is not None and
                        auth_user.profile.contact_information.city is not None and
                        auth_user.profile.contact_information.postal_code is not None and
                        auth_user.profile.contact_information.street is not None and
                        auth_user.profile.contact_information.house_number is not None
                )

                if not required_basic_fields or not required_contact_fields or not auth_user.profile.contract.payment_method:
                    messages.warning(
                        request=request,
                        message=f"To receive transfers and have access to full functionality, complete the information in the <strong><a href='{request.build_absolute_uri(reverse(viewname='settings'))}'>Settings</a></strong> tab and set up a payment method.",
                    )

                messages.success(
                    request=request,
                    message="You have been logged in successfully.",
                )

                return redirect(to="dashboard")

    else:
        form = LoginForm()

    return render(
        request=request,
        template_name="core/index.html",
        context={
            "title": "Login",
            "form": form,
        }
    )


def contact_us(request):
    form = ContactUsForm(data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            firstname, lastname, email, subject, message = [
                form.cleaned_data.get("firstname"),
                form.cleaned_data.get("lastname"),
                form.cleaned_data.get("email"),
                form.cleaned_data.get("subject"),
                form.cleaned_data.get("message")
            ]

            try:
                html_message = render_to_string(
                    template_name="contact-us-mail.html",
                    context={
                        "firstname": firstname,
                        "lastname": lastname,
                        "email": email,
                        "subject": subject,
                        "message": message,
                    }
                )

                message = EmailMultiAlternatives(
                    subject=subject,
                    body=html_message,
                    from_email=os.environ.get("EMAIL_FROM"),
                    to=[os.environ.get("EMAIL_HOST_USER")],
                )

                message.send()

                messages.success(
                    request=request,
                    message="The message has been sent, we will respond to you shortly.",
                )

            except Exception as e:
                messages.error(
                    request=request,
                    message="Failed to send the email, please try again.",
                )

    return render(
        request=request,
        template_name="contact-us.html",
        context={
            "title": "Contact Us",
            "form": form,
        }
    )
