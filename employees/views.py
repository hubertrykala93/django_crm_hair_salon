import os
from django.shortcuts import render, redirect, reverse
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from contracts.models import ContractType, JobPosition, JobType, PaymentFrequency, Currency, SportBenefit, \
    HealthBenefit, InsuranceBenefit, DevelopmentBenefit
from payments.models import CryptoCurrency
from accounts.forms import RegisterForm, BasicInformationForm, ContactInformationForm
from contracts.forms import ContractForm, BenefitsForm
from payments.forms import BankTransferForm, PrepaidTransferForm, PayPalTransferForm, CryptoTransferForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings


def generate_contract(request):
    logo_url = request.build_absolute_uri(settings.MEDIA_URL + 'home/logo.png')

    context = {
        "logo_url": logo_url,
        "firstname": request.session["basic_information"].get("firstname", None),
        "lastname": request.session["basic_information"].get("lastname", None),
        "date_of_birth": request.session["basic_information"].get("date_of_birth", None),
        "phone_number": request.session["contact_information"].get("phone_number", None),
        "country": request.session["contact_information"].get("country", None),
        "province": request.session["contact_information"].get("province", None),
        "city": request.session["contact_information"].get("city", None),
        "postal_code": request.session["contact_information"].get("postal_code", None),
        "street": request.session["contact_information"].get("street", None),
        "house_number": request.session["contact_information"].get("house_number", None),
        "apartment_number": request.session["contact_information"].get("apartment_number", None),
        "contract_type": ContractType.objects.get(
            pk=request.session["contract_information"].get("contract_type", None)),
        "job_type": JobType.objects.get(pk=request.session["contract_information"].get("job_type", None)),
        "job_position": JobPosition.objects.get(
            pk=request.session["contract_information"].get("job_position", None)),
        "payment_frequency": PaymentFrequency.objects.get(
            pk=request.session["contract_information"].get("payment_frequency", None)),
        "currency": Currency.objects.get(pk=request.session["contract_information"].get("currency", None)),
        "start_date": request.session["contract_information"].get("start_date"),
        "end_date": request.session["contract_information"].get("end_date"),
        "salary": request.session["contract_information"].get("salary", None),
        "work_hours_per_week": request.session["contract_information"].get("work_hours_per_week", None),
    }

    if "banktransfer" in request.session:
        context.update(
            {
                "payment_method": "Bank Transfer",
                "bank_name": request.session["banktransfer"].get("bank_name", None),
                "iban": request.session["banktransfer"].get("iban", None),
                "swift": request.session["banktransfer"].get("swift", None),
                "account_number": request.session["banktransfer"].get("account_number", None)
            },
        )

    if "prepaidtransfer" in request.session:
        context.update(
            {
                "payment_method": "Prepaid Transfer",
                "owner_name": request.session["prepaidtransfer"].get("owner_name", None),
                "card_number": request.session["prepaidtransfer"].get("card_number", None),
                "expiration_date": request.session["prepaidtransfer"].get("expiration_date", None),
            },
        )

    if "paypaltransfer" in request.session:
        context.update(
            {
                "payment_method": "PayPal Transfer",
                "paypal_email": request.session["paypaltransfer"].get("paypal_email", None),
            },
        )

    if "cryptotransfer" in request.session:
        context.update(
            {
                "payment_method": "Crypto Transfer",
                "cryptocurrency": request.session["cryptotransfer"].get("cryptocurrency", None),
                "wallet_address": request.session["cryptotransfer"].get("wallet_address", None),
            },
        )

    if "benefit_information" in request.session:
        sport_benefits = []
        health_benefits = []
        insurance_benefits = []
        development_benefits = []

        if request.session["benefit_information"].get("sport_benefits"):
            for sport_benefit in request.session["benefit_information"]["sport_benefits"]:
                sport_benefits.append(SportBenefit.objects.get(pk=sport_benefit))

            context.update(
                {
                    "sport_benefits": sport_benefits,
                },
            )

        if request.session["benefit_information"].get("health_benefits"):
            for health_benefit in request.session["benefit_information"]["health_benefits"]:
                health_benefits.append(HealthBenefit.objects.get(pk=health_benefit))

            context.update(
                {
                    "health_benefits": health_benefits,
                },
            )

        if request.session["benefit_information"].get("insurance_benefits"):
            for insurance_benefit in request.session["benefit_information"]["insurance_benefits"]:
                insurance_benefits.append(InsuranceBenefit.objects.get(pk=insurance_benefit))

            context.update(
                {
                    "insurance_benefits": insurance_benefits,
                },
            )

        if request.session["benefit_information"].get("development_benefits"):
            for development_benefit in request.session["benefit_information"]["development_benefits"]:
                development_benefits.append(DevelopmentBenefit.objects.get(pk=development_benefit))

            context.update(
                {
                    "development_benefits": development_benefits,
                },
            )

    html_string = render_to_string(
        template_name="employees/contract-pdf.html",
        context=context,
    )
    pdf_file = HTML(string=html_string).write_pdf(
        stylesheets=[os.path.join(settings.BASE_DIR, "static/css/style_pdf.css")])

    return pdf_file


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
        if date_field in contract_information_copy:
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


