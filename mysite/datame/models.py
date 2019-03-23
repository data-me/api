from django.db import models
from django.utils import timezone

# Create your models here.
class Bill_model(models.Model):

    STATUS_CHOICES = (
        ('PE', 'PENDING'),
        ('AC', 'ACEPTED'),
        ('RE', 'REJECTED')
    )

    quantity = models.FloatField()
    tax = models.FloatField()
    total = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField('Status',max_length = 8, choices = STATUS_CHOICES)
    #offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    #user_plan = models.ForeignKey(user_plan_model, on_delete=models.CASCADE)


    def __str__(self):
        return self.status 

class Offer_model(models.Model):
    CURRENCY_CHOICES = (
        ('0', '€'),
        ('1', '$'),
        ('2', '£')
    )

    title = models.CharField('Offer title', max_length = 80)
    description = models.TextField('Offer description')
    price_offered = models.FloatField('Price offered')
    currency = models.CharField('Currency type',max_length = 1, choices = CURRENCY_CHOICES)
    creation_date = models.DateTimeField(auto_now_add=True)
    limit_time = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title
