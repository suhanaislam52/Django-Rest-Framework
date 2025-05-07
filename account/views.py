from django.shortcuts import render
from rest_framework.serializers import Serializer
from .models import *
from .serializers import *
from rest_framework.views import APIView
from .helpers import *

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

class VerifyOtp(APIView):
    def post(self,request):
        try:
            data=request.data
            user_obj=User.objects.get(phone=data.get('phone'))
            otp=data.get('otp')

            if user_obj.otp==otp:
                user_obj.is_phone_verified=True
                user_obj.save()
                return Response({'status':200,'message':'Your OTP was verified'})
            return Response({'status':403,'message:':'Your OTP was wrong'})
        except Exception as e:
            print(e)
        return Response({'status':403,'message':'Something went wrong'})
    def patch(self,request):
        try:
            data=request.data
            user_obj=User.objects.filter(phone=data.get('phone'))
            if not User.objects.filter(phone=data.get('phone')).exists():
                return Response({'status':403,'message':'No user found'})
            
            status, time=send_otp_to_mobile(data.get('phone'),user_obj[0])
            if status:
                return Response({'status':403,'message':'new otp sent'})
            return Response({'status':404,'error':'try after few seconds'})
        
        except Exception as e:
            print(e)