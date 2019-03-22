from django.shortcuts import render
import datetime
from .models import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pytz, datetime

# Create your views here.

def hi(request):
    if request.method == 'GET':
        data = {"response": "hi"}
        return JsonResponse(data)


@csrf_exempt
def Bill(request):
    if request.method == "POST":
        data = request.POST
        quantity = data['quantity']
        tax = data['tax']
        total = data['total']
        date = datetime.datetime.utcnow()
        

        # Creation of new offer
        new_bill = Bill_model.objects.create(quantity=quantity, tax=tax, total=total, date=date, status=Bill_model.STATUS_CHOICES[0][1])
 
        print(new_bill)
        print('Sucessfully created new bill')
        return JsonResponse({"message":"Successfully created new bill"})