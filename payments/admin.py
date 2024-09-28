from django.contrib import admin
from .models import PrepaidTransfer, BankTransfer, CryptoTransfer, PayPalTransfer, PaymentMethod
from .forms import AdminBankTransferForm, AdminCryptoTransferForm, AdminPrepaidTransferForm, AdminPayPalTransferForm, \
    AdminPaymentMethodForm


@admin.register(PaymentMethod)
class AdminPaymentMethod(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]
    form = AdminPaymentMethodForm
    fieldsets = (
        (
            "Payment Method", {
                "fields": [
                    "name",
                ],
            },
        ),
        (
            "Additional", {
                "fields": [
                    "active",
                ],
            },
        ),
    )


@admin.register(PrepaidTransfer)
class AdminPrepaidTransfer(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "card_number",
    ]
    form = AdminPrepaidTransferForm
    fieldsets = (
        (
            "Individual Payment Method Name", {
                "fields": [
                    "name",
                ],
            },
        ),
        (
            "Card Information", {
                "fields": [
                    "card_number",
                ],
            },
        ),
    )


@admin.register(BankTransfer)
class AdminBankTransfer(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "bank_name",
        "iban",
        "account_number",
    ]
    form = AdminBankTransferForm
    fieldsets = (
        (
            "Individual Payment Method Name", {
                "fields": [
                    "name",
                ],
            },
        ),
        (
            "Bank Information", {
                "fields": [
                    "bank_name",
                ],
            },
        ),
        (
            "Account Information", {
                "fields": [
                    "iban",
                    "account_number",
                ]
            }
        )
    )


@admin.register(CryptoTransfer)
class AdminCryptoTransfer(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "wallet_address",
    ]
    form = AdminCryptoTransferForm
    fieldsets = (
        (
            "Individual Payment Method Name", {
                "fields": [
                    "name",
                ],
            },
        ),
        (
            "Wallet Information", {
                "fields": [
                    "wallet_address",
                ],
            },
        ),
    )


@admin.register(PayPalTransfer)
class AdminPayPalTransfer(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "paypal_email",
    ]
    form = AdminPayPalTransferForm
    fieldsets = (
        (
            "Individual Payment Method Name", {
                "fields": [
                    "name",
                ],
            },
        ),
        (
            "PayPal Information", {
                "fields": [
                    "paypal_email",
                ],
            },
        ),
    )
