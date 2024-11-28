import os
from django.shortcuts import render, redirect
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from contracts.models import ContractType, JobPosition, JobType, PaymentFrequency, Currency, SportBenefit, \
    HealthBenefit, InsuranceBenefit, DevelopmentBenefit, EmploymentStatus
from payments.models import CryptoCurrency
from employees.forms import EmployeeRegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from weasyprint import HTML
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction, IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist, FieldError
import logging
from smtplib import SMTPAuthenticationError, SMTPRecipientsRefused, SMTPException

logger = logging.getLogger(__name__)


def generate_contract(request, user):
    logo_url = request.build_absolute_uri(settings.MEDIA_URL + 'home/logo.png')

    basic_information = user.profile.basic_information
    contact_information = user.profile.contact_information
    contract_information = user.profile.contract
    benefits = user.profile.contract.benefits
    banktransfer = user.banktransfer

    context = {
        "logo_url": logo_url,
        "firstname": basic_information.firstname,
        "lastname": basic_information.lastname,
        "date_of_birth": basic_information.date_of_birth,
        "phone_number": contact_information.phone_number,
        "country": contact_information.country,
        "province": contact_information.province,
        "city": contact_information.city,
        "postal_code": contact_information.postal_code,
        "street": contact_information.street,
        "house_number": contact_information.house_number,
        "apartment_number": contact_information.apartment_number or None,
        "contract_type": contract_information.contract_type,
        "job_type": contract_information.job_type,
        "job_position": contract_information.job_position,
        "payment_frequency": contract_information.payment_frequency,
        "currency": contract_information.currency,
        "start_date": contract_information.start_date,
        "end_date": contract_information.end_date or None,
        "salary": contract_information.salary,
        "work_hours_per_week": contract_information.work_hours_per_week or None,
        "payment_method": "Bank Transfer",
        "bank_name": banktransfer.bank_name,
        "iban": banktransfer.iban,
        "swift": banktransfer.swift,
        "account_number": banktransfer.account_number,
        "sport_benefits": benefits.sport_benefits.all(),
        "health_benefits": benefits.health_benefits.all(),
        "insurance_benefits": benefits.insurance_benefits.all(),
        "development_benefits": benefits.development_benefits.all(),
    }

    html_string = render_to_string(
        template_name="employees/contract-pdf.html",
        context=context,
    )
    pdf_file = HTML(string=html_string).write_pdf(
        stylesheets=[os.path.join(settings.BASE_DIR, "static/css/style_pdf.css")])

    return user, pdf_file


def send_registration_email(request, user, pdf_file):
    try:
        html_message = render_to_string(
            template_name="employees/account-registration-email.html",
            context={
                "email": user.email,
                "domain": get_current_site(request=request),
            },
        )

        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject="Account Registration Request",
            body=plain_message,
            from_email=os.environ.get("EMAIL_FROM"),
            to=[user.email],
        )

        message.attach_alternative(content=html_message, mimetype="text/html")
        message.attach(
            filename=f"{user.profile.basic_information.firstname.lower().capitalize()}_{user.profile.basic_information.lastname.lower().capitalize()}_Contract.pdf",
            content=pdf_file, mimetype="application/pdf")
        message.send()

        messages.info(
            request=request,
            message=f"The contract has been successfully sent to '{user.profile.basic_information.firstname} {user.profile.basic_information.lastname}'.",
        )

    except SMTPAuthenticationError as e:
        logger.error(msg=f"SMTP Authentication Error: {e}")
        messages.error(
            request=request,
            message="Authentication failed while sending the email. Please check email settings.",
        )

    except SMTPRecipientsRefused as e:
        logger.error(msg=f"Recipient Address Refused: {e}")
        messages.error(
            request=request,
            message="The recipient's email address is invalid. Please check and try again.",
        )

    except SMTPException as e:
        logger.error(msg=f"SMTP Error: {e}")
        messages.error(
            request=request,
            message="An error occurred while sending the email. Please try again later.",
        )

    except OSError as e:
        logger.error(msg=f"File system error: {e}")
        messages.error(
            request=request,
            message="Failed to send the email due to an issue with the file system."
        )

    except Exception as e:
        logger.error(msg=f"Unexpected error: {e}")
        messages.error(
            request=request,
            message="An unexpected error occurred. Please try again later.",
        )


def pagination(request, object_list, per_page):
    paginator = Paginator(
        object_list=object_list,
        per_page=per_page,
    )

    page = request.GET.get("page", 1)

    objects = paginator.get_page(number=page)

    return objects


def save_profile_data(instance, cleaned_data, fields):
    for field in fields:
        setattr(instance, field, cleaned_data.get(field))

    instance.save()


