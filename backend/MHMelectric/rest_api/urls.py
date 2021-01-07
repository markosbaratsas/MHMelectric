from django.urls import path

import rest_api.views as views

urlpatterns = [
    path('', views.index),
    path('get_first_car/', views.get_first_car, name="get_first_car"),
    path('admin/system/sessionsupd', views.SessionsUpload.as_view(), name="sessions_upload"),
    path('admin/healthcheck/', views.check_db_connection, name="check_db_connection"),
    path('admin/resetsessions', views.resetsessions, name="resetsessions"),
]
