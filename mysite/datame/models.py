from django.db import models


# Create your models here.


class DataScientist_model(models.Model):
    name = models.CharField('Name', max_length = 30)
    surname = models.CharField('Surname', max_length = 50)
    
    def __str__(self):
        return self.name


class Apply_model(models.Model):
    
    STATUS_CHOICES = (
        ('PE', 'PENDING'),
        ('AC', 'ACEPTED'),
        ('RE', 'REJECTED')
    )
    
    title = models.CharField('Offer title', max_length = 80)
    description = models.TextField('Apply description')
    date = models.DateTimeField(blank=True)
    status = models.CharField('Status',max_length = 8, choices = STATUS_CHOICES)
    dataScientist = models.ForeignKey(DataScientist_model, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title
    
