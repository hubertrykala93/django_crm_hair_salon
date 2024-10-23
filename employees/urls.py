from django.urls import path
from . import views as employees_views

urlpatterns = [
    path(route="employees", view=employees_views.employees, name="employees"),
    path(route="delete-employee/<int:pk>", view=employees_views.delete_employee, name="delete-employee"),
    path(route="generate-contract", view=employees_views.generate_contract, name="generate-contract"),
]
