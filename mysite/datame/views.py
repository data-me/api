from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Offer_model
import pytz, datetime

# Create your views here.
@csrf_exempt
def Offer(request):
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

        print('Sucessfully created new offer')
        return JsonResponse({"message":"Successfully created new offer"})