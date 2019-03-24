from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone

# Create your models here.


class DataScientist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length = 30)
    surname = models.CharField('Surname', max_length = 50)

    def __str__(self):
        return self.name

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length = 30)

    def __str__(self):
        return self.name


# Create your models here.
class Bill(models.Model):

    STATUS_CHOICES = (
        ('PE', 'PENDING'),
        ('AC', 'ACCEPTED'),
        ('RE', 'REJECTED')
    )

    quantity = models.FloatField()
    tax = models.FloatField()
    total = models.FloatField()
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField('Status',max_length = 8, choices = STATUS_CHOICES)
    #offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    #user_plan = models.ForeignKey(user_plan, on_delete=models.CASCADE)


    def __str__(self):
        return self.status

class Offer(models.Model):
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

class Apply(models.Model):

    STATUS_CHOICES = (
        ('PE', 'PENDING'),
        ('AC', 'ACEPTED'),
        ('RE', 'REJECTED')
    )

    title = models.CharField('Apply title', max_length = 80)
    description = models.TextField('Apply description')
    date = models.DateTimeField(blank=True)
    status = models.CharField('Status',max_length = 8, choices = STATUS_CHOICES)
    dataScientist = models.OneToOneField(DataScientist, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

class Contract(models.Model):

    date_created = models.DateTimeField(blank=True)
    limit_date = models.DateTimeField(blank=True)
    accepted_ds = forms.BooleanField(initial=False)
    accepted_company = forms.BooleanField(initial=True)
    expiration = models.IntegerField()
    dataScientist = models.ForeignKey(DataScientist, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)


    def __str__(self):
        cadena = self.offer.title + "//" + self.dataScientist.name
        return cadena


class File(models.Model):

    name = models.CharField('Name', max_length = 80)
    path = models.CharField('Path', max_length = 200)
    apply = models.ForeignKey(Apply, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Curriculum vitae
class CV(models.Model):
    owner = models.OneToOneField('datame.DataScientist', default = "", on_delete = models.CASCADE)

    def __str__(self):
        return self.owner.name

# Sections of a curriculum
class Section(models.Model):
    name = models.CharField("Section name", max_length = 50)
    cv = models.ForeignKey("datame.CV", on_delete = models.CASCADE, related_name = 'sections')

    def __str__(self):
        return self.name

# Items of a section
class Item(models.Model):
    name = models.CharField("Name", max_length=50)
    section = models.ForeignKey("datame.Section", on_delete = models.CASCADE, related_name = 'items')
    description = models.CharField("Description", max_length=100)
    entity = models.CharField("Entity", max_length=50)
    date_start = models.DateTimeField("Start date")
    date_finish = models.DateTimeField("End date", blank=True, null=True)

    def __str__(self):
        return self.name
