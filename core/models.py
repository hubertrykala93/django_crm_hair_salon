from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
