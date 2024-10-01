from django.shortcuts import render, redirect, reverse
from .forms import RegisterForm, PasswordResetForm, OneTimePasswordForm, ChangePasswordForm, \
    UpdateContactInformationForm, UpdatePasswordForm, UpdateBasicInformationForm
from payments.forms import UpdateBankTransferForm, UpdateCryptoTransferForm, UpdatePrepaidTransferForm, \
    UpdatePayPalTransferForm
from django.contrib import messages
from .models import User, OneTimePassword
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import token_generator
from datetime import date, datetime
from payments.models import BankTransfer, PrepaidTransfer, PaymentMethod, CryptoTransfer, CryptoCurrency


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
def register(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            user = User(
                email=request.POST["email"]

            )
            password = make_password(
                password=request.POST["password"]
            )
            user.password = password
            user.save()

            try:
                html_message = render_to_string(
                    template_name="accounts/account-activation-email.html",
                    context={
                        "user": user,
                        "domain": get_current_site(request=request),
                        "uid": urlsafe_base64_encode(s=force_bytes(s=user.pk)),
                        "token": token_generator.make_token(user=user)
                    },
                    request=request,
                )
                plain_message = strip_tags(html_message)

                message = EmailMultiAlternatives(
                    subject="Account Activation Request",
                    body=plain_message,
                    to=[user.email],
                )
                message.attach_alternative(content=html_message, mimetype="text/html")
                message.send()

                user.save()

                messages.success(
                    request=request,
                    message="Your account has been successfully created. Please check your email to activate it.",
                )

                return redirect(to="register")

            except Exception as e:
                messages.error(
                    request=request,
                    message="Registration failed. Please try again.",
                )

                return redirect(to="register")

        else:
            if len(request.POST["password"]) != 0 and len(request.POST["repassword"]) == 0:
                messages.error(
                    request=request,
                    message="To register an account, you also need to provide the Confirm Password.",
                )

    else:
        form = RegisterForm()

    return render(
        request=request,
        template_name="accounts/register.html",
        context={
            "title": "Register",
            "form": form,
        },
    )


def activate(request, uidb64, token):
    try:
        uid = force_str(s=urlsafe_base64_decode(s=uidb64))
        user = User.objects.get(pk=int(uid))

    except User.DoesNotExist:
        messages.info(
            request=request,
            message="Your account does not exist, please register.",
        )

        return redirect(to="register")

    if user:
        if not user.is_verified:

            if token_generator.check_token(user=user, token=token):
                user.is_verified = True
                user.save()

                messages.success(
                    request=request,
                    message="Your account has been activated, you can now log in."
                )

            else:
                user.delete()

                messages.info(
                    request=request,
                    message="Your activation link has expired. Please create your account again.",
                )

                return redirect(to="register")

        else:
            messages.info(
                request=request,
                message="Your account has already been activated, you can log in.",
            )

    return redirect(to="home")


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
def password_reset_method(request):
    if request.method == "POST":
        if "method" in request.POST:
            if request.POST["method"] == "email":
                return redirect(to=reverse(viewname="forgot-password") + f"?method={request.POST['method']}")

            elif request.POST["method"] == "sms":
                return redirect(to=reverse(viewname="forgot-password") + f"?method={request.POST['method']}")

            elif request.POST["method"] == "voice":
                return redirect(to=reverse(viewname="forgot-password") + f"?method={request.POST['method']}")

    return render(
        request=request,
        template_name="accounts/password-reset-method.html",
        context={
            "title": "Choose Method",
        }
    )


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
def forgot_password(request):
    if request.method == "POST":
        form = PasswordResetForm(data=request.POST)

        if form.is_valid():
            user = User.objects.get(email=request.POST["email"])

            if not OneTimePassword.objects.filter(user=user).exists():
                otp = OneTimePassword(user=user)
                otp.save()

            otp = OneTimePassword.objects.get(user=user)

            if request.GET["method"] == "email":
                try:
                    html_message = render_to_string(
                        template_name="accounts/password-reset-email.html",
                        context={
                            "user": user,
                            "otp": otp.password,
                        },
                        request=request,
                    )
                    plain_message = strip_tags(html_message)

                    message = EmailMultiAlternatives(
                        subject="Password Reset Request",
                        body=plain_message,
                        to=[user.email],
                    )
                    message.attach_alternative(content=html_message, mimetype="text/html")
                    message.send()

                    messages.success(
                        request=request,
                        message=f"We have sent the password to the provided email address '{request.POST['email']}'. Please check your inbox.",
                    )

                    return redirect(f"{reverse('confirm-password')}?method={request.GET['method']}&email={user.email}")


                except Exception as e:
                    messages.error(
                        request=request,
                        message="Failed to send the email, please try again.",
                    )

                    return redirect(to=reverse(viewname="forgot-password") + f"?method={request.GET['method']}")

            else:
                if request.GET["method"] == "sms":
                    pass

                else:
                    pass

                return redirect(to=reverse(
                    viewname="confirm-password") + f"?method={request.GET['method']}&mobile={request.POST['mobile']}")

    else:
        form = PasswordResetForm()

    return render(
        request=request,
        template_name="accounts/forgot-password.html",
        context={
            "title": "Forgot Password",
            "form": form,
        }
    )


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
def confirm_one_time_password(request):
    if request.method == "POST":
        form = OneTimePasswordForm(data=request.POST)

        if form.is_valid():
            user = User.objects.get(email=request.GET["email"])

            return redirect(f"{reverse('change-password')}?email={user.email}")

    else:
        form = OneTimePasswordForm()

    return render(
        request=request,
        template_name="accounts/confirm-password.html",
        context={
            "title": "Confirm Password",
            "form": form,
        }
    )


@user_passes_test(test_func=lambda user: not user.is_authenticated, login_url="dashboard")
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(
            data=request.POST,
        )

        if form.is_valid():
            try:
                user = User.objects.get(email=request.GET["email"])
                otp = OneTimePassword.objects.get(user=user)

                user.set_password(raw_password=request.POST["password"])
                user.save()

                otp.delete()

                messages.success(
                    request=request,
                    message=f"The password for the account '{user.email}' has been successfully changed. "
                            f"You can now log in.",
                )

                return redirect(to="home")

            except User.DoesNotExist:
                messages.info(
                    request=request,
                    message=f"A user with the email address '{request.GET['email']}' does not exist."
                )

                return redirect(to="register")

            except OneTimePassword.DoesNotExist:
                messages.info(
                    request=request,
                    message=f"The One Time Password for the user '{request.GET['email']}' does not exist.",
                )

                return redirect(to="forgot-password")

    else:
        form = ChangePasswordForm()

    return render(
        request=request,
        template_name="accounts/change-password.html",
        context={
            "title": "Change Password",
            "form": form,
        }
    )


# Update Password
def handle_update_password(request):
    password = request.POST["password"]

    if password:
        user = request.user

        if user.check_password(raw_password=password):
            messages.info(
                request=request,
                message="You cannot change to the previous password; please create a new one.",
            )
        else:
            user.set_password(raw_password=password)
            user.save()

            update_session_auth_hash(
                request=request,
                user=user
            )

            messages.success(
                request=request,
                message="The password has been successfully changed.",
            )

    else:
        messages.info(
            request=request,
            message="No changes have been made.",
        )


def update_fields(instance, changes):
    updated_fields = []

    if not "cryptocurrency" in changes:
        for field, value in changes.items():
            current_value = getattr(instance, field)

            if current_value != value:
                setattr(instance, field, value)
                updated_fields.append(field)

    else:
        try:
            cryptocurrency = CryptoCurrency.objects.get(code=changes["cryptocurrency"])

        except CryptoCurrency.DoesNotExist:
            pass

        if instance.cryptocurrency.code != changes["cryptocurrency"]:
            updated_fields.append("cryptocurrency")

        if instance.wallet_address != changes["wallet_address"]:
            updated_fields.append("wallet_address")

        instance.cryptocurrency = CryptoCurrency.objects.get(code=changes["cryptocurrency"])
        instance.wallet_address = changes["wallet_address"]

    instance.save()

    return updated_fields


# Update Basic Information
def handle_profile_data(request):
    data = request.POST.copy()

    for key in ["csrfmiddlewaretoken", "basic-information", "contact-information"]:
        if key in data:
            data.pop(key)

    changes = {
        key: datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date() if key == "date_of_birth" else value
        for key, value in data.items()
    }

    updated_fields = update_fields(
        instance=request.user.profile.basic_information if "basic-information" in request.POST else request.user.profile.contact_information if "contact-information" in request.POST else None,
        changes=changes
    )

    if updated_fields:
        messages.success(
            request=request,
            message=f"{'Basic' if 'basic-information' in request.POST else 'Contact'} "
                    f"Information has been successfully updated."
        )

    else:
        messages.info(
            request=request,
            message="No changes have been made.",
        )


def payment_messages(request, instance, updated_fields, save_method, contract):
    method_name = instance.name.split(sep=" ")[0].lower() + " " + instance.name.split(sep=" ")[1].lower()

    if updated_fields and save_method:
        print("Updated Fields and Save Method")
        if contract.payment_method:
            print("Contract has Payment Method")

            if instance.name != contract.payment_method.name:
                contract.payment_method = instance
                contract.save()

                messages.success(
                    request=request,
                    message=f"The payment method has been successfully switched to {method_name} and updated.",
                )

            # messages.success(
            #     request=request,
            #     message=f"The payment method via {method_name} has been successfully updated.",
            # )

        else:
            print("Contract has not Payment Method")
            contract.payment_method = instance
            contract.save()

            messages.success(
                request=request,
                message=f"The payment method via {method_name} has been successfully updated and set.",
            )

    elif updated_fields and not save_method:
        print("Updated Fields and not Save Method")
        if contract.payment_method:
            print("Contract has Payment Method")
            if instance.name == contract.payment_method.name:
                contract.payment_method = None
                contract.save()

                messages.info(
                    request=request,
                    message=f"The payment method via {method_name} has been removed. To receive a transfer, please set one of the payment methods.",
                )

        messages.success(
            request=request,
            message=f"The payment method via {method_name} has been successfully updated.",
        )

    elif not updated_fields and save_method:
        print("Not Updated Fields and Save Method")
        if contract.payment_method:
            print("Contract has Payment Method")

            if instance.name != contract.payment_method.name:
                contract.payment_method = instance
                contract.save()

                messages.success(
                    request=request,
                    message=f"The payment method has been successfully switched to {method_name}.",
                )

            else:
                messages.info(
                    request=request,
                    message="No changes have been made.",
                )

        else:
            print("Contract has not Payment Method")
            contract.payment_method = instance
            contract.save()

            messages.success(
                request=request,
                message=f"The payment method via {method_name} has been successfully set.",
            )

    elif not updated_fields and not save_method:
        print("Not Updated Fields and not Save Method")
        if contract.payment_method:
            print(instance.name == contract.payment_method.name)
            print("Contract has Payment Method")
            if instance.name != contract.payment_method.name:
                print("Instance Name != Contract Payment Method Name")
                messages.info(
                    request=request,
                    message="No changes have been made.",
                )

            else:
                contract.payment_method = None
                contract.save()

                messages.info(
                    request=request,
                    message=f"The payment method via {method_name} has been removed. To receive a transfer, please set one of the payment methods.",
                )

        else:
            print("Contract has not Payment Method")
            messages.info(
                request=request,
                message="No changes have been made.",
            )


def handle_bank_transfer(request):
    data = request.POST.copy()

    for key in ["csrfmiddlewaretoken", "payment-information", "payment-method"]:
        if key in data:
            data.pop(key)

    save_method = data.pop("save_method", None)

    changes = {k: v for k, v in data.items()}

    updated_fields = update_fields(
        instance=request.user.banktransfer,
        changes=changes
    )

    payment_messages(
        request=request,
        instance=request.user.banktransfer,
        updated_fields=updated_fields,
        save_method=save_method,
        contract=request.user.profile.contract
    )


def handle_prepaid_transfer(request):
    data = request.POST.copy()

    for key in ["csrfmiddlewaretoken", "payment-information", "payment-method"]:
        if key in data:
            data.pop(key)

    save_method = data.pop("save_method", None)

    changes = {
        key: datetime.strptime(data["expiration_date"], "%Y-%m-%d").date() if key == "expiration_date" else value
        for key, value in data.items()
    }

    updated_fields = update_fields(
        instance=request.user.prepaidtransfer,
        changes=changes
    )

    payment_messages(
        request=request,
        instance=request.user.prepaidtransfer,
        updated_fields=updated_fields,
        save_method=save_method,
        contract=request.user.profile.contract
    )


def handle_paypal_transfer(request):
    data = request.POST.copy()

    for key in ["csrfmiddlewaretoken", "payment-method", "payment-information"]:
        if key in data:
            data.pop(key)

    save_method = data.pop("save_method", None)

    changes = {
        k: v for k, v in data.items()
    }

    updated_fields = update_fields(
        instance=request.user.paypaltransfer,
        changes=changes
    )

    payment_messages(
        request=request,
        instance=request.user.paypaltransfer,
        updated_fields=updated_fields,
        save_method=save_method,
        contract=request.user.profile.contract
    )


def handle_crypto_transfer(request):
    data = request.POST.copy()

    for key in ["csrfmiddlewaretoken", "payment-method", "payment-information"]:
        if key in data:
            data.pop(key)

    save_method = request.POST.get("save_method", None)

    changes = {
        k: v for k, v in data.items()
    }

    updated_fields = update_fields(
        instance=request.user.cryptotransfer,
        changes=changes,
    )

    payment_messages(
        request=request,
        instance=request.user.cryptotransfer,
        updated_fields=updated_fields,
        save_method=save_method,
        contract=request.user.profile.contract
    )


@login_required(login_url="home")
def settings(request):
    update_password_form = UpdatePasswordForm()
    update_basic_information_form = UpdateBasicInformationForm(
        initial={
            "date_of_birth": request.user.profile.basic_information.date_of_birth.strftime(
                "%Y-%m-%d") if request.user.profile.basic_information.date_of_birth else "",
        }
    )
    update_contact_information_form = UpdateContactInformationForm()
    update_bank_transfer_form = UpdateBankTransferForm()
    update_prepaid_transfer_form = UpdatePrepaidTransferForm(
        initial={
            "expiration_date": request.user.prepaidtransfer.expiration_date.strftime("%Y-%m-%d")
            if request.user.prepaidtransfer.expiration_date else "",
        }
    )
    update_paypal_transfer_form = UpdatePayPalTransferForm()
    update_crypto_transfer_form = UpdateCryptoTransferForm()

    if request.method == "POST":
        if "change-password" in request.POST:
            update_password_form = UpdatePasswordForm(
                data=request.POST,
                instance=request.user,
            )

            if update_password_form.is_valid():
                handle_update_password(request=request)

        if "basic-information" in request.POST:
            update_basic_information_form = UpdateBasicInformationForm(data=request.POST)

            if update_basic_information_form.is_valid():
                handle_profile_data(request=request)

        if "contact-information" in request.POST:
            update_contact_information_form = UpdateContactInformationForm(
                data=request.POST,
                instance=request.user.profile.contact_information,
            )

            if update_contact_information_form.is_valid():
                handle_profile_data(request=request)

        if "payment-information" in request.POST:
            if "payment-method" in request.POST:
                if request.POST["payment-method"] == "bank-transfer":
                    update_bank_transfer_form = UpdateBankTransferForm(
                        data=request.POST,
                        instance=request.user.banktransfer,
                    )

                    if update_bank_transfer_form.is_valid():
                        handle_bank_transfer(request=request)

                elif request.POST["payment-method"] == "prepaid-transfer":
                    update_prepaid_transfer_form = UpdatePrepaidTransferForm(
                        data=request.POST,
                        instance=request.user.prepaidtransfer,
                    )

                    if update_prepaid_transfer_form.is_valid():
                        handle_prepaid_transfer(request=request)

                elif request.POST["payment-method"] == "paypal-transfer":
                    update_paypal_transfer_form = UpdatePayPalTransferForm(
                        data=request.POST,
                        user=request.user,
                        instance=request.user.paypaltransfer,
                    )

                    if update_paypal_transfer_form.is_valid():
                        handle_paypal_transfer(request=request)

                else:
                    update_crypto_transfer_form = UpdateCryptoTransferForm(
                        data=request.POST,
                        instance=request.user.cryptotransfer,
                    )

                    if update_crypto_transfer_form.is_valid():
                        handle_crypto_transfer(request=request)

    return render(
        request=request,
        template_name="accounts/settings.html",
        context={
            "title": "Profile",
            "user": request.user,
            "basic_information": request.user.profile.basic_information,
            "contact_information": request.user.profile.contact_information,
            "contract": request.user.profile.contract,
            "benefits": request.user.profile.contract.benefits,
            "banktransfer": request.user.banktransfer,
            "prepaidtransfer": request.user.prepaidtransfer,
            "paypaltransfer": request.user.paypaltransfer,
            "cryptotransfer": request.user.cryptotransfer,
            "update_password_form": update_password_form,
            "update_basic_information_form": update_basic_information_form,
            "update_contact_information_form": update_contact_information_form,
            "update_bank_transfer_form": update_bank_transfer_form,
            "update_prepaid_transfer_form": update_prepaid_transfer_form,
            "update_paypal_transfer_form": update_paypal_transfer_form,
            "update_crypto_transfer_form": update_crypto_transfer_form,
            "cryptocurrencies": CryptoCurrency.objects.all(),
        }
    )


@login_required(login_url="home")
def log_out(request):
    logout(request=request)

    return redirect(to="home")
