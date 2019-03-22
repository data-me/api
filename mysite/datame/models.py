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
