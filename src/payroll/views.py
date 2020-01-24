from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import EmployeeSalary
import requests
import datetime

# Create your views here.
def index(request):
    return render(request, 'index.html')

def calculate_income_tax(annual_rate):
    if annual_rate >= 18201 and annual_rate <= 37000:
        income_tax = (0.19 * (annual_rate - 18200) / 12)
        return income_tax
    elif annual_rate >= 37001 and annual_rate <= 80000:
        income_tax = (3572 + 0.325 * (annual_rate - 37000)) / 12
        return income_tax
    elif annual_rate >= 80001 and annual_rate <= 180000:
        income_tax = (17547 + 0.37 * (annual_rate - 80000)) / 12
        return income_tax
    elif annual_rate >= 180001:
        income_tax = (54547 + 0.45 * (annual_rate - 180000)) / 12
        return income_tax
    else:
        income_tax = 0
        return income_tax

def generate_payslip(request):
    if request.method == 'POST':
        last_name = (request.POST.get('user_id', None)).lower()
        first_name = (request.POST.get('benefit', None)).lower()
        annual_rate= int(request.POST.get('currency', None))
        super_rate = int(request.POST.get('total_max', None))
        income_tax = calculate_income_tax(annual_rate)
        gross_income = round(annual_rate / 12)
        net_income = gross_income - income_tax
        super_amount = round(gross_income * super_rate / 100)
        pay_amount = net_income - super_amount

        update = EmployeeSalary(last_name=last_name, first_name=first_name, annual_rate=annual_rate,
                        gross_income=gross_income, income_tax=income_tax,
                                net_income=net_income, super_amount=super_amount, pay_amount=pay_amount)
        update.save()
        return HttpResponse("salary data added")



