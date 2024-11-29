from django.db import models
from accounts.models import User
from django.utils.text import slugify


class ServiceCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(ServiceCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ServiceTaxRate(models.Model):
    rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.23)

    class Meta:
        verbose_name = "Service Tax Rate"
        verbose_name_plural = "Services Tax Rate"

    def __str__(self):
        return str(self.rate)


class Service(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    employees = models.ManyToManyField(to=User)
    description = models.TextField()
    category = models.ForeignKey(to=ServiceCategory, on_delete=models.SET_NULL, null=True)
    duration = models.PositiveIntegerField()
    tax_rate = models.ForeignKey(to=ServiceTaxRate, on_delete=models.SET_NULL, null=True)
    net_price = models.DecimalField(max_digits=5, decimal_places=2)
    gross_price = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        if self.net_price is None and self.gross_price is not None:
            self.net_price = self.gross_price / (1 + self.tax_rate)

        elif self.gross_price is None and self.net_price is not None:
            self.gross_price = self.net_price * (1 + self.tax_rate)

        if self.gross_price is None and self.net_price is None:
            raise ValueError("At least one of Net Price or Gross Price must be provided.")

        super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
