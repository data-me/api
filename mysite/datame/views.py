from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def hi(request):
    if request.method == 'GET':
        data = {"response": "hi"}
        return JsonResponse(data)
