from django.urls import path

import rest_api.views as views

urlpatterns = [
    path('', views.index),
    path('get_first_car/', views.get_first_car, name="get_first_car"),
]
