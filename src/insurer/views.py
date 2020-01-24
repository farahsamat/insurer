from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Policy, Payment
from .serializers import PolicySerializer, PaymentSerializer
import requests
import datetime


def index(request):
    return render(request, 'index.html')

def policy_list(request):
    if request.method == 'GET':
        policy = Policy.objects.all()
        serializer = PolicySerializer(policy, many=True)
        return JsonResponse(serializer.data, safe=False)

    else:
        return render(request, 'policy.html')

def add_policy(request):
    if request.method == 'POST':
        response = requests.get('http://127.0.0.1:8000/insurer/policy-list')
        data = response.json()
        user_id = (request.POST.get('user_id', None)).lower()
        benefit = (request.POST.get('benefit', None)).lower()
        currency = (request.POST.get('currency', None)).lower()
        total_max = int(request.POST.get('total_max', None))

        for record in data:
            if record["external_user_id"].lower() == user_id and record["benefit"].lower() == benefit and \
                    record["currency"].lower() == currency:
                return HttpResponse("policy exists")
            elif len(data)==0:
                update = Policy(external_user_id=user_id, benefit=benefit, currency=currency,
                                total_max_amount=total_max)
                update.save()
                return HttpResponse("policy added")
            else:
                update = Policy(external_user_id=user_id, benefit=benefit, currency=currency,
                                total_max_amount=total_max)
                update.save()
                return HttpResponse("policy added")

    else:
        return render(request, 'policy.html')

def payment_list(request):
    if request.method == 'GET':
        payment = Payment.objects.all()
        serializer = PaymentSerializer(payment, many=True)
        return JsonResponse(serializer.data, safe=False)

    else:
        return render(request, 'payment.html')

def make_payment(request):
    pay_r = requests.get('http://127.0.0.1:8000/insurer/payment-list')
    payment_data = pay_r.json()

    pol_r = requests.get('http://127.0.0.1:8000/insurer/policy-list')
    pol_data = pol_r.json()

    if request.method == 'POST':
        user_id = request.POST.get('user_id', None).lower()
        benefit = request.POST.get('benefit', None).lower()
        currency = request.POST.get('currency', None).lower()
        amount = int(request.POST.get('amount', None))
        prev_authorized_claim = 0
        total_max = 0

        for policy, payment in zip(pol_data, payment_data):
            if payment["authorization"]=='true' and payment["external_user_id"].lower() == user_id and payment["benefit"].lower() == benefit and payment["currency"].lower() == currency:
                if policy["external_user_id"].lower() == payment["external_user_id"].lower() and policy["benefit"].lower() == payment["benefit"].lower() and policy["currency"].lower() == payment["currency"].lower() and payment:
                    prev_authorized_claim += payment["amount"]
                    total_max = policy["total_max_amount"]

            elif payment["authorization"]=='false' and payment["external_user_id"].lower() == user_id and payment["benefit"].lower() == benefit and payment["currency"].lower() == currency:
                if policy["external_user_id"].lower() == payment["external_user_id"].lower() and policy["benefit"].lower() == payment["benefit"].lower() and policy["currency"].lower() == payment["currency"].lower() and payment:
                    prev_authorized_claim += 0
                    total_max = policy["total_max_amount"]
            else:
                return HttpResponse("policy does not exist")

        total_claim = prev_authorized_claim + amount
        if total_claim <= total_max:
            authorization = 'true'
            #update payment database
            update = Payment(external_user_id=user_id, benefit=benefit, currency=currency,
                            amount=amount, authorization=authorization, timestamp=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat())
            update.save()
            return HttpResponse("Payment successful")

        elif total_claim >= total_max:
            authorization = 'false'
            #update payment database
            update = Payment(external_user_id=user_id, benefit=benefit, currency=currency,
                            amount=amount, authorization=authorization,
                            timestamp=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat())
            update.save()
            return HttpResponse("Exceeds total max amount")

    else:
        return render(request, 'payment.html')
