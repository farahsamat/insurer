from django.db import models

# Create your models here.
class EmployeeSalary(models.Model):
    month = models.DateTimeField()
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    annual_rate = models.IntegerField()
    gross_income = models.IntegerField()
    income_tax = models.IntegerField()
    net_income = models.IntegerField()
    super_amount = models.IntegerField()
    pay_amount = models.IntegerField()
