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
from django.contrib.auth.models import Group
from django.core.serializers.json import DjangoJSONEncoder
from django import forms
from statsmodels.sandbox.distributions.sppatch import expect
from django.forms.models import model_to_dict
from django.db.models import Q

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Offer):
            return str(obj)
        return super().default(obj)


@csrf_exempt
@api_view(['GET','POST'])
def Message_view(request):
    if request.method == "POST":
        data = request.POST
        title = data['title']
        body = data['body']
        moment = datetime.datetime.utcnow()
        #receiverId = User.objects.all().get(user = data['receiverId'])
        receiverId = data['receiverId']
        receiver = User.objects.all().get(pk = receiverId)
        senderId = request.user
        print(senderId)

        new_message = Message.objects.create(title=title, body=body, moment=moment, receiver=receiver, sender=senderId)

        print('Sucessfully created new message')
        return JsonResponse({"message":"Successfully created new message"})
    if request.method == "GET":
        data = request.GET
        user = request.user
        messages = []
        try:
            messages = Message.objects.all().filter(receiver = user).values()
            print(messages)
        except:
            print("You have 0 messages")

        return JsonResponse(list(messages), safe=False)


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
        applysInOffer = Apply.objects.all().filter(offer = offer)
        for apply in applysInOffer:
            if(apply.dataScientist.id == dataScientist.id):
                return JsonResponse({"message":"DataScientist already applied"})
        #Aqu� pretendo hacer una restriccion comparando si el usuario logueado est� dentro de la lista de usuarios que han hecho apply
        #Sin embargo lo dejo comentado ya que no puedo probarlo
        #usuariosAplicados = Apply_model.objects.all().select_related("dataScientist")
        #if(not (dataScientist in usuariosAplicados)):

        new_apply = Apply.objects.create(title=title, description=description, status='PE', date=date, dataScientist = dataScientist, offer = offer)

        return JsonResponse({"message":"Successfully created new apply"})
    if request.method == "GET":
        user_logged = User.objects.all().get(pk = request.user.id)
        if (user_logged.groups.filter(name='Company').exists()):
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
        elif(user_logged.groups.filter(name='DataScientist').exists()):
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

# Accept/Reject contract

class AcceptApply_view(APIView):
    def post(self, request, format=None):
        user_logged = User.objects.all().get(pk = request.user.id)
        if (user_logged.groups.filter(name='Company').exists()):
            company = Company.objects.all().get(user = user_logged)
            data = request.POST
            idApply = data['idApply']
            apply = Apply.objects.all().get(pk = idApply)
            if(apply.offer.company == company):
                if (apply.offer.finished == True):
                    res = JsonResponse({"message":"Offer has been already accepted"})
                else:
                    applysToUpdate = Apply.objects.all().filter(offer = apply.offer).update(status = 'RE')
                    apply.status = 'AC'
                    apply.save()
                    apply.offer.finished = True
                    apply.offer.save()
                    res = JsonResponse(model_to_dict(apply), safe=False)
            else:
               res = JsonResponse({"message":"The company doesnt own the offer"})
        else:
            res = JsonResponse({"message":"Only companies can update an apply"})
        return res


class Offer_view(APIView):
    def get(self, request, format=None):
        try:
            data = request.GET
            if data.get('search') != None:
                date = datetime.datetime.utcnow()
                ofertas = Offer.objects.filter(Q(title__contains = data['search']) | Q(description__contains = data['search']), limit_time__gte = date, finished=False).values()
                return JsonResponse(list(ofertas), safe=False)
            else:
                ofertas = []
                try:
                    thisCompany = Company.objects.all().get(user = request.user)
                    # All offers instead only those who don't have an applicant
                    ofertas = Offer.objects.all().filter(company = thisCompany).values()
                except:
                    date = datetime.datetime.utcnow()
                    # All offers whos time has not come yet, have to filter it doesn't have an applicant yet
                    ofertas = Offer.objects.all().filter(limit_time__gte = date, finished=False).values()
                return JsonResponse(list(ofertas), safe=False)
        except:
            return JsonResponse({"message":"Sorry! Something went wrong..."})
    def post(self, request, format=None):
        try:
            data = request.POST
            title = data['title']
            description = data['description']
            price_offered = data['price_offered']
            currency = data['currency']
            limit_time = data['limit_time']
            contract = data['contract']
            files = data['files']
            thisCompany = Company.objects.all().get(user = request.user)
            # Time management
            split_time = limit_time.split(',') # Split by comma what was sent from client
            split_time = list(map(int, split_time)) # Convert from list of string to list of integers

            if len(split_time) == 7:
                date = datetime.datetime(split_time[0], split_time[1],
                    split_time[2], split_time[3], split_time[4], split_time[5], split_time[6], pytz.UTC)

            # Creation of new offer

            new_offer = Offer.objects.create(title=title, description=description, price_offered=float(price_offered), currency=currency, limit_time=date, contract=contract, files=files, company = thisCompany)

            print('La data que devuelve es: ' + str(data))
            print('Sucessfully created new offer')
            return JsonResponse({"message":"Successfully created new offer"})
        except Exception as e:
            print('execeptio', e)
            return JsonResponse({"message":"Sorry! Something went wrong..."})


