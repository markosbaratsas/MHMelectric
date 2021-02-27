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

    path('get_user_info/', views.get_user_info, name="get_user_info"),
]
