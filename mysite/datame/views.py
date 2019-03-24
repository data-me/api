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
from http.client import HTTPResponse
from django.core import serializers
from django.contrib.auth.models import User
from django import forms

# Create your views here.
@csrf_exempt
def Apply_view(request):
    if request.method == "POST":
        data = request.POST
        title = data['title']
        description = data['description']
        date = datetime.datetime.utcnow()
        dataScientist = DataScientist.objects.all().filter(user = request.user)
        offer = data['offer']
        #Aqu� pretendo hacer una restriccion comparando si el usuario logueado est� dentro de la lista de usuarios que han hecho apply
        #Sin embargo lo dejo comentado ya que no puedo probarlo
        #usuariosAplicados = Apply_model.objects.all().select_related("dataScientist")
        #if(not (dataScientist in usuariosAplicados)):

        new_apply = Apply.objects.create(title=title, description=description, status=Apply_model.STATUS_CHOICES[0][1], date=date, dataScientist = dataScientist, offer = offer)

        print('Sucessfully created new apply')
        return JsonResponse({"message":"Successfully created new apply"})
    if request.method == "GET":
        applys = []
        data = request.GET
        filtro = data['filtro']
        #TODO Cuando se realice el login lo ideal es que no se le tenga que pasar la ID del principal, sino recuperarla mediante autentificacion
        userId = data['userId']
        userRecuperado = User.objects.all().get(pk = userId)
        dataScientistRecuperado = DataScientist.objects.all().get(user = userRecuperado)
        if (filtro == 'PE'):
            applys = Apply.objects.all().filter(dataScientist = dataScientistRecuperado,status ='PE')
        if (filtro == 'AC'):
            applys = Apply.objects.all().filter(dataScientist = dataScientistRecuperado,status ='AC')
        if (filtro == 'RE'):
            applys = Apply.objects.all().filter(dataScientist = dataScientistRecuperado,status ='RE')
        dataF = serializers.serialize('json', applys)
        return JsonResponse(dataF, safe=False)

@csrf_exempt
def Contract_view(request):
    if request.method == "POST":
        data = request.POST
        limit_date = data['limit_date']
        accepted_ds = bool(data['accepted_ds'])
        accepted_company = bool(data['accepted_company'])
        expiration = data['expiration']
        dataScientistId = data['dataScientist']
        offerId = data['offer']
        date_created = datetime.datetime.utcnow()       
        dataScientist = DataScientist.objects.all().get(pk = dataScientistId)
        offer = Offer.objects.all().get(pk = offerId)
        
         # Time management
        split_time = limit_date.split(',') # Split by comma what was sent from client
        split_time = list(map(int, split_time)) # Convert from list of string to list of integers

        if len(split_time) == 7:
            date = datetime.datetime(split_time[0], split_time[1],
                split_time[2], split_time[3], split_time[4], split_time[5], split_time[6], pytz.UTC)
        
        # Creation of new offer
        new_contract = Contract.objects.create(date_created = date_created, limit_date=date, accepted_ds=accepted_ds, accepted_company=accepted_company, expiration=expiration, dataScientist = dataScientist, offer = offer)

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
        new_file = File.objects.create(name=name, path=path, apply=apply, offer=offer)

        print('Sucessfully created File')
        return JsonResponse({"message":"Successfully created new File"})

@csrf_exempt
def Bill_view(request):
    if request.method == "POST":
        data = request.POST
        quantity = data['quantity']
        tax = data['tax']
        total = data['total']
        date = datetime.datetime.utcnow()
        status = data['status']
        contractId = data['contract']
        contract = Contract.objects.all().get(pk = contractId)

        # Creation of new offer
        new_bill = Bill.objects.create(quantity=quantity, tax=tax, total=total, date=date, status=status, contract = contract)

        print('Sucessfully created new bill')
        return JsonResponse({"message":"Successfully created new bill"})

@csrf_exempt
def Offer_view(request):
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
            new_offer = Offer.objects.create(title=title, description=description,
                price_offered=float(price_offered), currency=currency, limit_time=date)

            print('La data que devuelve es: ' + str(data))
            print('Sucessfully created new offer')
            return JsonResponse({"message":"Successfully created new offer"})
        if request.method == "GET":
            ofertas = []
            date = datetime.datetime.utcnow()
            ofertas = Offer.objects.all().filter(limit_time__gte = date)
            data = serializers.serialize('json', ofertas)
                #else:
                 #   company = Company_model.objects.get(user = request.user)
                  #      if(company != None):
                   #         ofertas = Company_model.objects.get(user = request.user).select_related("offers")
            return JsonResponse(data, safe=False)


@csrf_exempt
def CV(request):
    try:
        if request.method == "GET":
            curriculum = []
            sections = []
            items = []
            if(request.user.is_authenticated):
                dataScientist = DataScientist.objects.get(user = request.user)
                # Ver mi CV
                if (dataScientist != None):
                    curriculum = CV.objects.all().filter(owner = dataScientist)
                    sections = Section.objects.all().filter(cv = curriculum[0])
                    for sec in sections:
                        sec_items = Item.objects.all().filter(section = sec)
                        items.append(sec_items);
                # Ver el CV de un Data scientist (como Company)
                else:
                    company = Company.objects.get(user = request.user)
                    if(company != None):
                        scientist = request.data.get('dataScientist')
                        Curriculum = CV.objects.all().filter(owner = scientist)
                        sections = Section.objects.all().filter(cv = curriculum[0])
                        for sec in sections:
                            sec_items = Item.objects.all().filter(section = sec)
                            items.append(sec_items);

            return JsonResponse(items)


    except:
        print('La data que devuelve es: ' + str(data))
