from django.db import models

# Create your models here.
AUTHORIZATION = [("true", "true"), ("false","false")]

class Policy(models.Model):
    external_user_id = models.CharField(max_length=50)
    benefit = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    total_max_amount = models.IntegerField()
    #total_max_amount = models.CharField(max_length=50)

    def __str__(self):
        template = '{0.external_user_id} {0.benefit} {0.currency} {0.total_max_amount}'
        return template.format(self)

class Payment(models.Model):
    external_user_id = models.CharField(max_length=50)
    benefit = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    amount = models.IntegerField()
    #amount = models.CharField(max_length=50)
    authorization = models.CharField(max_length=5, choices=AUTHORIZATION, default="false")
    timestamp = models.DateTimeField('Timestamp')

    def __str__(self):
        template = '{0.external_user_id} {0.benefit} {0.currency} {0.amount} {0.authorization} {0.timestamp}'
        return template.format(self)