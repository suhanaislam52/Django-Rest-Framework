from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def home(request):
    return Response({'status': 200, 'message': "Hello from django rest"})
# Create your views here.
