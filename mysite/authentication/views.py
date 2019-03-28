from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from datame.models import Company
from authentication.serializers import CompanySerializer


class HelloWorld(APIView):
    def get(self, request, format=None):
        saludo = 'Hola, ' + str(request.user) + '!'
        return Response({'saludo':saludo})


class ListCompanies(APIView):
    def get(self, request, format=None):

        companies = Company.objects.all() # TODO: Hacer paginación

        serializer = CompanySerializer(companies,many=True)

        return Response({ 'companies' : serializer.data})

