from rest_framework import serializers
from .models import *

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model=Student
        #field =['name','age']
        #fields= '__all__' 
        exclude= ['id' ,]