def send_registration_email(request):
    try:
        html_message = render_to_string(
            template_name="employees/account-registration-email.html",
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

        pdf_file = generate_contract(request=request)

        message.attach_alternative(content=html_message, mimetype="text/html")
        message.attach(
            filename=f"{request.session['basic_information']['firstname'].lower().capitalize()}_{request.session['basic_information']['lastname'].lower().capitalize()}_Contract.pdf",
            content=pdf_file, mimetype="application/pdf")
        message.send()

        messages.info(
            request=request,
            message=f"The contract has been successfully sent to '{request.session['basic_information']['firstname']} {request.session['basic_information']['lastname']}'.",
        )

    except Exception as e:
        messages.error(
            request=request,
            message="Failed to send the registration email, please try again.",
        )


def register_employee(request, form):
    if form.is_valid():
        request.session["registration_in_progress"] = True

        request.session["user"] = {
            "email": form.cleaned_data.get("email"),
        }
        request.session.modified = True

        return redirect(to=reverse(
            viewname="employees") + f"?register-employee&tab=basic-information")

    return form


def basic_information(request, form):
    if form.is_valid():
        request.session["basic_information"] = {
            "firstname": form.cleaned_data.get("firstname"),
            "lastname": form.cleaned_data.get("lastname"),
            "date_of_birth": form.cleaned_data.get("date_of_birth"),
        }
        request.session.modified = True

        return redirect(to=reverse(viewname="employees") + f"?register-employee&tab=contact-information")

    return form


def contact_information(request, form):
    if form.is_valid():
        request.session["contact_information"] = {
            "phone_number": form.cleaned_data.get("phone_number"),
            "country": form.cleaned_data.get("country"),
            "province": form.cleaned_data.get("province"),
            "city": form.cleaned_data.get("city"),
            "postal_code": form.cleaned_data.get("postal_code"),
            "street": form.cleaned_data.get("street"),
            "house_number": form.cleaned_data.get("house_number"),
        }

        if form.cleaned_data.get("apartment_number"):
            request.session["contact_information"].update(
                {
                    "apartment_number": form.cleaned_data.get("apartment_number")
                }
            )
            request.session.modified = True

        return redirect(to=reverse(viewname="employees") + f"?register-employee&tab=contract-information")

    return form


def contract_information(request, form):
    if form.is_valid():
        request.session["contract_information"] = {
            "contract_type": form.cleaned_data.get("contract_type").pk,
            "job_type": form.cleaned_data.get("job_type").pk,
            "job_position": form.cleaned_data.get("job_position").pk,
            "payment_frequency": form.cleaned_data.get("payment_frequency").pk,
            "currency": form.cleaned_data.get("currency").pk,
            "start_date": form.cleaned_data.get("start_date"),
            "salary": float(form.cleaned_data.get("salary")),
        }

        if form.cleaned_data.get("work_hours_per_week"):
            request.session["contract_information"].update(
                {
                    "work_hours_per_week": form.cleaned_data.get(
                        "work_hours_per_week"),
                }
            )

        if form.cleaned_data.get("end_date"):
            request.session["contract_information"].update(
                {
                    "end_date": form.cleaned_data.get("end_date"),
                }
            )
        request.session.modified = True

        return redirect(to=reverse(viewname="employees") + f"?register-employee&tab=benefits-information")

    return form


def benefits_information(request, form, data):
    if form.is_valid():
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
            viewname="employees") + f"?register-employee&tab=payment-information&method=bank-transfer")


