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

# Accept/Reject contract



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
            logged_user = User.objects.all().get(pk = request.user.id)
            try:
                    #Ver mi CV
                    dataScientistRecuperado = DataScientist.objects.all().get(user = logged_user)
                    curriculum = CV.objects.all().filter(owner = dataScientistRecuperado).first()
                    sections = Section.objects.all().filter(cv = curriculum)
                    for sec in sections:
                        sec_items = Item.objects.all().filter(section = sec)
                        data_sec_items = serializers.serialize('json', sec_items)
                        items.append(data_sec_items)

            except:
                    #Ver CV de otro
                    dataScientistId = data['dataScientistId']
                    dataScientistUserRecuperado = User.objects.all().get(pk = dataScientistId)
                    scientist = DataScientist.objects.all().get(user = dataScientistUserRecuperado)
                    curriculum = CV.objects.all().filter(owner = scientist).first()
                    sections = Section.objects.all().filter(cv = curriculum)
                    for sec in sections:
                        sec_items = Item.objects.all().filter(section = sec)
                        data_sec_items = serializers.serialize('json', sec_items)
                        items.append(data_sec_items)

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

                logged_userid = request.user.id

                if logged_userid == section.cv.owner.user_id:
                    date_start = data['datestart']
                    date_finish = data['datefinish']

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
            except:
                return JsonResponse({"message":"Sorry! Something went wrong..."})
