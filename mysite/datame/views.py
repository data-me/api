from django.shortcuts import render
import datetime
from .models import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pytz, datetime
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json


# Create your views here.
@csrf_exempt
def Apply(request):
    if request.method == "POST":
        data = request.POST
        title = data['title']
        description = data['description']
        date = datetime.datetime.utcnow()
        dataScientist = DataScientist_model.objects.all().filter(user = request.user)
        offer = data['offer']
        #Aqu� pretendo hacer una restriccion comparando si el usuario logueado est� dentro de la lista de usuarios que han hecho apply
        #Sin embargo lo dejo comentado ya que no puedo probarlo
        #usuariosAplicados = Apply_model.objects.all().select_related("dataScientist")
        #if(not (dataScientist in usuariosAplicados)):
        
        new_apply = Apply_model.objects.create(title=title, description=description, status=Apply_model.STATUS_CHOICES[0][1], date=date, dataScientist = dataScientist, offer = offer)
        
        print('Sucessfully created new apply')
        return JsonResponse({"message":"Successfully created new apply"})
    
@csrf_exempt   
def Contract(request):
    if request.method == "POST":
        data = request.POST
        limit_date = data['limit_date']
        accepted_ds = data['accepted_ds']
        accepted_company = data['accepted_company']
        expiration = data['expiration']
        dataScientist = data['dataScientist']
        offer = data['offer']
        date_created = datetime.datetime.utcnow()
        
        # Creation of new offer
        new_contract = Contract_model.objects.create(limit_date=limit_date, accepted_ds=accepted_ds, accepted_company=accepted_company, expiration=expiration, dataScientist = dataScientist, offer = offer, date_created = date_created )

        print('Sucessfully created contract')
        return JsonResponse({"message":"Successfully created new contract"})
    
@csrf_exempt   
def File(request):
    if request.method == "POST":
        data = request.POST
        name = data['name']
        path = data['path']
        apply = data['apply']
        offer = data['offer']
        
        # Creation of new offer
        new_file = File_model.objects.create(name=name, path=path, apply=apply, offer=offer)

        print('Sucessfully created File')
        return JsonResponse({"message":"Successfully created new File"})
@csrf_exempt
def Bill(request):
    if request.method == "POST":
        data = request.POST
        quantity = data['quantity']
        tax = data['tax']
        total = data['total']
        date = datetime.datetime.utcnow()
        status = data['status']
        

        # Creation of new offer
        new_bill = Bill_model.objects.create(quantity=quantity, tax=tax, total=total, date=date, status=status)
 
        print('Sucessfully created new bill')
        return JsonResponse({"message":"Successfully created new bill"})

@csrf_exempt
def Offer(request):
    try:
        if request.method == "POST":
            data = request.POST
            title = data['title']
            description = data['description']
            price_offered = data['price_offered']
            currency = data['currency']
            limit_time = data['limit_time']

            # Time management
            split_time = limit_time.split(',') # Split by comma what was sent from client 
            split_time = list(map(int, split_time)) # Convert from list of string to list of integers

            if len(split_time) == 7:
                date = datetime.datetime(split_time[0], split_time[1], 
                    split_time[2], split_time[3], split_time[4], split_time[5], split_time[6], pytz.UTC)
            
            # Creation of new offer
            new_offer = Offer_model.objects.create(title=title, description=description, 
                price_offered=float(price_offered), currency=currency, limit_time=date)

            print('La data que devuelve es: ' + str(data)) 
            print('Sucessfully created new offer')
            return JsonResponse({"message":"Successfully created new offer"})
        if request.method == "GET":
            ofertas = []
            if(request.user.is_authenticated):
                dataScientist = DataScientist_model.objects.get(user = request.user)
                if (dataScientist != None):
                    date = date.utcnow()
                    ofertas = Offer_model.objects.all().filter(limit_time__gte = date)
                #else:
                 #   company = Company_model.objects.get(user = request.user)
                  #      if(company != None):
                   #         ofertas = Company_model.objects.get(user = request.user).select_related("offers")
            return JsonResponse(ofertas)    
                

    except:
        print('La data que devuelve es: ' + str(data)) 
        