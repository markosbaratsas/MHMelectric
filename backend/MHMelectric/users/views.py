from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_csv.renderers import CSVRenderer, JSONRenderer

from rest_api.models import (Car_Owner, Car, Charging_point, Charge_program,
Provider, Station, Periodic_bill, Session)
from users.models import API_key
from rest_api.serializers import (CarSerializer, Car_OwnerSerializer,
Periodic_billSerializer, SessionSerializer, StationSerializer,
Charging_pointSerializer, Charge_programSerializer, ProviderSerializer)
from users.serializers import RegistrationSerializer


@api_view(['POST', ])
@renderer_classes([JSONRenderer, CSVRenderer])
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
        return Response(data)

@api_view(['POST', ])
@renderer_classes([JSONRenderer, CSVRenderer])
@permission_classes((IsAuthenticated,))
def delete_token(request):

    if request.method == "POST":
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        return Response(status=status.HTTP_200_OK)

@api_view(['POST', ])
@renderer_classes([JSONRenderer, CSVRenderer])
@permission_classes((IsAuthenticated,))
def admin_create_user(request, username, password):

    # check if user is superuser
    if request.user.is_superuser:
        # if user exists get User object, else create it
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.save()

        if created:
            return Response({'Success': f'User {username} created'}, status=status.HTTP_200_OK)
        else:
            return Response({'Success': f'Password updated for {username}'}, status=status.HTTP_200_OK)

    else:
        return Response({'Failed': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', ])
@renderer_classes([JSONRenderer, CSVRenderer])
@permission_classes((IsAuthenticated,))
def admin_get_user(request, username):

    # check if user is superuser
    if request.user.is_superuser:
        # if user exists get User object, else create it
        try:
            user = User.objects.get(username=username)

            data = {}
            data['username'] = user.username
            data['email'] = user.email
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({'No data'}, status=status.HTTP_402_PAYMENT_REQUIRED)

    else:
        return Response({'Failed': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)

# inherit class ObtainAuthToken () https://github.com/encode/django-rest-framework/blob/master/rest_framework/authtoken/views.py )
# and change just the post method
class ObtainAPIKey(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        api_key = token.key[0:4] + "-" + token.key[4:8] + "-" + token.key[8:12]
        API_key.objects.get_or_create(api_key=api_key, token=token)

        return Response({'api_key': api_key}, status=status.HTTP_200_OK)

@api_view(['POST', ])
@renderer_classes([JSONRenderer, CSVRenderer])
def cli_logout(request):

    if request.method == "POST":
        try:
            api_key = API_key.objects.get(api_key=request.data['api_key'])
            api_key.token.delete() # delete token and API_key object will be automatically deleted
        except (AttributeError, ObjectDoesNotExist):
            pass

        return Response(status=status.HTTP_200_OK)

@api_view(['GET', ])
@renderer_classes([JSONRenderer, CSVRenderer])
def get_token_from_api_key(request):

    if request.method == "GET":
        try:
            api_key = API_key.objects.get(api_key=request.data['api_key'])
            return Response({'token': api_key.token.key}, status=status.HTTP_200_OK)
        except (AttributeError, ObjectDoesNotExist):
            return Response({'Failed': 'API key not found'}, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_user_info(request):

    username = request.user.username
    email = request.user.email

    try:
        car_owner = Car_Owner.objects.get(user=request.user)

    except:
        return Response({
            'username': username,
            'email': email
        }, status=status.HTTP_200_OK)


    car_owner = Car_OwnerSerializer(car_owner).data
    return Response({
        'username': username,
        'email': email,
        'car_owner': car_owner
    }, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_car_info_from_user(request):

    try:
        car_owner = Car_Owner.objects.get(user=request.user)
        cars = Car.objects.filter(owner=car_owner)

        cars = CarSerializer(cars, many=True).data

    except:
        return Response({}, status=status.HTTP_200_OK)


    return Response({
        'cars': cars
    }, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_periodic_bills_of_user(request):

    try:
        car_owner = Car_Owner.objects.get(user=request.user)
        periodic_bills = Periodic_bill.objects.filter(owner=car_owner)

        periodic_bills = Periodic_billSerializer(periodic_bills, many=True).data

    except:
        return Response({
            'periodic_bills': []
        }, status=status.HTTP_200_OK)


    return Response({
        'periodic_bills': periodic_bills
    }, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_sessions_of_periodic_bill(request, periodic_bill_id):

    try:
        periodic_bill = Periodic_bill.objects.get(periodic_bill_id=periodic_bill_id)
        car_owner = Car_Owner.objects.get(user=request.user)
        sessions = Session.objects.filter(periodic_bill=periodic_bill, car_owner=car_owner)

        sessions = SessionSerializer(sessions, many=True).data

        for i in sessions: # maybe the's a better way to do this...

            try: 
                specific_car = Car.objects.get(car_id=i["car"])
                i["car"] = CarSerializer(specific_car).data
            except:
                pass

            try: 
                i["station"] = Station.objects.get(station_id=i["station"]).get_some_info()
            except:
                pass

            try: 
                i["charge_program"] = Charge_program.objects.get(charge_program_id=i["charge_program"]).get_some_info()
            except:
                pass

            try: 
                i["provider"] = Provider.objects.get(provider_id=i["provider"]).get_some_info()
            except:
                pass

    except:
        return Response({
            'sessions': []
        }, status=status.HTTP_200_OK)


    return Response({
        'sessions': sessions
    }, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def pay_periodic_bill(request, periodic_bill_id):

    try:
        car_owner = Car_Owner.objects.get(user=request.user)

        periodic_bill = Periodic_bill.objects.get(periodic_bill_id=periodic_bill_id, owner=car_owner)
        periodic_bill.paid = True
        periodic_bill.save()

    except:
        return Response({
            'status': 'Failed'
        }, status=status.HTTP_200_OK)


    return Response({
        'status': 'Success'
    }, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
@renderer_classes([JSONRenderer, CSVRenderer])
def add_session(request):
    
    serializer = SessionSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        session = serializer.save()
        data['response'] = 'Successfully created a new session.'
        data['session'] = SessionSerializer(session).data
    else:
        data = serializer.errors
    return Response(data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
@renderer_classes([JSONRenderer, CSVRenderer])
def get_stations_from_city(request, city):

    stations = Station.objects.filter(city=city)
    stations = StationSerializer(stations, many=True).data
    return Response({
        'stations': stations
    }, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
@renderer_classes([JSONRenderer, CSVRenderer])
def get_charging_points_from_station(request, station):

    charging_points = Charging_point.objects.filter(station=station)
    charging_points = Charging_pointSerializer(charging_points, many=True).data
    return Response({
        'charging_points': charging_points
    }, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
@renderer_classes([JSONRenderer, CSVRenderer])
def get_charge_programs(request):

    charge_programs = Charge_program.objects.all()
    charge_programs = Charge_programSerializer(charge_programs, many=True).data
    return Response({
        'charge_programs': charge_programs
    }, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
@renderer_classes([JSONRenderer, CSVRenderer])
def get_providers(request):

    providers = Provider.objects.all()
    providers = ProviderSerializer(providers, many=True).data
    return Response({
        'providers': providers
    }, status=status.HTTP_200_OK)
