from django.urls import path
from . import views as core_views

urlpatterns = [
    path(route="dashboard", view=core_views.dashboard, name="dashboard"),
]
