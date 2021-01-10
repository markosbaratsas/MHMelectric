from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections
from django.db.utils import OperationalError
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
import pytz
import traceback
from datetime import datetime
import time

from rest_api.models import Car, Charging_point, Session, UploadedCSV
from rest_api.serializers import CarSerializer, UploadedCSVSerializer
from rest_api.scripts import upload_csv_file

def index(request):
    return HttpResponse("<h1>We made it so far!</h1>")

# we could do something like this for the other requests
@api_view(['GET', ])
#@permission_classes((IsAuthenticated,))
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
#@permission_classes((IsAuthenticated,))
def sessions_per_point(request, pointID, date_from, date_to):
    data = {}

    try:
        charging_point = Charging_point.objects.get(charging_point_id_given=pointID)
    except:
        return Response({'Failed': f'There is no charging point with pointID {pointID}'}, status=status.HTTP_400_BAD_REQUEST)

    data['Point'] = charging_point.charging_point_id_given
    data['PointOperator'] = charging_point.operator.title
    data['RequestTimestamp'] = datetime.now(pytz.timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S")
    data['PeriodFrom'] = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00"
    data['PeriodTo'] = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 23:59:59"

    sessions = list(Session.objects.filter(
        charging_point=charging_point,
        connection_time__range=[data['PeriodFrom'][:10], data['PeriodTo'][:10]]
    ))
    sessions.sort(key=lambda x: x.connection_time)

    data['NumberOfChargingSessions'] = int(len(sessions))
    data['ChargingSessionsList'] = []
    for i in range(len(sessions)):
        try:
            car_type = Car.objects.get(car_id=sessions[i].car).car_type
        except:
            car_type = ''
        item = {
            'SessionIndex': int(i + 1),
            'SessionID': sessions[i].session_id_given,
            'StartedOn': sessions[i].connection_time,
            'FinishedOn': sessions[i].disconnection_time,
            'Protocol': sessions[i].protocol,
            'EnergyDelivered': float(sessions[i].kWh_delivered),
            'Payment': sessions[i].user_payment_method,
            'VehicleType': car_type
        }

        data['ChargingSessionsList'].append(item)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET', ])
#@permission_classes((IsAuthenticated,))
def sessions_per_ev(request, vehicleID, date_from, date_to):
    data = {}

    try:
        car = Car.objects.get(car_id_given=vehicleID)
    except:
        return Response({'Failed': f'There is no charging point with vehicleID {vehicleID}'}, status=status.HTTP_400_BAD_REQUEST)

    data['VehicleID'] = car.car_id_given
    data['RequestTimestamp'] = datetime.now(pytz.timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S")
    data['PeriodFrom'] = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00"
    data['PeriodTo'] = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 23:59:59"

    sessions = list(Session.objects.filter(
        #car=car,
        #connection_time__range=[data['PeriodFrom'][:10], data['PeriodTo'][:10]]
    ))
    sessions.sort(key=lambda x: x.connection_time)

    data['TotalEnergyConsumed'] = 0
    data['NumberOfVisitedPoints'] = 0
    visited_points = set()
    data['NumberOfVehicleChargingSessions'] = int(len(sessions))
    data['ChargingSessionsList'] = []
    
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
        item = {
            'SessionIndex': int(i + 1),
            'SessionID': sessions[i].session_id_given,
            'EnergyProvider': session_provider,
            'StartedOn': sessions[i].connection_time,
            'FinishedOn': sessions[i].disconnection_time,
            'EnergyDelivered': float(sessions[i].kWh_delivered),
            'PricePolicyRef': session_program,
            'CostPerkWh':   session_price,
            'SessionCost': session_cost
        }
        if sessions[i].charging_point != None:
            visited_points.add(sessions[i].charging_point)
        data['TotalEnergyConsumed'] += float(sessions[i].kWh_delivered)
        data['TotalEnergyConsumed'] = round(data['TotalEnergyConsumed'], 3)
        data['ChargingSessionsList'].append(item)
    data['NumberOfVisitedPoints'] = int(len(visited_points))
    return Response(data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class SessionsUpload(APIView):
    parser_classes = (MultiPartParser, FileUploadParser,)
    serializer = UploadedCSVSerializer

    def post(self, request, format='csv'):
        if request.user.is_superuser:
            upload = self.serializer(data=request.FILES)
            if upload.is_valid() and self.serializer.check_extension(request.FILES['file'].name):
                file = UploadedCSV.objects.create(csv_file=upload.validated_data['file'], uploaded_from=request.user)

                data = upload_csv_file(file)
                return Response(data, status.HTTP_200_OK)
            else:
                data = upload.errors
                return Response(data, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Failed': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', ])
def check_db_connection(request):
    db_conn = connections['default']
    try:
        db_conn.cursor()
    except OperationalError:
        return Response({'status': 'failed'}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'OK'}, status=status.HTTP_200_OK)


@api_view(['POST', ])
def resetsessions(request):
    try:
        Session.objects.all().delete()
    except:
        return Response({'status': 'failed'}, status=status.HTTP_200_OK)
        pass

    user, _ = User.objects.get_or_create(username="admin")
    user.set_password("petrol4ever")
    user.save()
    return Response({'status': 'OK'}, status=status.HTTP_200_OK)
