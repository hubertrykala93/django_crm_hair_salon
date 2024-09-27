import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
            user = authenticate(
                username=User.objects.get(email=request.POST["email"]).username,
                password=request.POST["password"],
            )

            if user.is_verified:
                if user is not None:
                    if "remember" in request.POST:
                        request.session["user_id"] = user.id
                        request.session.set_expiry(value=1000000)
                        request.session.modified = True

                    login(
                        request=request,
                        user=user,
                    )

                    messages.success(
                        request=request,
                        message="You have been logged in successfully.",
                    )

                    return redirect(to="dashboard")

            else:
                messages.info(
                    request=request,
                    message="Your account has not been activated yet. Please activate your account to log in.",
                )

    else:
        form = LoginForm()

    return render(
        request=request,
        template_name="accounts/login.html",
        context={
            "title": "Login",
            "form": form,
        }
    )


@login_required(login_url="home")
def dashboard(request):
    return render(
        request=request,
        template_name="core/dashboard.html",
        context={
            "title": "Dashboard",
        },
    )


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
def contact_us(request):
    form = ContactUsForm(data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            firstname, lastname, email, subject, message = [
                request.POST["firstname"].strip(),
                request.POST["lastname"].strip(),
                request.POST["email"].strip(),
                request.POST["subject"].strip(),
                request.POST["message"].strip()
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
