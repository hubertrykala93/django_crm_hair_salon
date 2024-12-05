from django.db import models
from accounts.models import User
from django.utils.text import slugify
from django.utils.timezone import now
import os
from PIL import Image


class ServiceCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def save(self, *args, **kwargs):
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


class ServiceImage(models.Model):
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="services")
    size = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    format = models.CharField(max_length=100, null=True)
    alt = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = "Service Image"
        verbose_name_plural = "Service Images"

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.pk:
            super(ServiceImage, self).save(*args, **kwargs)

            self._resize_image()
            self._save_attributes()

            super(ServiceImage, self).save(*args, **kwargs)

        else:
            super(ServiceImage, self).save(*args, **kwargs)
            self._resize_image()
            self._save_attributes()

            super(ServiceImage, self).save(*args, **kwargs)

    def _resize_image(self):
        image = Image.open(fp=self.image.path)

        if image.mode == "RGBA":
            image = image.convert(mode="RGB")

        max_width = 1200

        width_percent = max_width / float(image.size[0])
        new_height = int((float(image.size[1]) * float(width_percent)))

        new_size = (max_width, new_height)
        image = image.resize(new_size, Image.LANCZOS)

        image.save(fp=self.image.path, quality=85)

        return image

    def _save_attributes(self):
        image = self._resize_image()

        self.size = os.path.getsize(filename=self.image.path)
        self.width, self.height = image.width, image.height
        self.format = self.image.name.split(".")[-1]


class Service(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.OneToOneField(to=ServiceImage, on_delete=models.SET_NULL, null=True)
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
        self.slug = slugify(self.name)

        if self.gross_price is None:
            self.gross_price = self.net_price * (1 + self.tax_rate.rate)

        super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
