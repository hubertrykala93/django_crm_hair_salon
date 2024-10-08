from django.db import models
from payments.models import PaymentMethod
from datetime import timedelta
from django.utils.text import slugify


class Currency(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Currency, self).save(*args, **kwargs)


class PaymentFrequency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)

    class Meta:
        verbose_name = "Payment Frequency"
        verbose_name_plural = "Payments Frequency"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(PaymentFrequency, self).save(*args, **kwargs)


class JobType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)

    class Meta:
        verbose_name = "Job Type"
        verbose_name_plural = "Job Types"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(JobType, self).save(*args, **kwargs)


class SportBenefit(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)

    class Meta:
        verbose_name = "Sport Benefit"
        verbose_name_plural = "Sport Benefits"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(SportBenefit, self).save(*args, **kwargs)


class HealthBenefit(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)

    class Meta:
        verbose_name = "Health Benefit"
        verbose_name_plural = "Health Benefits"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(HealthBenefit, self).save(*args, **kwargs)


class InsuranceBenefit(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)

    class Meta:
        verbose_name = "Insurance Benefit"
        verbose_name_plural = "Insurance Benefits"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(InsuranceBenefit, self).save(*args, **kwargs)


class DevelopmentBenefit(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)

    class Meta:
        verbose_name = "Development Benefit"
        verbose_name_plural = "Development Benefits"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(DevelopmentBenefit, self).save(*args, **kwargs)


class Benefit(models.Model):
    sport_benefits = models.ManyToManyField(to=SportBenefit)
    health_benefits = models.ManyToManyField(to=HealthBenefit)
    insurance_benefits = models.ManyToManyField(to=InsuranceBenefit)
    development_benefits = models.ManyToManyField(to=DevelopmentBenefit)

    class Meta:
        verbose_name = "Benefit"
        verbose_name_plural = "Benefits"

    def __str__(self):
        return str(self.pk)


class ContractType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)

    class Meta:
        verbose_name = "Contract Type"
        verbose_name_plural = "Contract Types"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(ContractType, self).save(*args, **kwargs)


class JobPosition(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, null=True)

    class Meta:
        verbose_name = "Job Position"
        verbose_name_plural = "Job Positions"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(JobPosition, self).save(*args, **kwargs)


class EmploymentStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)

    class Meta:
        verbose_name = "Employment Status"
        verbose_name_plural = "Employment Statuses"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(EmploymentStatus, self).save(*args, **kwargs)


class Contract(models.Model):
    contract_type = models.ForeignKey(to=ContractType, on_delete=models.SET_NULL, null=True, blank=True)
    job_type = models.ForeignKey(to=JobType, on_delete=models.SET_NULL, null=True, blank=True)
    job_position = models.ForeignKey(to=JobPosition, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    time_remaining = models.DurationField(null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.ForeignKey(to=Currency, on_delete=models.SET_NULL, null=True, blank=True)
    payment_frequency = models.ForeignKey(to=PaymentFrequency, on_delete=models.SET_NULL, null=True)
    payment_method = models.ForeignKey(to=PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    work_hours_per_week = models.IntegerField(null=True, blank=True)
    benefits = models.OneToOneField(to=Benefit, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(to=EmploymentStatus, on_delete=models.SET_NULL, null=True)
    invoices = models.ManyToManyField(to="invoices.Invoice")
    total_invoices = models.IntegerField(default=0, null=True)
    total_earnings_gross = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True)
    total_earnings_net = models.DecimalField(default=0, max_digits=10, decimal_places=2, null=True)

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.end_date and self.start_date:
            self.time_remaining = self.end_date - self.start_date

            if self.time_remaining < timedelta(days=0):
                self.status = EmploymentStatus.objects.get(name="Inactive")

            else:
                self.status = EmploymentStatus.objects.get(name="Active")

        else:
            self.time_remaining = None

        super(Contract, self).save(*args, **kwargs)
