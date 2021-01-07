from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from rest_api.models import Car
from rest_api.serializers import CarSerializer
from users.serializers import RegistrationSerializer

def index(request):
    return HttpResponse("<h1>We made it so far!</h1>")

# we could do something like this for the other requests
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_first_car(request):
    try:
        cars = Car.objects.all()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    car = list(cars)[0]
    if request.method == "GET":
        serializer = CarSerializer(car)
        return Response(serializer.data)


@api_view(['POST', ])
def register_user(request):
    
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Successfully created a new user.'
            data['email'] = user.email
            data['username'] = user.username
            data['token'] = Token.objects.get(user=user).key
        else: 
            data = serializer.errors
            print(data)
        return Response(data)

@api_view(['POST', ])
def delete_token(request):
    
    if request.method == "POST":
        try:
            print(request.body)
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        return Response(status=status.HTTP_200_OK)
