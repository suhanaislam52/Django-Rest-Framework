from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *
from .serializers import StudentSerializer  # Import the serializer specifically
from .serializers import BookSerializer
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


#@api_view(['GET'])
#def home(request):
 #   student_objs=Student.objects.all()
 #   serializer=StudentSerializer(student_objs, many=True)
 #   return Response({'status': 200, 'payload': serializer.data})
# Create your views here.


#@api_view(['GET','POST'])
#def post_student(request):
 #   data=request.data
  #  serializer=StudentSerializer(data=request.data)

   # if request.data['age'] < 18:
   #     return Response({'status':403, 'message':'age must be > 18'})

  #  if not serializer.is_valid():
  #      print(serializer.errors)
  #      return Response({'status': 403 ,'errors':serializer.errors, 'messsage':'Something went wrong'})
  #  serializer.save()
  #  return Response({'status':200,'payload':serializer.data, 'message': 'you data has been saved'})

#@api_view(['PUT'])
#def update_student(request):

 #   try: 
  #      student_obj=Student.objects.get(id=id)
  #      serializer=StudentSerializer(student_obj,data=request.data,partial=True)
  #      if not serializer.is_valid():
  #          print(serializer.errors)
  #          return Response({'status':403,'errors':serializer.errors,'message':"Something went wrong"})
    
  #      serializer.save()
  #      return Response({'status':200,'payload':serializer.data, 'message': 'you data has been saved'})


   #     serializer=StudentSerializer(data=request.data)
  #      if not serializer.is_valid():
  #          print(serializer.errors)
  #          return Response({'status':403,'errors':serializer.errors,'message':"Something went wrong"})
    
  #  except Exception as e:
  #      return Response({'status':403,'message':'invalid id'})
    
#@api_view(['DELETE'])
#def delete_student(request , id):
 #   try:
 #       id=request.GET.get('id')
 #       student_obj=Student.objects.get(id=id)
 #       student_obj.delete()
 #       return Response({'status':200,'message':'deleted'})
 #   except Exception as e:
 #       print(e)
 #       return Response({'status':403,'message':'invalid id'})
    
@api_view(['GET'])
def get_book(request):
    book_objs=Book.objects.all()
    serializer=BookSerializer(book_objs,many=True)
    return Response({'status':200,'payload':serializer.data})

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class StudentAPI(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]


    def get(self,request):
        student_objs=Student.objects.all()
        serializer=StudentSerializer(student_objs, many=True)
        return Response({'status': 200, 'payload': serializer.data})

    def post(self,request):
        data=request.data
        serializer=StudentSerializer(data=request.data)

        if request.data['age'] < 18:
          return Response({'status':403, 'message':'age must be > 18'})

        if not serializer.is_valid():
          print(serializer.errors)
          return Response({'status': 403 ,'errors':serializer.errors, 'messsage':'Something went wrong'})
        serializer.save()
        return Response({'status':200,'payload':serializer.data, 'message': 'you data has been saved'})

    def put(self,request):
        pass

    def patch(self,request):
        try: 
            student_obj=Student.objects.get(id=request.data['id'])
            serializer=StudentSerializer(student_obj,data=request.data,partial=True)
            if not serializer.is_valid():
              print(serializer.errors)
              return Response({'status':403,'errors':serializer.errors,'message':"Something went wrong"})
    
            serializer.save()
            return Response({'status':200,'payload':serializer.data, 'message': 'you data has been saved'})


            serializer=StudentSerializer(data=request.data)
            if not serializer.is_valid():
              print(serializer.errors)
              return Response({'status':403,'errors':serializer.errors,'message':"Something went wrong"})
    
        except Exception as e:
         return Response({'status':403,'message':'invalid id'})

    def delete(self,request):   
        def delete_student(request , id):
          try:
           id=request.GET.get('id')
           student_obj=Student.objects.get(id=id)
           student_obj.delete()
           return Response({'status':200,'message':'deleted'})
          except Exception as e:
           print(e)
           return Response({'status':403,'message':'invalid id'})
     
from rest_framework_simplejwt.tokens import RefreshToken
class RegisterUser(APIView):
   def post(self,request):
      serializer=UserSerializer(data=request.data)

      if not serializer.is_valid():
         return Response({'status':403, 'errors':serializer.errors,'message':'something went wrong'})
      serializer.save()

      user=User.objects.get(username=serializer.data['username'])
      refresh=RefreshToken.for_user(user)
      return Response({'status':200,'payload':serializer.data,'refresh':str(refresh),'access':str(refresh.access_token),'message':'your data has been saved'})
   

from rest_framework import generics

class StudentGeneric(generics.ListAPIView,generics.CreateAPIView):
   queryset=Student.objects.all()
   serializer_class=StudentSerializer

class StudentGeneric1(generics.UpdateAPIView,generics.DestroyAPIView):
   queryset=Student.objects.all()
   serializer_class=StudentSerializer
   lookup_field='id'

import pandas as pd 
from django.conf import Settings
import uuid
class ExportImportExcel(APIView):
   def get(self,request):
      student_objs=Student.objects.all()
      serializer=StudentSerializer(student_objs,many=True)
      df=pd.DataFrame(serializer.data)
      print(df)

      df.to_csv(f"public/static/excel/{uuid.uuid4()}.csv",encoding="UTF-8",ondex=False)

      return Response({'status':200})
   
   def post(self, request):
    exceled_upload_obj = ExcelFileUpload.objects.create(excel_file_upload=request.FILES['files'])
    df = pd.read_csv(f"{settings.BASE_DIR}/public/static/{exceled_upload_obj.excel_file_upload}")
    
    for student in df.values.tolist():
        Student.objects.create(
            name=student[1],
            age=student[3]
        )
        print(student)
        
    return Response({'status': 200})

