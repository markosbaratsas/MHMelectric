from django.http import HttpResponse
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections
from django.db.utils import OperationalError
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework_csv.renderers import CSVRenderer, JSONRenderer
from rest_framework.throttling import UserRateThrottle
import pytz
import traceback
import csv
from datetime import datetime
import time
from pytz import timezone

from rest_api.models import Car, Charging_point, Session, UploadedCSV, Operator, Provider, Station
from rest_api.serializers import CarSerializer, UploadedCSVSerializer
from rest_api.scripts import upload_csv_file

def index(request):
    return HttpResponse("<h1>We made it so far!</h1>")

# we could do something like this for the other requests
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def get_first_car(request):
    try:
        cars = Car.objects.all()
    except:      
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    car = list(cars)[0]
    if request.method == "GET":
        serializer = CarSerializer(car)
        return Response(serializer.data)


@api_view(['GET', ])
@renderer_classes([JSONRenderer, CSVRenderer])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def sessions_per_point(request, pointID, date_from, date_to):
    try:
        charging_point = Charging_point.objects.get(charging_point_id_given=pointID)
    except:
        return Response({'Failed': f'There is no charging point with pointID {pointID}'}, status=status.HTTP_400_BAD_REQUEST)

    data = []
    Point = charging_point.charging_point_id_given
    if charging_point.operator == None:
        PointOperator = 'None'
    else:
        PointOperator = charging_point.operator.title
    RequestTimestamp = datetime.now(pytz.timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S")
    PeriodFrom = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00"
    PeriodTo = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 23:59:59"

    sessions = list(Session.objects.filter(
        charging_point=charging_point,
        # connection_time__range=[data['PeriodFrom'][:10], data['PeriodTo'][:10]]
        connection_time__range=[datetime.strptime(PeriodFrom, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone('UTC')),
                    datetime.strptime(PeriodTo, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone('UTC'))]
    ))
    sessions.sort(key=lambda x: x.connection_time)

    NumberOfChargingSessions = int(len(sessions))
    if len(sessions)==0:
        return Response({'Failed': f'There is no session in point {pointID}'}, status=status.HTTP_402_PAYMENT_REQUIRED)
    for i in range(len(sessions)):
        try:
            car_type = Car.objects.get(car_id=sessions[i].car).car_type
        except:
            car_type = ''
        data.append({
            'Point': Point,
            'PointOperator': PointOperator,
            'RequestTimestamp': RequestTimestamp,
            'PeriodFrom': PeriodFrom,
            'PeriodTo': PeriodTo,
            'NumberOfChargingSessions': NumberOfChargingSessions,

            'SessionIndex': int(i + 1),
            'SessionID': sessions[i].session_id_given,
            'StartedOn': sessions[i].connection_time,
            'FinishedOn': sessions[i].disconnection_time,
            'Protocol': sessions[i].protocol,
            'EnergyDelivered': float(sessions[i].kWh_delivered),
            'Payment': sessions[i].user_payment_method,
            'VehicleType': car_type
        })

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@renderer_classes([JSONRenderer, CSVRenderer])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def sessions_per_station(request, stationID, date_from, date_to):
    try:
        station = Station.objects.get(station_id_given=stationID)
    except:
        return Response({'Failed': f'There is no station with stationID {stationID}'}, status=status.HTTP_400_BAD_REQUEST)
    data = []
    StationID = station.station_id_given
    if station.operator == None:
        Operator = 'None'
    else:
        Operator = station.operator.title
    RequestTimestamp = datetime.now(pytz.timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S")
    PeriodFrom = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00"
    PeriodTo = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 23:59:59"

    sessions = list(Session.objects.filter(
        station=station,
        connection_time__range=[datetime.strptime(PeriodFrom, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone('UTC')),
                    datetime.strptime(PeriodTo, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone('UTC'))]
    ))
    sessions.sort(key=lambda x: x.connection_time)

    totalEnergyDelivered = 0.0
    activePoints = {}
    if len(sessions)==0:
        return Response({'Failed': f'There is no session in station {stationID}'}, status=status.HTTP_402_PAYMENT_REQUIRED)
    for i in range(len(sessions)):
        energyDelivered = float(sessions[i].kWh_delivered)
        totalEnergyDelivered += energyDelivered
        charging_point = sessions[i].charging_point.charging_point_id_given
        if charging_point in activePoints.keys():
            activePoints[charging_point][0] += 1
            activePoints[charging_point][1] += energyDelivered
        else:
            activePoints[charging_point] = [1, energyDelivered]
    NumberOfChargingSessions = int(len(sessions))
    NumberOfActivePoints = len(activePoints)
    for i in activePoints.keys():
        data.append({
            'StationID': StationID,
            'Operator': Operator,
            'RequestTimestamp': RequestTimestamp,
            'PeriodFrom': PeriodFrom,
            'PeriodTo': PeriodTo,
            'totalEnergyDelivered': totalEnergyDelivered,
            'NumberOfChargingSessions': NumberOfChargingSessions,
            'NumberOfActivePoints': NumberOfActivePoints,

            'PointID': i,
            'PointSessions': activePoints[i][0],
            'EnergyDelivered': activePoints[i][1],
        })

    return Response(data, status=status.HTTP_200_OK)
    

@api_view(['GET', ])
@renderer_classes([JSONRenderer, CSVRenderer])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def sessions_per_ev(request, vehicleID, date_from, date_to):
    try:
        car = Car.objects.get(car_id_given=vehicleID)
    except:
        return Response({'Failed': f'There is no vehicle with vehicleID {vehicleID}'}, status=status.HTTP_400_BAD_REQUEST)
    data = []
    VehicleID = car.car_id_given
    RequestTimestamp = datetime.now(pytz.timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S")
    PeriodFrom = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00"
    PeriodTo = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 23:59:59"

    sessions = list(Session.objects.filter(
        car=car,
        connection_time__range=[datetime.strptime(PeriodFrom, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone('UTC')),
                    datetime.strptime(PeriodTo, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone('UTC'))]
    ))
    sessions.sort(key=lambda x: x.connection_time)

    TotalEnergyConsumed = 0
    NumberOfVisitedPoints = 0
    visited_points = set()
    NumberOfVehicleChargingSessions = int(len(sessions))
    
    if len(sessions)==0:
        return Response({'Failed': f'There is no session of EV {vehicleID}'}, status=status.HTTP_402_PAYMENT_REQUIRED)
    for i in range(len(sessions)):
        if sessions[i].charging_point != None:
            visited_points.add(sessions[i].charging_point)
        TotalEnergyConsumed += float(sessions[i].kWh_delivered)
        TotalEnergyConsumed = round(TotalEnergyConsumed, 3) 
    NumberOfVisitedPoints = int(len(visited_points))

    for i in range(len(sessions)):
        try:
            session_provider = sessions[i].charging_point.Operator.title
        except:
            session_provider = ''
        try:
            session_program = sessions[i].sessions[i].charge_program.description
            session_price = sessions[i].charge_program.price
            session_cost = round(float(sessions[i].kWh_delivered)*sessions[i].charge_program.price,2)
        except:
            session_program = ''
            session_price = "unknown"
            session_cost = "unknown"
        data.append({
            'VehicleID': VehicleID,
            'PeriodFrom': PeriodFrom,
            'PeriodTo': PeriodTo,
            'TotalEnergyConsumed': TotalEnergyConsumed,
            'NumberOfVisitedPoints': NumberOfVisitedPoints,
            'NumberOfVehicleChargingSessions': NumberOfVehicleChargingSessions,

            'SessionID': sessions[i].session_id_given,
            'EnergyProvider': session_provider,
            'StartedOn': sessions[i].connection_time,
            'FinishedOn': sessions[i].disconnection_time,
            'EnergyDelivered': float(sessions[i].kWh_delivered),
            'PricePolicyRef': session_program,
            'CostPerkWh':   session_price,
            'SessionCost': session_cost
        })

    return Response(data, status=status.HTTP_200_OK)
    

@api_view(['GET', ])
@renderer_classes([JSONRenderer, CSVRenderer])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def sessions_per_provider(request, providerID, date_from, date_to):
    try:
        provider = Provider.objects.get(provider_id_given=providerID)
    except:
        return Response({'Failed': f'There is no provider with providerID {providerID}'}, status=status.HTTP_400_BAD_REQUEST)
    data = []
    ProviderID = provider.provider_id_given
    ProviderName = provider.title
    PeriodFrom = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00"
    PeriodTo = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 23:59:59"

    sessions = list(Session.objects.filter(
        provider=provider,
        connection_time__range=[datetime.strptime(PeriodFrom, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone('UTC')),
                    datetime.strptime(PeriodTo, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone('UTC'))]
    ))
    sessions.sort(key=lambda x: x.connection_time)

    if len(sessions)==0:
        return Response({'Failed': f'There is no session of provider {providerID}'}, status=status.HTTP_402_PAYMENT_REQUIRED)
    for i in range(len(sessions)):
        try:
            stationID = Station.objects.get(station_id=sessions[i].station).station_id_given
        except:
            stationID = ''
        try:
            vehicleID = Car.objects.get(car_id=sessions[i].car).car_id_given
        except:
            vehicleID = ''
        try:
            session_program = sessions[i].sessions[i].charge_program.description
            session_price = sessions[i].charge_program.price
            session_cost = round(float(sessions[i].kWh_delivered)*sessions[i].charge_program.price,2)
        except:
            session_program = ''
            session_price = "unknown"
            session_cost = "unknown"
        data.append({
            'ProviderID': ProviderID,
            'ProviderName': ProviderName,
            'PeriodFrom': PeriodFrom,
            'PeriodTo': PeriodTo,

            'StationID': stationID,
            'SessionID': sessions[i].session_id_given,
            'VehicleID': vehicleID,
            'StartedOn': sessions[i].connection_time,
            'FinishedOn': sessions[i].disconnection_time,
            'Protocol': sessions[i].protocol,
            'EnergyDelivered': sessions[i].kWh_delivered,
            'PricePolicyRef': session_program,
            'CostPerkWh':   session_price,
            'SessionCost': session_cost
        })

    return Response(data, status=status.HTTP_200_OK)
    

@renderer_classes([JSONRenderer, CSVRenderer])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
class SessionsUpload(APIView):
    parser_classes = (MultiPartParser, FileUploadParser,)
    serializer = UploadedCSVSerializer

    def post(self, request, format='csv'):
        if request.user.is_superuser:
            upload = self.serializer(data=request.FILES)
            if upload.is_valid() and self.serializer.check_extension(request.FILES['file'].name):
                file = UploadedCSV.objects.create(csv_file=upload.validated_data['file'], uploaded_from=request.user)

                data = upload_csv_file(file.csv_file)
                return Response(data, status.HTTP_200_OK)
            else:
                data = upload.errors
                return Response(data, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Failed': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', ])
@renderer_classes([JSONRenderer, CSVRenderer])
def check_db_connection(request):
    db_conn = connections['default']
    try:
        db_conn.cursor()
    except OperationalError:
        return Response({'status': 'failed'}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'OK'}, status=status.HTTP_200_OK)


@api_view(['POST', ])
@renderer_classes([JSONRenderer, CSVRenderer])
def resetsessions(request):
    try:
        Session.objects.all().delete()
    except:
        return Response({'status': 'failed'}, status=status.HTTP_200_OK)
        pass

    user, _ = User.objects.get_or_create(username="admin",
                    is_superuser=True)
    user.set_password("petrol4ever")
    user.save()
    return Response({'status': 'OK'}, status=status.HTTP_200_OK)
