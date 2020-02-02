from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Policy, Payment
from .serializers import PolicySerializer, PaymentSerializer
import requests
import datetime
import string
import re

chars = re.escape(string.punctuation)

def home(request):
    return render(request, 'home.html')

def policy_list(request):
    if request.method == 'GET':
        policy = Policy.objects.all()
        serializer = PolicySerializer(policy, many=True)
        return JsonResponse(serializer.data, safe=False)

    else:
        return render(request, 'policy.html')

def add_policy(request):
    if request.method == 'POST':
        policy_url = 'http://127.0.0.1:8000/policy-list'
        data = requests.get(policy_url).json()

        #get user input
        user_id = request.POST.get('user_id', None).lower()
        benefit = request.POST.get('benefit', None).lower()
        currency = request.POST.get('currency', None).lower()
        total_max = int(request.POST.get('total_max', None))
        policy_query = user_id+benefit+currency
        existing_policy = [record["external_user_id"].lower()+record["benefit"].lower()+record["currency"].lower() for record in data]

        if policy_query not in existing_policy:
            update = Policy(external_user_id=user_id, benefit=benefit, currency=currency,
                            total_max_amount=total_max)
            update.save()
            return HttpResponse("policy added")

        else:
            return HttpResponse("policy exists")

    else:
        return render(request, 'policy.html')

####PAYMENT####
def payment_list(request):
    if request.method == 'GET':
        payment = Payment.objects.all()
        serializer = PaymentSerializer(payment, many=True)
        return JsonResponse(serializer.data, safe=False)

    else:
        return render(request, 'payment.html')

def make_payment(request):
    if request.method == 'POST':
        policy_url = 'http://127.0.0.1:8000/policy-list'
        policy_data = requests.get(policy_url).json()

        payment_url = 'http://127.0.0.1:8000/payment-list'
        payment_data = requests.get(payment_url).json()

        #user input
        user_id = request.POST.get('user_id', None).lower()
        benefit = request.POST.get('benefit', None).lower()
        currency = request.POST.get('currency', None).lower()
        amount = int(request.POST.get('amount', None))

        policy_query = user_id + benefit + currency
        prev_authorized_claim = 0

        for policy_record in policy_data:
            if policy_query == policy_record["external_user_id"].lower() + policy_record["benefit"].lower() + policy_record["currency"].lower():
                total_max = policy_record["total_max_amount"]

                for payment_record in payment_data:
                    if payment_record["authorization"] == 'true':
                        prev_authorized_claim += payment_record["amount"]
                    elif payment_record["authorization"] == 'false':
                        prev_authorized_claim += 0
                    else:
                        prev_authorized_claim += 0

                    total_claim = prev_authorized_claim + amount

                    if total_claim <= total_max:
                        authorization = 'true'
                        # update payment database
                        update = Payment(external_user_id=user_id, benefit=benefit, currency=currency,
                                         amount=amount, authorization=authorization,
                                         timestamp=datetime.datetime.utcnow().replace(
                                             tzinfo=datetime.timezone.utc).isoformat())
                        update.save()
                        return HttpResponse("Payment successful")

                    elif total_claim >= total_max:
                        authorization = 'false'
                        # update payment database
                        update = Payment(external_user_id=user_id, benefit=benefit, currency=currency,
                                         amount=amount, authorization=authorization,
                                         timestamp=datetime.datetime.utcnow().replace(
                                             tzinfo=datetime.timezone.utc).isoformat())
                        update.save()
                        return HttpResponse("POLICY_AMOUNT_EXCEEDED")
            else:
                return HttpResponse("POLICY_NOT_FOUND")

    else:
        return render(request, 'payment.html')
