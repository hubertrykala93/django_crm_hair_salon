import os
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from accounts.models import User
from contracts.models import ContractType, JobPosition, JobType, PaymentFrequency, Currency, SportBenefit, \
    HealthBenefit, InsuranceBenefit, DevelopmentBenefit
from payments.models import CryptoCurrency
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .forms import LoginForm, ContactUsForm
from accounts.forms import RegisterForm, BasicInformationForm, ContactInformationForm
from contracts.forms import ContractForm, BenefitsForm
from payments.forms import BankTransferForm, PrepaidTransferForm, PayPalTransferForm, CryptoTransferForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from datetime import datetime, date


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


def save_employee(request):
    # User Saving
    user = User(
        email=request.session["user"]["email"],
    )
    user.is_active = False
    user.set_password(raw_password=user.generate_password())
    user.save()

    # Basic Information Saving
    for field, value in request.session["basic_information"].items():
        setattr(user.profile.basic_information, field, value)

    user.profile.basic_information.save()

    # Contact Information Saving
    for field, value in request.session["contact_information"].items():
        setattr(user.profile.contact_information, field, value)

    user.profile.contact_information.save()

    # Contract Saving
    contract_mapping = {
        "contract_type": ContractType,
        "job_type": JobType,
        "job_position": JobPosition,
        "payment_frequency": PaymentFrequency,
        "currency": Currency,
    }
    contract_information_copy = request.session["contract_information"].copy()

    for field, model in contract_mapping.items():
        field_value = model.objects.get(pk=contract_information_copy[field])
        setattr(user.profile.contract, field, field_value)
        contract_information_copy.pop(field)

    for date_field in ["start_date", "end_date"]:
        date_value = datetime.strptime(contract_information_copy[date_field], "%Y-%m-%d")
        setattr(user.profile.contract, date_field, date_value)

        contract_information_copy.pop(date_field)

    for field, value in contract_information_copy.items():
        setattr(user.profile.contract, field, value)

    user.profile.contract.save()

    # Benefits Saving
    benefits_mapping = {
        "sport_benefits": SportBenefit,
        "health_benefits": HealthBenefit,
        "insurance_benefits": InsuranceBenefit,
        "development_benefits": DevelopmentBenefit,
    }

    for key, model in benefits_mapping.items():
        if request.session["benefit_information"].get(key):
            benefit_ids = request.session["benefit_information"].get(key)

            for id in benefit_ids:
                benefit = model.objects.get(pk=id)
                getattr(user.profile.contract.benefits, key).add(benefit)

    # Payment Method Saving
    if "banktransfer" in request.session:
        payment_method = user.banktransfer

        for field, value in request.session["banktransfer"].items():
            setattr(payment_method, field, value)
            payment_method.save()

        user.profile.contract.payment_method = payment_method
        user.profile.contract.save()

    if "prepaidtransfer" in request.session:
        payment_method = user.prepaidtransfer

        for field, value in request.session["prepaidtransfer"].items():
            setattr(payment_method, field, value)
            payment_method.save()

        user.profile.contract.payment_method = payment_method
        user.profile.contract.save()

    if "paypaltransfer" in request.session:
        payment_method = user.paypaltransfer

        for field, value in request.session["paypaltransfer"].items():
            setattr(payment_method, field, value)
            payment_method.save()

        user.profile.contract.payment_method = payment_method
        user.profile.contract.save()

    if "cryptotransfer" in request.session:
        payment_method = user.cryptotransfer
        payment_method.wallet_address = request.session["cryptotransfer"]["wallet_address"]
        payment_method.save()

        user.profile.contract.payment_method = payment_method
        user.profile.contract.save()

    messages.success(
        request=request,
        message="The new employee has been successfully added.",
    )


def clean_session_after_employee_save(request):
    keys_to_keep = ["_auth_user_id", "_auth_user_backend", "_auth_user_hash"]

    session_backup = {key: request.session[key] for key in keys_to_keep if key in request.session}
    request.session.clear()

    request.session.update(session_backup)

    request.session.modified = True


