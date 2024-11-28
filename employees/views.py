import os
from django.shortcuts import render, redirect
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from contracts.models import ContractType, JobPosition, JobType, PaymentFrequency, Currency, SportBenefit, \
    HealthBenefit, InsuranceBenefit, DevelopmentBenefit, EmploymentStatus
from payments.models import CryptoCurrency
from contracts.forms import BenefitsForm
from employees.forms import EmployeeRegisterForm
from payments.forms import BankTransferForm, PrepaidTransferForm, PayPalTransferForm, CryptoTransferForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q


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


def pagination(request, object_list, per_page):
    paginator = Paginator(
        object_list=object_list,
        per_page=per_page,
    )

    page = request.GET.get("page", 1)

    objects = paginator.get_page(number=page)

    return objects


@login_required(login_url="index")
def employees(request):
    register_form = EmployeeRegisterForm()
    employee = None

    if request.GET.get("update-employee"):
        try:
            employee = User.objects.get(pk=request.GET.get("update-employee"))

        except User.DoesNotExist:
            messages.error(
                request=request,
                message="Employee not found.",
            )
            return redirect(to="employees")

    if request.method == "POST":
        if "register-employee" in request.POST:
            register_form = EmployeeRegisterForm(
                data=request.POST,
            )

            if register_form.is_valid():
                # User Save
                employee = User(
                    email=register_form.cleaned_data.get("email"),
                )
                employee.is_active = False
                employee.set_password(raw_password=employee.generate_password())
                employee.save()

                # Basic Information Save
                employee.profile.basic_information.firstname = register_form.cleaned_data.get("firstname")
                employee.profile.basic_information.lastname = register_form.cleaned_data.get("lastname")
                employee.profile.basic_information.date_of_birth = register_form.cleaned_data.get("date_of_birth")
                employee.profile.basic_information.save()

                # Contact Information Save
                employee.profile.contact_information.phone_number = register_form.cleaned_data.get("phone_number")
                employee.profile.contact_information.country = register_form.cleaned_data.get("country")
                employee.profile.contact_information.province = register_form.cleaned_data.get("province")
                employee.profile.contact_information.city = register_form.cleaned_data.get("city")
                employee.profile.contact_information.postal_code = register_form.cleaned_data.get("postal_code")
                employee.profile.contact_information.street = register_form.cleaned_data.get("street")
                employee.profile.contact_information.house_number = register_form.cleaned_data.get("house_number")

                if register_form.cleaned_data.get("apartment_number"):
                    employee.profile.contact_information.apartment_number = register_form.cleaned_data.get(
                        "apartment_number")

                employee.profile.contact_information.save()

                # Contract Details Save
                employee.profile.contract.contract_type = register_form.cleaned_data.get("contract_type")
                employee.profile.contract.job_type = register_form.cleaned_data.get("job_type")
                employee.profile.contract.job_position = register_form.cleaned_data.get("job_position")
                employee.profile.contract.payment_frequency = register_form.cleaned_data.get("payment_frequency")
                employee.profile.contract.currency = register_form.cleaned_data.get("currency")
                employee.profile.contract.start_date = register_form.cleaned_data.get("start_date")
                employee.profile.contract.end_date = register_form.cleaned_data.get("end_date")
                employee.profile.contract.salary = register_form.cleaned_data.get("salary")

                if register_form.cleaned_data.get("work_hours_per_week"):
                    employee.profile.contract.work_hours_per_week = register_form.cleaned_data.get(
                        "work_hours_per_week")

                if register_form.cleaned_data.get("end_date"):
                    employee.profile.contract.end_date = register_form.cleaned_data.get("end_date")

                employee.profile.contract.save()

                # Benefit Details Save
                if "sport_benefits" in request.POST:
                    for sport_benefit in request.POST.getlist("sport_benefits"):
                        employee.profile.contract.benefits.sport_benefits.add(
                            SportBenefit.objects.get(
                                pk=int(sport_benefit),
                            )
                        )

                if "health_benefits" in request.POST:
                    for health_benefit in request.POST.getlist("health_benefits"):
                        employee.profile.contract.benefits.health_benefits.add(
                            HealthBenefit.objects.get(
                                pk=int(health_benefit),
                            )
                        )

                if "insurance_benefits" in request.POST:
                    for insurance_benefit in request.POST.getlist("insurance_benefits"):
                        employee.profile.contract.benefits.insurance_benefits.add(
                            InsuranceBenefit.objects.get(
                                pk=int(insurance_benefit),
                            )
                        )

                if "development_benefits" in request.POST:
                    for development_benefit in request.POST.getlist("development_benefits"):
                        employee.profile.contract.benefits.development_benefits.add(
                            DevelopmentBenefit.objects.get(
                                pk=int(development_benefit),
                            )
                        )

                # Payment Details Save
                employee.banktransfer.bank_name = register_form.cleaned_data.get("bank_name")
                employee.banktransfer.iban = register_form.cleaned_data.get("iban")
                employee.banktransfer.swift = register_form.cleaned_data.get("swift")
                employee.banktransfer.account_number = register_form.cleaned_data.get("account_number")
                employee.banktransfer.save()

                employee.profile.contract.payment_method = employee.banktransfer
                employee.profile.contract.save()

                messages.success(
                    request=request,
                    message="The employee has been successfully registered in the system.",
                )

                return redirect(to="employees")

        elif "update-employee" in request.POST:
            register_form = EmployeeRegisterForm(
                data=request.POST,
                instance=employee,
            )

            if register_form.is_valid():
                # Update User Email
                updated = False

                if employee.email != register_form.cleaned_data.get("email"):
                    employee.email = register_form.cleaned_data.get("email")
                    updated = True

                if updated:
                    print("User Email Updated")
                    employee.save()

                # Update User Details
                updated = False

                if employee.profile.basic_information.firstname != register_form.cleaned_data.get("firstname"):
                    employee.profile.basic_information.firstname = register_form.cleaned_data.get("firstname")
                    updated = True

                if employee.profile.basic_information.lastname != register_form.cleaned_data.get("lastname"):
                    employee.profile.basic_information.lastname = register_form.cleaned_data.get("lastname")
                    updated = True

                if employee.profile.basic_information.date_of_birth != register_form.cleaned_data.get("date_of_birth"):
                    employee.profile.basic_information.date_of_birth = register_form.cleaned_data.get("date_of_birth")
                    updated = True

                if updated:
                    print("User Details Updated")
                    employee.profile.basic_information.save()

                # Update Contact Details
                updated = False

                if employee.profile.contact_information.phone_number != register_form.cleaned_data.get("phone_number"):
                    employee.profile.contact_information.phone_number = register_form.cleaned_data.get("phone_number")
                    updated = True

                if employee.profile.contact_information.country != register_form.cleaned_data.get("country"):
                    employee.profile.contact_information.country = register_form.cleaned_data.get("country")
                    updated = True

                if employee.profile.contact_information.province != register_form.cleaned_data.get("province"):
                    employee.profile.contact_information.province = register_form.cleaned_data.get("province")
                    updated = True

                if employee.profile.contact_information.city != register_form.cleaned_data.get("city"):
                    employee.profile.contact_information.city = register_form.cleaned_data.get("city")
                    updated = True

                if employee.profile.contact_information.postal_code != register_form.cleaned_data.get("postal_code"):
                    employee.profile.contact_information.postal_code = register_form.cleaned_data.get("postal_code")
                    updated = True

                if employee.profile.contact_information.street != register_form.cleaned_data.get("street"):
                    employee.profile.contact_information.street = register_form.cleaned_data.get("street")
                    updated = True

                if employee.profile.contact_information.house_number != register_form.cleaned_data.get("house_number"):
                    employee.profile.contact_information.house_number = register_form.cleaned_data.get("house_number")
                    updated = True

                if employee.profile.contact_information.apartment_number != register_form.cleaned_data.get(
                        "apartment_number"):
                    employee.profile.contact_information.apartment_number = register_form.cleaned_data.get(
                        "apartment_number")
                    updated = True

                if updated:
                    print("Contact Details Updated")
                    employee.profile.contact_information.save()

                # Update Contract Details
                updated = False

                if employee.profile.contract.contract_type != register_form.cleaned_data.get("contract_type"):
                    employee.profile.contract.contract_type = register_form.cleaned_data.get("contract_type")
                    updated = True

                if employee.profile.contract.job_type != register_form.cleaned_data.get("job_type"):
                    employee.profile.contract.job_type = register_form.cleaned_data.get("job_type")
                    updated = True

                if employee.profile.contract.job_position != register_form.cleaned_data.get("job_position"):
                    employee.profile.contract.job_position = register_form.cleaned_data.get("job_position")
                    updated = True

                if employee.profile.contract.payment_frequency != register_form.cleaned_data.get("payment_frequency"):
                    employee.profile.contract.payment_frequency = register_form.cleaned_data.get("payment_frequency")
                    updated = True

                if employee.profile.contract.work_hours_per_week != register_form.cleaned_data.get(
                        "work_hours_per_week"):
                    employee.profile.contract.work_hours_per_week = register_form.cleaned_data.get(
                        "work_hours_per_week")
                    updated = True

                if employee.profile.contract.currency != register_form.cleaned_data.get("currency"):
                    employee.profile.contract.currency = register_form.cleaned_data.get("currency")
                    updated = True

                if employee.profile.contract.start_date != register_form.cleaned_data.get("start_date"):
                    employee.profile.contract.start_date = register_form.cleaned_data.get("start_date")
                    updated = True

                if employee.profile.contract.end_date != register_form.cleaned_data.get("end_date"):
                    employee.profile.contract.end_date = register_form.cleaned_data.get("end_date")
                    updated = True

                if employee.profile.contract.salary != register_form.cleaned_data.get("salary"):
                    employee.profile.contract.salary = register_form.cleaned_data.get("salary")
                    updated = True

                if updated:
                    print("Contract Details Updated")
                    employee.profile.contract.save()

                # Update Payment Details
                updated = False

                if employee.banktransfer.bank_name != register_form.cleaned_data.get("bank_name"):
                    employee.banktransfer.bank_name = register_form.cleaned_data.get("bank_name")
                    updated = True

                if employee.banktransfer.iban != register_form.cleaned_data.get("iban"):
                    employee.banktransfer.iban = register_form.cleaned_data.get("iban")
                    updated = True

                if employee.banktransfer.swift != register_form.cleaned_data.get("swift"):
                    employee.banktransfer.swift = register_form.cleaned_data.get("swift")
                    updated = True

                if employee.banktransfer.account_number != register_form.cleaned_data.get("account_number"):
                    employee.banktransfer.account_number = register_form.cleaned_data.get("account_number")
                    updated = True

                if updated:
                    print("Payment Details Updated")
                    employee.banktransfer.save()

                messages.success(
                    request=request,
                    message="Employee details has been successfully updated.",
                )

                return redirect(to="employees")


            else:
                print("Form is not Valid.")

    # Sorting
    employees = User.objects.exclude(
        email="admin@gmail.com"
    ).order_by(
        "-date_joined",
    )

    order_options = {
        "salary": "-profile__contract__salary",
        "working-hours": "-profile__contract__work_hours_per_week",
    }

    order = request.GET.get("order", None)

    if order is not None:
        if order in order_options:
            employees = employees.order_by(order_options[order])

    # Filters
    selected_contract_types = []
    selected_job_types = []
    selected_job_positions = []
    selected_currencies = []
    selected_payment_frequencies = []
    selected_employment_statuses = []

    if "contract_type" in request.GET:
        selected_contract_types = request.GET.getlist("contract_type")

        try:
            employees = employees.filter(
                profile__contract__contract_type__slug__in=selected_contract_types,
            )

        except ContractType.DoesNotExist:
            employees = employees.none()

    if "job_type" in request.GET:
        selected_job_types = request.GET.getlist("job_type")

        try:
            employees = employees.filter(
                profile__contract__job_type__slug__in=selected_job_types,
            )

        except JobType.DoesNotExist:
            employees = employees.none()

    if "job_position" in request.GET:
        selected_job_positions = request.GET.getlist("job_position")

        try:
            employees = employees.filter(
                profile__contract__job_position__slug__in=selected_job_positions,
            )

        except JobPosition.DoesNotExist:
            employees = employees.none()

    if "currency" in request.GET:
        selected_currencies = request.GET.getlist("currency")

        try:
            employees = employees.filter(
                profile__contract__currency__slug__in=selected_currencies,
            )

        except Currency.DoesNotExist:
            employees = employees.none()

    if "payment_frequency" in request.GET:
        selected_payment_frequencies = request.GET.getlist("payment_frequency")

        try:
            employees = employees.filter(profile__contract__payment_frequency__slug__in=selected_payment_frequencies)

        except PaymentFrequency.DoesNotExist:
            employees = employees.none()

    if "employment_status" in request.GET:
        selected_employment_statuses = request.GET.getlist("employment_status")

        try:
            employees = employees.filter(
                profile__contract__status__slug__in=selected_employment_statuses,
            )

        except EmploymentStatus.DoesNotExist:
            employees = employees.none()

    if "search" in request.GET:
        search_query = request.GET.get("search", "").strip()

        if search_query:
            employees = employees.filter(
                Q(profile__basic_information__firstname__icontains=search_query) | Q(
                    email__icontains=search_query,
                ),
            )

    return render(
        request=request,
        template_name="employees/employees.html",
        context={
            "title": "Employees" if not request.GET or "order" in request.GET or "search" in request.GET else "Register Employee" if "register-employee" in request.GET else "Update Employee",
            "register_form": register_form,
            "employee": employee,
            "selected_sport_benefits": request.POST.getlist(
                "sport_benefits") if "sport_benefits" in request.POST else None,
            "selected_health_benefits": request.POST.getlist(
                "health_benefits") if "health_benefits" in request.POST else None,
            "selected_insurance_benefits": request.POST.getlist(
                "insurance_benefits") if "insurance_benefits" in request.POST else None,
            "selected_development_benefits": request.POST.getlist(
                "development_benefits") if "development_benefits" in request.POST else None,
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
            "employment_statuses": EmploymentStatus.objects.all(),
            "selected_contract_types": selected_contract_types,
            "selected_job_types": selected_job_types,
            "selected_job_positions": selected_job_positions,
            "selected_currencies": selected_currencies,
            "selected_payment_frequencies": selected_payment_frequencies,
            "selected_employment_statuses": selected_employment_statuses,
            "objects": pagination(
                request=request,
                object_list=employees,
                per_page=6
            )
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
