from django.contrib import admin
from django.urls import path,include

from .views import *
from . import views

urlpatterns = [
   path('',home),
   path('student/', views.post_student, name='post_student'),
   path('update-student/<id>/',update_student),
]