@login_required(login_url="index")
def employees(request):
    # Register Employee
    register_form = RegisterForm()
    basic_information_form = BasicInformationForm()
    contact_information_form = ContactInformationForm()
    contract_information_form = ContractForm()
    bank_transfer_form = BankTransferForm()
    prepaid_transfer_form = PrepaidTransferForm()
    paypal_transfer_form = PayPalTransferForm()
    crypto_transfer_form = CryptoTransferForm()

    if request.method == "POST":
        if "register-employee" in request.GET:
            if 'register-employee' in request.POST:
                register_form = RegisterForm(data=request.POST)

                result = register_employee(request=request, form=register_form)

                if isinstance(result, RegisterForm):
                    register_form = result

                else:
                    return result

            if "basic-information" in request.POST:
                basic_information_form = BasicInformationForm(
                    data=request.POST,
                )

                result = basic_information(request=request, form=basic_information_form)

                if isinstance(result, BasicInformationForm):
                    basic_information_form = result

                else:
                    return result

            if "contact-information" in request.POST:
                contact_information_form = ContactInformationForm(
                    data=request.POST,
                )

                result = contact_information(request=request, form=contact_information_form)

                if isinstance(result, ContactInformationForm):
                    contact_information_form = result

                else:
                    return result

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

                contract_information_form = ContractForm(data=data)

                result = contract_information(request=request, form=contract_information_form)

                if isinstance(result, ContractForm):
                    contract_information_form = result

                else:
                    return result

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

                result = benefits_information(request=request, form=benefits_form, data=data)

                if isinstance(result, BenefitsForm):
                    benefits_form = result

                else:
                    return result

            if "payment-information" in request.POST:
                if request.POST["payment-information"] == "bank-transfer":
                    bank_transfer_form = BankTransferForm(data=request.POST)

                    if bank_transfer_form.is_valid():
                        request.session["banktransfer"] = {
                            "bank_name": bank_transfer_form.cleaned_data.get("bank_name"),
                            "iban": bank_transfer_form.cleaned_data.get("iban"),
                            "swift": bank_transfer_form.cleaned_data.get("swift"),
                            "account_number": bank_transfer_form.cleaned_data.get("account_number"),
                        }

                if request.POST["payment-information"] == "prepaid-transfer":
                    prepaid_transfer_form = PrepaidTransferForm(data=request.POST)

                    if prepaid_transfer_form.is_valid():
                        request.session["prepaidtransfer"] = {
                            "owner_name": prepaid_transfer_form.cleaned_data.get("owner_name"),
                            "card_number": prepaid_transfer_form.cleaned_data.get("card_number"),
                            "expiration_date": prepaid_transfer_form.cleaned_data.get("expiration_date"),
                        }

                if request.POST["payment-information"] == "paypal-transfer":
                    paypal_transfer_form = PayPalTransferForm(data=request.POST)

                    if paypal_transfer_form.is_valid():
                        request.session["paypaltransfer"] = {
                            "paypal_email": paypal_transfer_form.cleaned_data.get("paypal_email"),
                        }

                if request.POST["payment-information"] == "crypto-transfer":
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

                send_registration_email(request=request)

                save_employee(request=request)

                return redirect(to=reverse(viewname="employees"))

    # Update Employee
    updated_employee = None
    update_email_form = RegisterForm()
    update_basic_information_form = BasicInformationForm()
    update_contact_information_form = ContactInformationForm()

    if "update-employee" in request.GET:
        try:
            updated_employee = User.objects.get(pk=request.GET["update-employee"])

            if "update-employee" in request.POST:
                update_email_form = RegisterForm(data=request.POST, instance=updated_employee)

                if update_email_form.is_valid():
                    if updated_employee.email != update_email_form.cleaned_data.get("email"):
                        updated_employee.email = update_email_form.cleaned_data.get("email")

                        updated_employee.save()

                    return redirect(to=reverse(
                        viewname="employees") + f"?update-employee={request.GET['update-employee']}&tab=basic-information")

            if "update-basic-information" in request.POST:
                update_basic_information_form = BasicInformationForm(data=request.POST)
                instance = updated_employee.profile.basic_information

                if update_basic_information_form.is_valid():
                    cleaned_data = update_basic_information_form.cleaned_data
                    fields_to_update = {}

                    if cleaned_data.get("firstname") != instance.firstname:
                        fields_to_update["firstname"] = cleaned_data.get("firstname")

                    if cleaned_data.get("lastname") != instance.lastname:
                        fields_to_update["lastname"] = cleaned_data.get("lastname")

                    if cleaned_data.get("date_of_birth") != instance.date_of_birth.strftime("%Y-%m-%d"):
                        fields_to_update["date_of_birth"] = cleaned_data.get("date_of_birth")

                    for field, value in fields_to_update.items():
                        setattr(instance, field, value)

                    instance.save()

                    return redirect(to=reverse(
                        viewname="employees") + f"?update-employee={request.GET['update-employee']}&tab=contact-information")

            if "update-contact-information" in request.POST:
                print(request.POST)
                update_contact_information_form = ContactInformationForm(
                    data=request.POST,
                    instance=updated_employee.profile.contact_information
                )
                instance = updated_employee.profile.contact_information

                if update_contact_information_form.is_valid():
                    cleaned_data = update_contact_information_form.cleaned_data
                    fields_to_update = {}

                    if cleaned_data.get("phone_number") != instance.phone_number:
                        fields_to_update["phone_number"] = cleaned_data.get("phone_number")

                    if cleaned_data.get("country") != instance.country:
                        fields_to_update["country"] = cleaned_data.get("country")

                    if cleaned_data.get("province") != instance.province:
                        fields_to_update["province"] = cleaned_data.get("province")

                    if cleaned_data.get("city") != instance.city:
                        fields_to_update["city"] = cleaned_data.get("city")

                    if cleaned_data.get("postal_code") != instance.postal_code:
                        fields_to_update["postal_code"] = cleaned_data.get("postal_code")

                    if cleaned_data.get("house_number") != instance.house_number:
                        fields_to_update["house_number"] = cleaned_data.get("house_number")

                    if cleaned_data.get("apartment_number") != instance.apartment_number:
                        fields_to_update["apartment_number"] = cleaned_data.get("apartment_number")

                    for key, value in fields_to_update.items():
                        setattr(instance, key, value)

                    instance.save()

                    return redirect(to=reverse(
                        viewname="employees") + f"?update-employee={request.GET['update-employee']}&tab=contract-information")

        except User.DoesNotExist:
            messages.error(
                request=request,
                message="Something went wrong. This employee does not exist.",
            )

    return render(
        request=request,
        template_name="employees/employees.html",
        context={
            "title": "Employees" if not request.GET else "Register Employee" if "register-employee" in request.GET else "Update Employee",
            "employees": User.objects.exclude(email="admin@gmail.com").order_by("-date_joined"),
            "register_form": register_form,
            "basic_information_form": basic_information_form,
            "contact_information_form": contact_information_form,
            "contract_information_form": contract_information_form,
            "bank_transfer_form": bank_transfer_form,
            "prepaid_transfer_form": prepaid_transfer_form,
            "paypal_transfer_form": paypal_transfer_form,
            "crypto_transfer_form": crypto_transfer_form,
            "updated_employee": updated_employee,
            "update_email_form": update_email_form,
            "update_basic_information_form": update_basic_information_form,
            "update_contact_information_form": update_contact_information_form,
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


def delete_employee(request, pk):
    try:
        employee = User.objects.get(pk=pk)
        employee.delete()

        messages.success(
            request=request,
            message=f"The employee '{employee.profile.basic_information.firstname} {employee.profile.basic_information.lastname}' has been successfully deleted.",
        )
        return redirect(to="employees")

    except User.DoesNotExist:
        messages.info(
            request=request,
            message="The selected employee does not exist in the database.",
        )
