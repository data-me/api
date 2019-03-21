from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.


class DataScientist_model(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length = 30)
    surname = models.CharField('Surname', max_length = 50)
    
    def __str__(self):
        return self.name

class Offer_model(models.Model):
    CURRENCY_CHOICES = (
        ('0', '\u20ac'),
        ('1', '$'),
        ('2', '\u00a3')
    )

    title = models.CharField('Offer title', max_length = 80)
    description = models.TextField('Offer description')
    price_offered = models.FloatField('Price offered')
    currency = models.CharField('Currency type',max_length = 1, choices = CURRENCY_CHOICES)
    creation_date = models.DateTimeField(auto_now_add=True)
    limit_time = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title

class Apply_model(models.Model):
    
    STATUS_CHOICES = (
        ('PE', 'PENDING'),
        ('AC', 'ACEPTED'),
        ('RE', 'REJECTED')
    )
    
    title = models.CharField('Apply title', max_length = 80)
    description = models.TextField('Apply description')
    date = models.DateTimeField(blank=True)
    status = models.CharField('Status',max_length = 8, choices = STATUS_CHOICES)
    dataScientist = models.OneToOneField(DataScientist_model, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer_model, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title

class Contract_model(models.Model):
    
    date_created = models.DateTimeField(blank=True)
    limit_date = models.DateTimeField(blank=True)
    accepted_ds = forms.BooleanField(initial=False)
    accepted_company = forms.BooleanField(initial=True)
    expiration = models.IntegerField()
    dataScientist = models.ForeignKey(DataScientist_model, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer_model, on_delete=models.CASCADE)
    

    def __str__(self):
        cadena = self.offer.title + "//" + self.dataScientist.name
        return cadena
    
    
class File_model(models.Model):
    
    name = models.CharField('Name', max_length = 80)
    path = models.CharField('Path', max_length = 200)
    apply = models.ForeignKey(Apply_model, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer_model, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    
