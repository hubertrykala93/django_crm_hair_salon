from django.urls import path
from . import views as invoices_views

urlpatterns = [
    path(route="generate-invoice", view=invoices_views.generate_invoice, name="generate-invoice"),
]
