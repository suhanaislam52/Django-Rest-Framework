from django.shortcuts import render
from rest_framework.serializers import Serializer
from .models import *
from .serializers import *
from rest_framework.views import APIView

class RegisterView(APIView):
    def post(self,request):
        try:
            serializer=UserSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'status':403,
                    'errors':serializers.errors
                }

                )
            serializer.save()
            return Response({'status':200,'message':'An OTP has been sent to your number and email'})
        except Exception as e:
            print(e)  
            return Response({'status':404,'error':'Something went wrong'})  

# Create your views here.
