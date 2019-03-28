from django.shortcuts import render
import datetime, json, pytz, datetime
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from http.client import HTTPResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from statsmodels.sandbox.distributions.sppatch import expect

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Offer):
            return str(obj)
        return super().default(obj)

# Create your views here.
@csrf_exempt
@api_view(['GET','POST'])
def Apply_view(request):
    if request.method == "POST":
        data = request.POST
        title = data['title']
        description = data['description']
        date = datetime.datetime.utcnow()
        dataScientist = DataScientist.objects.all().get(user = request.user)
        offerId = data['offerId']
        offer = Offer.objects.all().get(pk = offerId)
        #Aqu� pretendo hacer una restriccion comparando si el usuario logueado est� dentro de la lista de usuarios que han hecho apply
        #Sin embargo lo dejo comentado ya que no puedo probarlo
        #usuariosAplicados = Apply_model.objects.all().select_related("dataScientist")
        #if(not (dataScientist in usuariosAplicados)):

        new_apply = Apply.objects.create(title=title, description=description, status=Apply.STATUS_CHOICES[0][1], date=date, dataScientist = dataScientist, offer = offer)

        print('Sucessfully created new apply')
        return JsonResponse({"message":"Successfully created new apply"})
    if request.method == "GET":
        
        try:
                thisCompany = Company.objects.all().get(user = request.user) 
                offers = Offer.objects.all().filter(company = thisCompany).distinct()
                applys = []
                data = request.GET
                filtro = data['filtro']
                #TODO Cuando se realice el login lo ideal es que no se le tenga que pasar la ID del principal, sino recuperarla mediante autentificacion
                if (filtro == 'PE'):
                    for offer in offers:
                        applysInOffer = Apply.objects.all().filter(offer = offer, status = 'PE').values()
                        applys.extend(list(applysInOffer))
                if (filtro == 'AC'):
                    for offer in offers:
                        applysInOffer = Apply.objects.all().filter(offer = offer, status = 'AC').values()
                        applys.extend(list(applysInOffer))
                if (filtro == 'RE'):
                    for offer in offers:
                        applysInOffer = Apply.objects.all().filter(offer = offer, status = 'RE').values()
                        applys.extend(list(applysInOffer))
                return JsonResponse(list(applys), safe=False) 
        except:
                dataScientistRecuperado = DataScientist.objects.all().get(user = request.user)
                applys = []
                data = request.GET
                filtro = data['filtro']
                #TODO Cuando se realice el login lo ideal es que no se le tenga que pasar la ID del principal, sino recuperarla mediante autentificacion
                if (filtro == 'PE'):
                    applys = Apply.objects.all().filter(dataScientist = dataScientistRecuperado,status ='PE').values()
                if (filtro == 'AC'):
                    applys = Apply.objects.all().filter(dataScientist = dataScientistRecuperado,status ='AC').values()
                if (filtro == 'RE'):
                    applys = Apply.objects.all().filter(dataScientist = dataScientistRecuperado,status ='RE').values()
                return JsonResponse(list(applys), safe=False)

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

# Accept/Reject contract

class Contract_actions_view(APIView):
    def post(self, request, format=None):
        try:
            data = request.POST
            contractid = data['contractid']

            contract = Contract.objects.all().get(pk = contractid)
            
            logged_userid = request.user.id

            if logged_userid == contract.apply.dataScientist.id and contract.accepted_ds == None:
                accepted_ds = data['accepted_ds']

                contract.accepted_ds = accepted_ds
                contract.save()
                
                message = ""

                if accepted_ds == 'False':
                    message = "Successfully rejected contract"
                else:
                    message = "Successfully accepted contract"

                return JsonResponse({"message":message})
        except:
             return JsonResponse({"message":"Sorry! Something went wrong..."})

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
    elif request.method == 'GET':
        data = request.GET
        idUsuario = data['idUsuario']
        userRecuperado = User.objects.all().get(pk = idUsuario)
        dataScientistRecuperado = DataScientist.objects.all().get(user = userRecuperado)
        bills = []
        contracts = []
        #bills = Bill.objects.all().values()
        applies = Apply.objects.all().filter(dataScientist = dataScientistRecuperado).distinct()
        for apply in applies:
            try:
                contract = Contract.objects.all().filter(apply=apply).distinct()
            except:
                contract = None
            if (contract != None):
                contracts.extend(list(contract))
        for contract in contracts:
            try:
                bill = Bill.objects.all().filter(contract_id = contract.id).values()
            except:
                bill = None
            if (bill != None):
                bills.extend(list(bill))
        return JsonResponse(bills, safe=False)
        
