from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

import users.views as views

urlpatterns = [
    path('register', views.register_user, name="register_user"),
    path('login', obtain_auth_token, name="obtain_auth_token"),
    path('logout', views.delete_token, name="delete_token"),
    path(r'admin/usermod/<username>/<password>', views.admin_create_user, 
                                                        name="admin_create_user"),
    path(r'admin/users/<username>/', views.admin_get_user, 
                                                        name="admin_get_user"),

    # CLI
    path('cli_login', views.ObtainAPIKey.as_view(), name="ObtainAPIKey"),
    path('cli_logout', views.cli_logout, name="cli_logout"),
    path('get_token_from_api_key', views.get_token_from_api_key, name="get_token_from_api_key"),

    # Frontend
    path('get_user_info/', views.get_user_info, name="get_user_info"),
    path('get_car_info_from_user/', views.get_car_info_from_user, name="get_car_info_from_user"),
    path('get_periodic_bills_of_user/', views.get_periodic_bills_of_user, name="get_periodic_bills_of_user"),
    path(r'get_sessions_of_periodic_bill/<periodic_bill_id>/', views.get_sessions_of_periodic_bill, name="get_sessions_of_periodic_bill"),
    path(r'pay_periodic_bill/<periodic_bill_id>/', views.pay_periodic_bill, name="pay_periodic_bill"),
    path('add_session', views.add_session, name="add_session"),
    path(r'get_stations_from_city/<city>/', views.get_stations_from_city, name="get_stations_from_city"),
    path(r'get_charging_points_from_station/<station>/', views.get_charging_points_from_station, name="get_charging_points_from_station"),
    path('get_charge_programs/', views.get_charge_programs, name="get_charge_programs"),
    path('get_providers/', views.get_providers, name="get_providers"),
    path('add_car', views.add_car, name="add_car"),
]
