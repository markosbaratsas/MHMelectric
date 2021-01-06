from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

import rest_api.views as views

urlpatterns = [
    path('', views.index),
    path('get_first_car/', views.get_first_car, name="get_first_car"),
    path('register', views.register_user, name="register_user"),    
    path('login', obtain_auth_token, name="obtain_auth_token"),    
]