def send_registration_request(request):
    try:
        html_message = render_to_string(
            template_name="core/account-registration-email.html",
            context={
                "email": request.session["user"]["email"],
                "domain": get_current_site(request=request),
            },
        )

        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject="Account Registration Request",
            body=plain_message,
            from_email=os.environ.get("EMAIL_FROM"),
            to=[request.session["user"]["email"]],
        )

        message.attach_alternative(content=html_message, mimetype="text/html")
        message.send()

        messages.success(
            request=request,
            message="The account registration email has been sent successfully.",
        )

    except Exception as e:
        messages.error(
            request=request,
            message="Failed to send the registration email, please try again.",
        )


@login_required(login_url="index")
def dashboard(request):
    register_form = RegisterForm()
    basic_information_form = BasicInformationForm()
    contact_information_form = ContactInformationForm()
    contract_information_form = ContractForm()
    bank_transfer_form = BankTransferForm()
    prepaid_transfer_form = PrepaidTransferForm()
    paypal_transfer_form = PayPalTransferForm()
    crypto_transfer_form = CryptoTransferForm()

    if request.method == "POST":
        if 'register-employee' in request.POST:
            register_form = RegisterForm(data=request.POST)

            if register_form.is_valid():
                request.session["user"] = {
                    "email": register_form.cleaned_data.get("email"),
                }
                request.session.modified = True

                return redirect(to=reverse(
                    viewname="dashboard") + f"?register-employee&tab=basic-information")

        if "basic-information" in request.POST:
            basic_information_form = BasicInformationForm(
                data=request.POST,
            )

            if basic_information_form.is_valid():
                request.session["basic_information"] = {
                    "firstname": basic_information_form.cleaned_data.get("firstname"),
                    "lastname": basic_information_form.cleaned_data.get("lastname"),
                    "date_of_birth": basic_information_form.cleaned_data.get("date_of_birth"),
                }
                request.session.modified = True

                return redirect(to=reverse(viewname="dashboard") + f"?register-employee&tab=contact-information")

        if "contact-information" in request.POST:
            contact_information_form = ContactInformationForm(
                data=request.POST,
            )

            if contact_information_form.is_valid():
                request.session["contact_information"] = {
                    "phone_number": contact_information_form.cleaned_data.get("phone_number"),
                    "country": contact_information_form.cleaned_data.get("country"),
                    "province": contact_information_form.cleaned_data.get("province"),
                    "city": contact_information_form.cleaned_data.get("city"),
                    "postal_code": contact_information_form.cleaned_data.get("postal_code"),
                    "street": contact_information_form.cleaned_data.get("street"),
                    "house_number": contact_information_form.cleaned_data.get("house_number"),
                }

                if contact_information_form.cleaned_data.get("apartment_number"):
                    request.session["contact_information"].update(
                        {
                            "apartment_number": contact_information_form.cleaned_data.get("apartment_number")
                        }
                    )
                    request.session.modified = True

                return redirect(to=reverse(viewname="dashboard") + f"?register-employee&tab=contract-information")

        if "contract-information" in request.POST:
            data = request.POST.copy()

            if request.POST.get("contract_type"):
                contract_type_instance = ContractType.objects.get(slug=request.POST["contract_type"])
                data["contract_type"] = contract_type_instance.pk

            if request.POST.get("job_type"):
                job_type_instance = JobType.objects.get(slug=request.POST["job_type"])
                data["job_type"] = job_type_instance.pk

            if request.POST.get("job_position"):
                job_position_instance = JobPosition.objects.get(slug=request.POST["job_position"])
                data["job_position"] = job_position_instance.pk

            if request.POST.get("payment_frequency"):
                payment_frequency_instance = PaymentFrequency.objects.get(slug=request.POST["payment_frequency"])
                data["payment_frequency"] = payment_frequency_instance.pk

            if request.POST.get("currency"):
                currency_instance = Currency.objects.get(slug=request.POST["currency"])
                data["currency"] = currency_instance.pk

            contract_information_form = ContractForm(
                data=data,
            )

            if contract_information_form.is_valid():
                request.session["contract_information"] = {
                    "contract_type": contract_information_form.cleaned_data.get("contract_type").pk,
                    "job_type": contract_information_form.cleaned_data.get("job_type").pk,
                    "job_position": contract_information_form.cleaned_data.get("job_position").pk,
                    "payment_frequency": contract_information_form.cleaned_data.get("payment_frequency").pk,
                    "currency": contract_information_form.cleaned_data.get("currency").pk,
                    "start_date": contract_information_form.cleaned_data.get("start_date"),
                    "salary": float(contract_information_form.cleaned_data.get("salary")),
                }

                if contract_information_form.cleaned_data.get("work_hours_per_week"):
                    request.session["contract_information"].update(
                        {
                            "work_hours_per_week": contract_information_form.cleaned_data.get("work_hours_per_week"),
                        }
                    )

                if contract_information_form.cleaned_data.get("end_date"):
                    request.session["contract_information"].update(
                        {
                            "end_date": contract_information_form.cleaned_data.get("end_date"),
                        }
                    )
                request.session.modified = True

                return redirect(to=reverse(viewname="dashboard") + f"?register-employee&tab=benefits-information")

        if "benefits-information" in request.POST:
            data = request.POST.copy()

            if "sport_benefits" in request.POST:
                sport_benefits_ids = []

                for sport_benefit in data.getlist("sport_benefits"):
                    sport_benefits_ids.append(SportBenefit.objects.get(slug=sport_benefit).pk)

                data.setlist("sport_benefits", sport_benefits_ids)

            if "health_benefits" in request.POST:
                health_benefits_ids = []

                for health_benefit in data.getlist("health_benefits"):
                    health_benefits_ids.append(HealthBenefit.objects.get(slug=health_benefit).pk)

                data.setlist("health_benefits", health_benefits_ids)

            if "insurance_benefits" in request.POST:
                insurance_benefits_ids = []

                for insurance_benefit in data.getlist("insurance_benefits"):
                    insurance_benefits_ids.append(InsuranceBenefit.objects.get(slug=insurance_benefit).pk)

                data.setlist("insurance_benefits", insurance_benefits_ids)

            if "development_benefits" in request.POST:
                development_benefits_ids = []

                for development_benefit in data.getlist("development_benefits"):
                    development_benefits_ids.append(DevelopmentBenefit.objects.get(slug=development_benefit).pk)

                data.setlist("development_benefits", development_benefits_ids)

            benefits_form = BenefitsForm(data=data)

            if benefits_form.is_valid():
                request.session["benefit_information"] = {}

                if data.get("sport_benefits"):
                    request.session["benefit_information"].update(
                        {
                            "sport_benefits": data.getlist("sport_benefits"),
                        },
                    )

                if data.get("health_benefits"):
                    request.session["benefit_information"].update(
                        {
                            "health_benefits": data.getlist("health_benefits"),
                        },
                    )

                if data.get("insurance_benefits"):
                    request.session["benefit_information"].update(
                        {
                            "insurance_benefits": data.getlist("insurance_benefits"),
                        },
                    )

                if data.get("development_benefits"):
                    request.session["benefit_information"].update(
                        {
                            "development_benefits": data.getlist("development_benefits"),
                        },
                    )
                request.session.modified = True

                return redirect(to=reverse(
                    viewname="dashboard") + f"?register-employee&tab=payment-information&method=bank-transfer")

        if "bank-transfer" in request.POST:
            bank_transfer_form = BankTransferForm(data=request.POST)

            if bank_transfer_form.is_valid():
                request.session["banktransfer"] = {
                    "bank_name": bank_transfer_form.cleaned_data.get("bank_name"),
                    "iban": bank_transfer_form.cleaned_data.get("iban"),
                    "swift": bank_transfer_form.cleaned_data.get("swift"),
                    "account_number": bank_transfer_form.cleaned_data.get("account_number"),
                }
                request.session.modified = True

                save_employee(request=request)

                send_registration_request(request=request)

                clean_session_after_employee_save(request=request)

                return redirect(to=reverse(viewname="dashboard") + "?employees")

        if "prepaid-transfer" in request.POST:
            prepaid_transfer_form = PrepaidTransferForm(data=request.POST)

            if prepaid_transfer_form.is_valid():
                request.session["prepaidtransfer"] = {
                    "owner_name": prepaid_transfer_form.cleaned_data.get("owner_name"),
                    "card_number": prepaid_transfer_form.cleaned_data.get("card_number"),
                    "expiration_date": prepaid_transfer_form.cleaned_data.get("expiration_date"),
                }
                request.session.modified = True

                save_employee(request=request)

                send_registration_request(request=request)

                clean_session_after_employee_save(request=request)

                return redirect(to=reverse(viewname="dashboard") + "?employees")

        if "paypal-transfer" in request.POST:
            paypal_transfer_form = PayPalTransferForm(data=request.POST)

            if paypal_transfer_form.is_valid():
                request.session["paypaltransfer"] = {
                    "paypal_email": paypal_transfer_form.cleaned_data.get("paypal_email"),
                }
                request.session.modified = True

                save_employee(request=request)

                send_registration_request(request=request)

                clean_session_after_employee_save(request=request)

                return redirect(to=reverse(viewname="dashboard") + "?employees")

        if "crypto-transfer" in request.POST:
            data = request.POST.copy()

            if request.POST.get("cryptocurrency"):
                cryptocurrency = CryptoCurrency.objects.get(code=data["cryptocurrency"]).pk
                data["cryptocurrency"] = cryptocurrency

            crypto_transfer_form = CryptoTransferForm(data=data)

            if crypto_transfer_form.is_valid():
                request.session["cryptotransfer"] = {
                    "cryptocurrency": crypto_transfer_form.cleaned_data.get("cryptocurrency").code,
                    "wallet_address": crypto_transfer_form.cleaned_data.get("wallet_address"),
                }
                request.session.modified = True

                send_registration_request(request=request)

                save_employee(request=request)

                clean_session_after_employee_save(request=request)

                return redirect(to=reverse(viewname="dashboard") + "?employees")

    return render(
        request=request,
        template_name="core/dashboard.html",
        context={
            "title": "Dashboard",
            "users": User.objects.exclude(email="admin@gmail.com").order_by("-date_joined"),
            "register_form": register_form,
            "basic_information_form": basic_information_form,
            "contact_information_form": contact_information_form,
            "contract_information_form": contract_information_form,
            "bank_transfer_form": bank_transfer_form,
            "prepaid_transfer_form": prepaid_transfer_form,
            "paypal_transfer_form": paypal_transfer_form,
            "crypto_transfer_form": crypto_transfer_form,
            "contract_types": ContractType.objects.all().order_by("name"),
            "job_types": JobType.objects.all().order_by("name"),
            "job_positions": JobPosition.objects.all().order_by("name"),
            "payment_frequencies": PaymentFrequency.objects.all().order_by("name"),
            "currencies": Currency.objects.all().order_by("name"),
            "sport_benefits": SportBenefit.objects.all().order_by("name"),
            "health_benefits": HealthBenefit.objects.all().order_by("name"),
            "insurance_benefits": InsuranceBenefit.objects.all().order_by("name"),
            "development_benefits": DevelopmentBenefit.objects.all().order_by("name"),
            "cryptocurrencies": CryptoCurrency.objects.all().order_by("name"),
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
