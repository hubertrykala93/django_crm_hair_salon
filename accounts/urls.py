from django.urls import path
from . import views as accounts_views

urlpatterns = [
    path(
        route="choose-method",
        view=accounts_views.password_reset_method,
        name="choose-method"
    ),
    path(
        route="forgot-password",
        view=accounts_views.forgot_password,
        name="forgot-password"
    ),
    path(
        route="confirm-password",
        view=accounts_views.confirm_one_time_password,
        name="confirm-password"
    ),
    path(
        route="change-password",
        view=accounts_views.change_password,
        name="change-password"
    ),
    path(
        route="logout",
        view=accounts_views.log_out,
        name="logout"
    ),
]
