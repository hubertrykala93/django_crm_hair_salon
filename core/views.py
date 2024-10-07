import os
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from accounts.models import User
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .forms import LoginForm, ContactUsForm
from accounts.forms import RegisterForm, BasicInformationForm, ContactInformationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags


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


@login_required(login_url="index")
@user_passes_test(test_func=lambda user: user.is_staff, login_url="dashboard")
def register_employee(request, form):
    user = User(
        email=form.cleaned_data.get("email"),
    )
    user.is_active = False

    user.set_password(raw_password=user.generate_password())
    user.save()

    request.session["registered_user"] = user.id
    request.session.modified = True


@login_required(login_url="index")
@user_passes_test(test_func=lambda user: user.is_staff, login_url="dashboard")
def update_basic_information(request, form):
    user = User.objects.get(pk=request.session["registered_user"])

    if user.profile.basic_information:
        user.profile.basic_information.firstname = form.cleaned_data.get("firstname")
        user.profile.basic_information.lastname = form.cleaned_data.get("lastname")
        user.profile.basic_information.date_of_birth = form.cleaned_data.get("date_of_birth")

    user.profile.basic_information.save()
    user.profile.save()

    request.session["basic_information"] = user.profile.basic_information.id
    request.session.modified = True


@login_required(login_url="index")
@user_passes_test(test_func=lambda user: user.is_staff, login_url="dashboard")
def update_contact_information(request, form):
    user = User.objects.get(pk=request.session["registered_user"])

    if user.profile.contact_information:
        user.profile.contact_information.phone_number = form.cleaned_data.get("phone_number")
        user.profile.contact_information.country = form.cleaned_data.get("country")
        user.profile.contact_information.province = form.cleaned_data.get("province")
        user.profile.contact_information.city = form.cleaned_data.get("city")
        user.profile.contact_information.postal_code = form.cleaned_data.get("postal_code")
        user.profile.contact_information.street = form.cleaned_data.get("street")
        user.profile.contact_information.house_number = form.cleaned_data.get("house_number")
        user.profile.contact_information.apartment_number = form.cleaned_data.get("apartment_number")

    user.profile.contact_information.save()
    user.profile.save()

    request.session["contact_information"] = user.profile.contact_information.id
    request.session.modified = True


@login_required(login_url="index")
def dashboard(request):
    register_form = RegisterForm()
    basic_information_form = BasicInformationForm()
    contact_information_form = ContactInformationForm()

    registered_user = None

    if request.session.get("registered_user"):
        try:
            registered_user = User.objects.get(pk=request.session["registered_user"])

        except User.DoesNotExist:
            pass

    if request.method == "POST":
        if 'register-employee' in request.POST:
            register_form = RegisterForm(data=request.POST)

            if register_form.is_valid():
                register_employee(
                    request=request,
                    form=register_form
                )

                try:
                    html_message = render_to_string(
                        template_name="core/account-registration-email.html",
                        context={
                            "email": register_form.cleaned_data.get("email"),
                            "domain": get_current_site(request=request),
                        }
                    )

                    plain_message = strip_tags(html_message)

                    message = EmailMultiAlternatives(
                        subject="Account Registration Request",
                        body=plain_message,
                        from_email=os.environ.get("EMAIL_FROM"),
                        to=[register_form.cleaned_data.get("email")],
                    )

                    message.attach_alternative(
                        content=html_message,
                        mimetype="text/html",
                    )
                    message.send()

                    return redirect(to=reverse(
                        viewname="dashboard") + f"?register-employee={request.session['registered_user'] if request.session.get('registered_user') else ''}&tab=basic-information")

                except Exception as e:
                    messages.error(
                        request=request,
                        message="Failed to send the registration email, please try again.",
                    )

        if "basic-information" in request.POST:
            basic_information_form = BasicInformationForm(
                data=request.POST,
            )

            if basic_information_form.is_valid():
                update_basic_information(
                    request=request,
                    form=basic_information_form
                )

            return redirect(to=reverse(
                viewname="dashboard") + f"?register-employee={request.session['registered_user'] if request.session.get('registered_user') else ''}&basic-information={request.session['basic_information'] if request.session.get('basic_information') else ''}&tab=contact-information")

        if "contact-information" in request.POST:
            contact_information_form = ContactInformationForm(
                data=request.POST,
                instance=registered_user.profile.contact_information,
            )

            if contact_information_form.is_valid():
                update_contact_information(
                    request=request,
                    form=contact_information_form,
                )

                return redirect(to=reverse(
                    viewname="dashboard") + f"?register-employee={request.session['registered_user'] if request.session.get('registered_user') else ''}&basic-information={request.session['basic_information'] if request.session.get('basic_information') else ''}&contact-information={request.session['contact_information'] if request.session.get('contact_information') else ''}&tab=contract-information")

    return render(
        request=request,
        template_name="core/dashboard.html",
        context={
            "title": "Dashboard",
            "users": User.objects.exclude(email__in=["admin@gmail.com", "hubert.rykala@gmail.com"]),
            "registered_user": registered_user,
            "register_form": register_form,
            "basic_information_form": basic_information_form,
            "contact_information_form": contact_information_form,
        },
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
