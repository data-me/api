from django.shortcuts import render
import datetime
from .models import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import pytz, datetime

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
        #Aquí pretendo hacer una restriccion comparando si el usuario logueado está dentro de la lista de usuarios que han hecho apply
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
