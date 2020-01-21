from django.db import models

# Create your models here.
AUTHORIZATION = [("true", "true"), ("false","false")]

class Policy(models.Model):
    external_user_id = models.CharField(max_length=50)
    benefit = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    total_max_amount = models.IntegerField()

class Payment(models.Model):
    external_user_id = models.CharField(max_length=50)
    benefit = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    amount = models.IntegerField()
    authorization = models.CharField(max_length=5, choices=AUTHORIZATION, default="false")
    timestamp = models.DateTimeField('Timestamp')