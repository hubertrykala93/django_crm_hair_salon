from django.contrib import admin
from .models import PrepaidTransfer, BankTransfer, CryptoTransfer, PayPalTransfer, PaymentMethod
from .forms import AdminBankTransferForm, AdminCryptoTransferForm, AdminPrepaidTransferForm, AdminPayPalTransferForm, \
    AdminPaymentMethodForm


@admin.register(PrepaidTransfer)
class AdminPrepaidTransfer(admin.ModelAdmin):
    list_display = [
        "id",
        "card_number",
    ]
    form = AdminPrepaidTransferForm
    fieldsets = (
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
        "bank_name",
        "iban",
        "account_number",
    ]
    form = AdminBankTransferForm
    fieldsets = (
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
        "wallet_address",
    ]
    form = AdminCryptoTransferForm
    fieldsets = (
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
        "paypal_email",
    ]
    form = AdminPayPalTransferForm
    fieldsets = (
        (
            "PayPal Information", {
                "fields": [
                    "paypal_email",
                ],
            },
        ),
    )
