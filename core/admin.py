from django.contrib import admin
from .models import Company


@admin.register(Company)
class AdminCompany(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
    ]