def save_benefits_data(request, benefit_type, instance):
    mapping = {
        "sport_benefits": SportBenefit,
        "health_benefits": HealthBenefit,
        "insurance_benefits": InsuranceBenefit,
        "development_benefits": DevelopmentBenefit,
    }
    if request.POST.get(benefit_type):
        benefits = mapping[benefit_type].objects.filter(pk__in=map(int, request.POST.getlist(benefit_type)))
        getattr(instance, benefit_type).set(benefits)


def update_fields(instance, cleaned_data, fields):
    updated = False

    for field in fields:
        new_value = cleaned_data.get(field)

        if getattr(instance, field) != new_value:
            setattr(instance, field, new_value)

            updated = True

    if updated:
        instance.save()

    return updated


def update_benefits(request, benefit_type, instance):
    mapping = {
        "sport_benefits": SportBenefit,
        "health_benefits": HealthBenefit,
        "insurance_benefits": InsuranceBenefit,
        "development_benefits": DevelopmentBenefit,
    }
    if request.POST.get("sport_benefits"):
        selected_benefits = set(request.POST.getlist(benefit_type))
        current_benefits = set(str(benefit.pk) for benefit in getattr(instance, benefit_type).all())

        to_add = selected_benefits - current_benefits
        to_remove = current_benefits - selected_benefits

        if to_add:
            benefits_to_add = mapping[benefit_type].objects.filter(pk__in=to_add)
            getattr(instance, benefit_type).add(*benefits_to_add)

        if to_remove:
            benefits_to_remove = mapping[benefit_type].objects.filter(pk__in=to_remove)
            getattr(instance, benefit_type).remove(*benefits_to_remove)

    else:
        getattr(instance, benefit_type).clear()


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
                try:
                    with transaction.atomic():
                        # User Save
                        employee = User(
                            email=register_form.cleaned_data.get("email"),
                        )
                        employee.is_active = False
                        employee.set_password(raw_password=employee.generate_password())
                        employee.save()

                        # Basic Information Save
                        save_profile_data(
                            instance=employee.profile.basic_information,
                            cleaned_data=register_form.cleaned_data,
                            fields=["firstname", "lastname", "date_of_birth"],
                        )

                        # Contact Information Save
                        save_profile_data(
                            instance=employee.profile.contact_information,
                            cleaned_data=register_form.cleaned_data,
                            fields=["phone_number", "country", "province", "city", "postal_code", "street",
                                    "house_number",
                                    "apartment_number"],
                        )

                        # Contract Details Save
                        save_profile_data(
                            instance=employee.profile.contract,
                            cleaned_data=register_form.cleaned_data,
                            fields=["contract_type", "job_type", "job_position", "payment_frequency", "currency",
                                    "start_date",
                                    "end_date", "salary", "work_hours_per_week"],
                        )

                        # Benefit Details Save
                        save_benefits_data(
                            request=request,
                            benefit_type="sport_benefits",
                            instance=employee.profile.contract.benefits,
                        )

                        save_benefits_data(
                            request=request,
                            benefit_type="health_benefits",
                            instance=employee.profile.contract.benefits,
                        )

                        save_benefits_data(
                            request=request,
                            benefit_type="insurance_benefits",
                            instance=employee.profile.contract.benefits,
                        )

                        save_benefits_data(
                            request=request,
                            benefit_type="development_benefits",
                            instance=employee.profile.contract.benefits,
                        )

                        # Payment Details Save
                        save_profile_data(
                            instance=employee.banktransfer,
                            cleaned_data=register_form.cleaned_data,
                            fields=["bank_name", "iban", "swift", "account_number"],
                        )

                    user, pdf_file = generate_contract(
                        request=request,
                        user=employee,
                    )

                    send_registration_email(
                        request=request,
                        user=user,
                        pdf_file=pdf_file,
                    )

                    messages.success(
                        request=request,
                        message="The employee has been successfully registered in the system.",
                    )

                except IntegrityError as e:
                    logger.error(msg=f"IntegrityError during employee registration: {e}")
                    messages.error(
                        request=request,
                        message="An error occurred during employee registration. Please try again later.",
                    )

                except DatabaseError as e:
                    logger.error(msg=f"DatabaseError during employee registration: {e}")
                    messages.error(
                        request=request,
                        message="A system error occurred. Please try again later.",
                    )

                except ObjectDoesNotExist as e:
                    logger.error(msg=f"ObjectDoesNotExist during employee registration: {e}")
                    messages.error(
                        request=request,
                        message="An error occurred during employee registration. Please contact support.",
                    )

                except Exception as e:
                    logger.error(msg=f"Unexpected error during employee registration: {e}")
                    messages.error(
                        request=request,
                        message="An unexpected error occurred. Please contact support.",
                    )

                return redirect(to="employees")

        elif "update-employee" in request.POST:
            register_form = EmployeeRegisterForm(
                data=request.POST,
                instance=employee,
            )

            if register_form.is_valid():
                try:
                    with transaction.atomic():
                        # Update User Email
                        update_fields(
                            instance=employee,
                            cleaned_data=register_form.cleaned_data,
                            fields=["email"],
                        )

                        # Update User Details
                        update_fields(
                            instance=employee.profile.basic_information,
                            cleaned_data=register_form.cleaned_data,
                            fields=["firstname", "lastname", "date_of_birth"],
                        )

                        # Update Contact Details
                        update_fields(
                            instance=employee.profile.contact_information,
                            cleaned_data=register_form.cleaned_data,
                            fields=["phone_number", "country", "province", "city", "postal_code", "street",
                                    "house_number",
                                    "apartment_number"],
                        )

                        # Update Contract Details
                        update_fields(
                            instance=employee.profile.contract,
                            cleaned_data=register_form.cleaned_data,
                            fields=["contract_type", "job_type", "job_position", "payment_frequency",
                                    "work_hours_per_week",
                                    "currency", "start_date", "end_date", "salary"],
                        )

                        # Update Benefits
                        update_benefits(
                            request=request,
                            benefit_type="sport_benefits",
                            instance=employee.profile.contract.benefits,
                        )

                        update_benefits(
                            request=request,
                            benefit_type="health_benefits",
                            instance=employee.profile.contract.benefits,
                        )

                        update_benefits(
                            request=request,
                            benefit_type="insurance_benefits",
                            instance=employee.profile.contract.benefits,
                        )

                        update_benefits(
                            request=request,
                            benefit_type="development_benefits",
                            instance=employee.profile.contract.benefits,
                        )

                        # Update Payment Details
                        update_fields(
                            instance=employee.banktransfer,
                            cleaned_data=register_form.cleaned_data,
                            fields=["bank_name", "iban", "swift", "account_number"],
                        )

                        messages.success(
                            request=request,
                            message="Employee details has been successfully updated.",
                        )

                except IntegrityError as e:
                    logger.error(msg=f"IntegrityError during employee update: {e}")
                    messages.error(
                        request=request,
                        message="An error occurred during employee update. Please try again later.",
                    )

                except DatabaseError as e:
                    logger.error(msg=f"DatabaseError during employee update: {e}")
                    messages.error(
                        request=request,
                        message="A system error occurred. Please try again later.",
                    )

                except ObjectDoesNotExist as e:
                    logger.error(msg=f"ObjectDoesNotExist during employee update: {e}")
                    messages.error(
                        request=request,
                        message="An error occurred during employee update. Please contact support.",
                    )

                except Exception as e:
                    logger.error(msg=f"Unexpected error during employee update: {e}")
                    messages.error(
                        request=request,
                        message="An unexpected error occurred. Please contact support.",
                    )

                return redirect(to="employees")

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

    filters = {
        "contract_type": "profile__contract__contract_type__slug",
        "job_type": "profile__contract__job_type__slug",
        "job_position": "profile__contract__job_position__slug",
        "currency": "profile__contract__currency__slug",
        "payment_frequency": "profile__contract__payment_frequency__slug",
        "employment_status": "profile__contract__status__slug",
    }

    if request.GET:
        for key, value in filters.items():
            selected_values = request.GET.getlist(key)

            if key == "contract_type":
                selected_contract_types.extend(selected_values)
            elif key == "job_type":
                selected_job_types.extend(selected_values)
            elif key == "job_position":
                selected_job_positions.extend(selected_values)
            elif key == "currency":
                selected_currencies.extend(selected_values)
            elif key == "payment_frequency":
                selected_payment_frequencies.extend(selected_values)
            elif key == "employment_status":
                selected_employment_statuses.extend(selected_values)

            if selected_values:
                try:
                    employees = employees.filter(**{
                        f"{value}__in": selected_values,
                    })

                except FieldError as e:
                    logger.warning(msg=f"Invalid filter field '{value}' in filter '{key}'. {str(e)}")
                    employees = employees.none()

                except ValueError as e:
                    logger.warning(msg=f"Invalid value for filter '{key}' with values {value}. {str(e)}")
                    employees = employees.none()

                except Exception as e:
                    logger.warning(msg=f"Unexpected error during filtering with filter '{key}': {str(e)}")
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
