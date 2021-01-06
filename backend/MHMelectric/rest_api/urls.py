from django.contrib import admin
from django.urls import path, include
import rest_api.views as views

urlpatterns = [
    path('', views.index),
    path('get_first_car/', views.get_first_car, name="get_first_car"),
    path('register', views.register_user, name="register_user"),    
]