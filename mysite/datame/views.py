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
        dataScientist = DataScientist_model.objects.filter(user = request.user)
        
        # Creation of new offer
        new_apply = Apply_model.objects.create(title=title, description=description, status=Apply_model.STATUS_CHOICES[0][1], date=date, dataScientist = dataScientist)

        print('Sucessfully created new apply')
        return JsonResponse({"message":"Successfully created new apply"})