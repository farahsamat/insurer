from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home),
    path('policy-list', views.policy_list),
    path('policy', views.add_policy),
    path('payment-list', views.payment_list),
    path('payment', views.make_payment),
]