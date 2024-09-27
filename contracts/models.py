from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, unique=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return str(self.pk)


class PaymentFrequency(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Payment Frequency"
        verbose_name_plural = "Payments Frequency"

    def __str__(self):
        return str(self.pk)


class JobType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)

    class Meta:
        verbose_name = "Job Type"
        verbose_name_plural = "Job Types"

    def __str__(self):
        return self.name


class SalaryPeriod(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Salary Period"
        verbose_name_plural = "Salary Periods"

    def __str__(self):
        return self.name


class SalaryBenefit(models.Model):
    date_of_award = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    period = models.ForeignKey(to=SalaryPeriod, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Salary Benefit"
        verbose_name_plural = "Salary Benefits"

    def __str__(self):
        return str(self.pk)


class SportBenefit(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)

    class Meta:
        verbose_name = "Sport Benefit"
        verbose_name_plural = "Sport Benefits"

    def __str__(self):
        return self.name


class HealthBenefit(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)

    class Meta:
        verbose_name = "Health Benefit"
        verbose_name_plural = "Health Benefits"

    def __str__(self):
        return self.name


class InsuranceBenefit(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)

    class Meta:
        verbose_name = "Insurance Benefit"
        verbose_name_plural = "Insurance Benefits"

    def __str__(self):
        return self.name


class DevelopmentBenefit(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)

    class Meta:
        verbose_name = "Development Benefit"
        verbose_name_plural = "Development Benefits"

    def __str__(self):
        return self.name


class Benefit(models.Model):
    job_type = models.ForeignKey(to=JobType, on_delete=models.SET_NULL, null=True, blank=True)
    salary_benefits = models.ManyToManyField(to=SalaryBenefit)
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

    class Meta:
        verbose_name = "Contract Type"
        verbose_name_plural = "Contract Types"

    def __str__(self):
        return self.name


class JobPosition(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = "Job Position"
        verbose_name_plural = "Job Positions"

    def __str__(self):
        return self.name


class EmploymentStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Employment Status"
        verbose_name_plural = "Employment Statuses"

    def __str__(self):
        return self.name


class Contract(models.Model):
    contract_type = models.ForeignKey(to=ContractType, on_delete=models.SET_NULL, null=True, blank=True)
    job_type = models.ForeignKey(to=JobType, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.ForeignKey(to=Currency, on_delete=models.SET_NULL, null=True, blank=True)
    payment_frequency = models.ForeignKey(to=PaymentFrequency, on_delete=models.SET_NULL, null=True)
    work_hours_per_week = models.IntegerField(null=True, blank=True)
    benefits = models.OneToOneField(to=Benefit, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    def __str__(self):
        return str(self.pk)
