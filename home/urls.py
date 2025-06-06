from django.contrib import admin
from django.urls import path,include

from .views import *
from . import views

urlpatterns = [
   #path('',home),
   #path('student/', views.post_student, name='post_student'),
   #path('update-student/<id>/',update_student),
   path('get-book/',get_book),
   path('student/',StudentAPI.as_view()),
   path('register/',RegisterUser.as_view()),
   path('generic-student/',StudentGeneric.as_view()),
   path('generic-student/<id>',StudentGeneric1.as_view()),
   path('excel/',ExportImportExcel.as_view())
]