@csrf_exempt
@api_view(['GET','POST'])
def Offer_view(request):
        if request.method == "POST":
            data = request.POST
            title = data['title']
            description = data['description']
            price_offered = data['price_offered']
            currency = data['currency']
            limit_time = data['limit_time']
            thisCompany = Company.objects.all().get(user = request.user)

            # Time management
            split_time = limit_time.split(',') # Split by comma what was sent from client
            split_time = list(map(int, split_time)) # Convert from list of string to list of integers

            if len(split_time) == 7:
                date = datetime.datetime(split_time[0], split_time[1],
                    split_time[2], split_time[3], split_time[4], split_time[5], split_time[6], pytz.UTC)

            # Creation of new offer
            new_offer = Offer.objects.create(title=title, description=description,
                price_offered=float(price_offered), currency=currency, limit_time=date, company = thisCompany)

            print('La data que devuelve es: ' + str(data))
            print('Sucessfully created new offer')
            return JsonResponse({"message":"Successfully created new offer"})
        if request.method == "GET":
            ofertas = []
            try:
                thisCompany = Company.objects.all().get(user = request.user)
                ofertas = Offer.objects.all().filter(company = thisCompany).values()
            except:
                date = datetime.datetime.utcnow()
                ofertas = Offer.objects.all().filter(limit_time__gte = date).values()
                
                    #else:
                     #   company = Company_model.objects.get(user = request.user)
                      #      if(company != None):
                       #         ofertas = Company_model.objects.get(user = request.user).select_related("offers")
            return JsonResponse(list(ofertas), safe=False)


class CV_view(APIView):
    def get(self, request, format=None):
        if request.method == "GET":
            data = request.GET

            items = []
            #TODO Cuando se realice el login lo ideal es que no se le tenga que pasar la ID del principal, sino recuperarla mediante autentificacion
            userId = data['userId']
            userRecuperado = User.objects.all().get(pk = userId)
            dataScientistRecuperado = DataScientist.objects.all().get(user = userRecuperado)

            # Ver mi CV
            if (dataScientistRecuperado != None):
                curriculum = CV.objects.all().filter(owner = dataScientistRecuperado).first()
                sections = Section.objects.all().filter(cv = curriculum)
                for sec in sections:
                    sec_items = Item.objects.all().filter(section = sec)
                    data_sec_items = serializers.serialize('json', sec_items)
                    items.append(data_sec_items)
            # Ver el CV de un Data scientist (como Company)
            else:
            #companyRecuperado = Company.objects.all().get(user = userRecuperado)
            #if (companyRecuperado != None):
                dataScientistId = data['dataScientistId']
                dataScientistUserRecuperado = User.objects.all().get(pk = dataScientistId)
                scientist = DataScientist.objects.all().get(user = dataScientistUserRecuperado)

                curriculum = CV.objects.all().filter(owner = scientist)
                sections = Section.objects.all().filter(cv = curriculum[0])
                for sec in sections:
                    sec_items = Item.objects.all().filter(section = sec)
                    items.append(sec_items)

            return JsonResponse(list(items), safe=False)
        
    def post(self, request, format=None):
        try:
            data = request.POST
            user = DataScientist.objects.all().get(pk = request.user.id)
            
            new_curriculum = CV.objects.create(owner=user)
            
            print('La data que devuelve es: ' + str(data))
            print('Sucessfully created new curriculum')
            return JsonResponse({"message":"Successfully created new curriculum"})
        except:
            return JsonResponse({"message":"Sorry! Something went wrong..."})

class Section_view(APIView):
    def post(self, request, format=None):
        try:
            data = request.POST
            cvid = data['cvid']

            cv = CV.objects.all().get(pk = cvid)
            logged_userid = request.user.id

            if logged_userid == cv.owner.id:
                secname = data['name']

                new_section = Section.objects.create(name = secname, cv = cv)
                    
                print('La data que devuelve es: ' + str(data))
                print('Sucessfully created new section')
                return JsonResponse({"message":"Successfully created new section"})
        except:
            return JsonResponse({"message":"Sorry! Something went wrong..."})


class Item_view(APIView):
    def post(self, request, format=None):
            try:
                data = request.POST
                
                secid = data['secid']
                section = Section.objects.all().get(pk = secid)

                logged_userid = request.user.id

                if logged_userid == section.cv.owner.id:
                    date_start = data['datestart']
                    date_finish = data['datefinish']
                    if date_start < date_finish:
                        itemname = data['name']
                        description = data['description']
                        entity = data['entity']
                        
                        new_item = Item.objects.create(name = itemname, section = section, description = description, entity = entity, date_start = date_start, date_finish = date_finish)
                        
                        print('La data que devuelve es: ' + str(data))
                        print('Sucessfully created new item')
                        return JsonResponse({"message":"Successfully created new item"})
            except:
                 return JsonResponse({"message":"Sorry! Something went wrong..."})
