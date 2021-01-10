from django.urls import path

import rest_api.views as views

urlpatterns = [
    path('', views.index),
    path('get_first_car/', views.get_first_car, name="get_first_car"),
    path(r'SessionsPerPoint/<pointID>/<date_from>/<date_to>/', views.sessions_per_point, name="sessions_per_point"),
    path(r'SessionsPerStation/<stationID>/<date_from>/<date_to>/', views.sessions_per_station, name='sessions_per_station'),
    path(r'SessionsPerEV/<vehicleID>/<date_from>/<date_to>/', views.sessions_per_ev, name='sessions_per_ev'),
    path(r'SessionsPerProvider/<providerID>/<date_from>/<date_to>/', views.sessions_per_provider, name='sessions_per_provider'),

    # admin views
    path('admin/system/sessionsupd', views.SessionsUpload.as_view(), name="sessions_upload"),
    path('admin/healthcheck/', views.check_db_connection, name="check_db_connection"),
    path('admin/resetsessions', views.resetsessions, name="resetsessions"),
]
