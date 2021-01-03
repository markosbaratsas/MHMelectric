from django.contrib import admin
from django.urls import path, include
import rest_api.views as views

urlpatterns = [
    path('', views.index),
]