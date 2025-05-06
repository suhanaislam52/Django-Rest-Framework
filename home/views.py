from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *
from .serializers import StudentSerializer  # Import the serializer specifically
from .serializers import BookSerializer



@api_view(['GET'])
def home(request):
    student_objs=Student.objects.all()
    serializer=StudentSerializer(student_objs, many=True)
    return Response({'status': 200, 'payload': serializer.data})
# Create your views here.


@api_view(['GET','POST'])
def post_student(request):
    data=request.data
    serializer=StudentSerializer(data=request.data)

    if request.data['age'] < 18:
        return Response({'status':403, 'message':'age must be > 18'})

    if not serializer.is_valid():
        print(serializer.errors)
        return Response({'status': 403 ,'errors':serializer.errors, 'messsage':'Something went wrong'})
    serializer.save()
    return Response({'status':200,'payload':serializer.data, 'message': 'you data has been saved'})

@api_view(['PUT'])
def update_student(request):

    try: 
        student_obj=Student.objects.get(id=id)
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
    
@api_view(['DELETE'])
def delete_student(request , id):
    try:
        id=request.GET.get('id')
        student_obj=Student.objects.get(id=id)
        student_obj.delete()
        return Response({'status':200,'message':'deleted'})
    except Exception as e:
        print(e)
        return Response({'status':403,'message':'invalid id'})
    
@api_view(['GET'])
def get_book(request):
    book_objs=Book.objects.all()
    serializer=BookSerializer(book_objs,many=True)
    return Response({'status':200,'payload':serializer.data})