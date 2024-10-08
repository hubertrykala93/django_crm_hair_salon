from django.contrib import admin
from .models import PrepaidTransfer, BankTransfer, CryptoTransfer, PayPalTransfer, PaymentMethod, CryptoCurrency, \
    Transaction
from .forms import AdminBankTransferForm, AdminCryptoTransferForm, AdminPrepaidTransferForm, AdminPayPalTransferForm, \
    AdminPaymentMethodForm, AdminCryptoCurrencyForm, AdminTransactionForm


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
    )


@admin.register(BankTransfer)
class AdminBankTransfer(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "user",
        "bank_name",
        "iban",
        "swift",
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
            "Related User", {
                "fields": [
                    "user",
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
                    "swift",
                    "account_number",
                ]
            }
        )
    )


@admin.register(PrepaidTransfer)
class AdminPrepaidTransfer(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "user",
        "owner_name",
        "card_number",
        "formatted_expiration_date",
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
            "Related User", {
                "fields": [
                    "user",
                ],
            },
        ),
        (
            "Owner", {
                "fields": [
                    "owner_name",
                ],
            },
        ),
        (
            "Card Information", {
                "fields": [
                    "card_number",
                    "expiration_date",
                ],
            },
        ),
    )

    def formatted_expiration_date(self, obj):
        if obj.expiration_date:
            return obj.expiration_date.strftime("%Y-%m-%d")

    formatted_expiration_date.short_description = "Expiration Date"


@admin.register(PayPalTransfer)
class AdminPayPalTransfer(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "user",
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
            "Related User", {
                "fields": [
                    "user",
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


@admin.register(CryptoCurrency)
class AdminCryptoCurrency(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "code",
    ]
    form = AdminCryptoCurrencyForm
    fieldsets = (
        (
            "Cryptocurrency", {
                "fields": [
                    "name",
                    "code",
                ],
            },
        ),
    )


@admin.register(CryptoTransfer)
class AdminCryptoTransfer(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "user",
        "cryptocurrency",
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
            "Related User", {
                "fields": [
                    "user",
                ],
            },
        ),
        (
            "Cryptocurrency", {
                "fields": [
                    "cryptocurrency",
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


@admin.register(Transaction)
class AdminTransaction(admin.ModelAdmin):
    list_display = [
        "id",
        "formatted_created_at",
        "formatted_updated_at",
        "transaction_id",
        "user",
        "description",
        "payment_method",
        "amount",
        "status",
    ]
    form = AdminTransactionForm
    fieldsets = (
        (
            "Select User", {
                "fields": [
                    "user",
                ],
            },
        ),
        (
            "Short Description", {
                "fields": [
                    "description",
                ],
            },
        ),
        (
            "Select Payment Method", {
                "fields": [
                    "payment_method",
                ],
            },
        ),
        (
            "Amount", {
                "fields": [
                    "amount",
                ],
            },
        )
    )

    def formatted_created_at(self, obj):
        if obj.created_at:
            return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")

    formatted_created_at.short_description = "Created At"

    def formatted_updated_at(self, obj):
        if obj.updated_at:
            return obj.updated_at.strftime("%Y-%m-%d %H:%M:%S")

    formatted_updated_at.short_description = "Updated At"