class Company_view(APIView):
    def get(self, request, format=None):
        if request.method == "GET":
            data = request.GET
            logged_user = User.objects.all().get(pk = request.user.id)
            print('logged_user: ' + str(logged_user))
            #company = []
            try:
                    companyRecuperada = Company.objects.all().get(user = logged_user)
                    thiscompany = Company.objects.all().filter(user = logged_user).values()
            except:
                    companyId = data['companyId']
                    companyUserRecuperado = User.objects.all().get(pk = companyId)
                    print('company user recuperada: ' + str(companyUserRecuperado))
                    thiscompany = Company.objects.all().filter(user = companyUserRecuperado).values()
                    print('company recuperada: ' + str(thiscompany))


            return JsonResponse(list(thiscompany), safe=False)


class CV_view(APIView):
    def get(self, request, format=None):
        if request.method == "GET":
            data = request.GET
            items = []
            logged_user = User.objects.all().get(pk = request.user.id)
            try:
                    #Ver mi CV
                    dataScientistRecuperado = DataScientist.objects.all().get(user = logged_user)
                    curriculum = CV.objects.all().filter(owner = dataScientistRecuperado).first()
                    sections = Section.objects.all().filter(cv = curriculum)
                    for sec in sections:
                        sec_items = Item.objects.all().filter(section = sec).values()
                        items.extend(sec_items)

            except:
                    #Ver CV de otro
                    dataScientistId = data['dataScientistId']
                    dataScientistUserRecuperado = User.objects.all().get(pk = dataScientistId)
                    scientist = DataScientist.objects.all().get(user = dataScientistUserRecuperado)
                    curriculum = CV.objects.all().filter(owner = scientist).first()
                    sections = Section.objects.all().filter(cv = curriculum)
                    for sec in sections:
                        sec_items = Item.objects.all().filter(section = sec).values()
                        items.extend(sec_items)

            return JsonResponse(list(items), safe=False)

    def post(self, request, format=None):
        try:
            data = request.POST
            logged_user = DataScientist.objects.all().get(pk = request.user.datascientist.id)

            new_curriculum = CV.objects.create(owner=logged_user)

            print('La data que devuelve es: ' + str(data))
            print('Sucessfully created new curriculum')
            return JsonResponse({"message":"Successfully created new curriculum"})
        except:
            return JsonResponse({"message":"Sorry! Something went wrong..."})

class Create_section_name(APIView):
    def post(self, request, format=None):
        try:
            if request.user.is_superuser or request.user.is_staff:
                data = request.POST

                new_section_name = Section_name.objects.create(name = data['name'])

                return JsonResponse({"message":"Successfully created new section name"})

            else:
                return JsonResponse({"message":"You do not have permission to perform this action"})
        except:
            return JsonResponse({"message":"Sorry! Something went wrong..."})


class Section_view(APIView):
    def post(self, request, format=None):
        try:
            data = request.POST
            sec = Section_name.objects.all().get(name = data['name'])

            logged_user = DataScientist.objects.all().get(pk = request.user.datascientist.id)

            cv = CV.objects.all().get(owner = logged_user)

            new_section = Section.objects.create(name = sec, cv = cv)

            return JsonResponse({"message":"Successfully created new section"})
        except:
            return JsonResponse({"message":"Sorry! Something went wrong..."})


class Item_view(APIView):
    def post(self, request, format=None):
            try:
                data = request.POST

                secid = data['secid']
                
                section = Section.objects.all().get(pk = secid)
            
                logged_userid = request.user.datascientist.id

                if logged_userid == section.cv.owner.user_id:

                    date_start = data['datestart']
                    date_finish = request.POST.get('datefinish')

                    if date_finish != None: 
                        if date_start < date_finish:
                        
                            try:
                                item_tosave = Item.objects.all().get(pk = data['itemid'])

                                item_tosave.name = data['name']
                                item_tosave.description = data['description']
                                item_tosave.entity = data['entity']
                                item_tosave.date_start = date_start
                                item_tosave.date_finish = date_finish

                                item_tosave.save()

                                return JsonResponse({"message":"Successfully edited item"})
                            except:
                                itemname = data['name']
                                description = data['description']
                                entity = data['entity']

                                new_item = Item.objects.create(name = itemname, section = section, description = description, entity = entity, date_start = date_start, date_finish = date_finish)

                                return JsonResponse({"message":"Successfully created new item"})
                        else:
                            return JsonResponse({"message":"Sorry, the starting date must be before the ending date!"})
                    else:
                        try:
                            print('olawenas')
                            item_tosave = Item.objects.all().get(pk = data['itemid'])

                            item_tosave.name = data['name']
                            item_tosave.description = data['description']
                            item_tosave.entity = data['entity']
                            item_tosave.date_start = date_start

                            item_tosave.save()

                            return JsonResponse({"message":"Successfully edited item"})
                        except:
                            print('olawenas')
                            itemname = data['name']
                            description = data['description']
                            entity = data['entity']

                            new_item = Item.objects.create(name = itemname, section = section, description = description, entity = entity, date_start = date_start)

                            return JsonResponse({"message":"Successfully created new item"})
            except:
                return JsonResponse({"message":"Sorry! Something went wrong..."})
