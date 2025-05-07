from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','password','phone']

    def create(self,validated_data):
        user=User.objects.create(username=validated_data['username'])
        user.set_password=(validated_data['password'])
        user.save()
        return user