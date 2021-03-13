from rest_api.models import UploadedCSV
import csv
from io import StringIO
import sys
from random import randrange
import datetime
from .models import *
from pytz import timezone

def upload_csv_file(csv_file):
    # print(type(csv_file))
    file = csv_file.read().decode('utf-8')
    csv_data = csv.reader(StringIO(file), delimiter=',')
    
    SessionsInUploadedFile = 0
    SessionsImported = 0
    firstRow = True
    for i in csv_data:
        if(firstRow == False):
            SessionsInUploadedFile += 1
            print(i[0])
            if(len(list(Session.objects.filter(session_id_given=i[0])))==0):
                stationID = randrange(len(list(Station.objects.all())))
                charge_programID = randrange(1, len(list(Charge_program.objects.all())))
                providerID = randrange(1, len(list(Provider.objects.all())))
                car = list(Car.objects.all())[randrange(len(list(Car.objects.all())))]
                if(len(list(Charging_point.objects.filter(station=stationID)))>0):
                    chargingPointID = list(Charging_point.objects.filter(station=stationID))[randrange(len(Charging_point.objects.filter(station=stationID)))]
                    #print(chargingPointID)
                else:
                    chargingPointID = None
                Periodic_bill.objects.get_or_create(owner=car.owner)
                bill = list(Periodic_bill.objects.filter(owner=car.owner))[0]
                Session.objects.create(session_id_given=i[0],
                    car=car.owner,
                    car_owner=None,
                    charging_point=chargingPointID,
                    station=list(Station.objects.filter(station_id=stationID))[0] if (len(list(Station.objects.filter(station_id=stationID)))) else None,
                    periodic_bill=bill,
                    connection_time=datetime.datetime.strptime(i[2], "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')) if i[2]!='null' and i[2]!='' else datetime.datetime.strptime("Sun, 01 Sep 2000 16:56:18 GMT", "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')),
                    disconnection_time=datetime.datetime.strptime(i[3], "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')) if i[3]!='null' and i[3]!='' else datetime.datetime.strptime("Sun, 01 Sep 2000 16:56:18 GMT", "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')),
                    done_charging_time=datetime.datetime.strptime(i[4], "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')) if i[4]!='null' and i[4]!='' else datetime.datetime.strptime("Sun, 01 Sep 2000 16:56:18 GMT", "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')),
                    kWh_delivered=i[5],
                    timezone=i[10], 
                    user_Wh_per_mile=i[12]  if i[12]!='null' else 0, 
                    user_kWh_requested=i[13]  if i[13]!='null' else 0,
                    user_miles_requested=i[14]  if i[14]!='null' else 0,
                    user_minutes_available=i[15]  if i[15]!='null' else 0,
                    user_modified_at=datetime.datetime.strptime(i[16], "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')) if i[16]!='null' and i[16]!='' else datetime.datetime.strptime("Sun, 01 Sep 2000 16:56:18 GMT", "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')),
                    user_payment_required=i[17]  if i[17]!='null' else True,
                    user_requested_departure=datetime.datetime.strptime(i[18], "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')) if i[18]!='null' and i[18]!='' else datetime.datetime.strptime("Sun, 01 Sep 2000 16:56:18 GMT", "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')),
                    charge_program=list(Charge_program.objects.filter(charge_program_id=charge_programID))[0],
                    provider=list(Provider.objects.filter(provider_id=providerID))[0])
                SessionsImported += 1

        firstRow = False
    TotalSessionsInDatabase = len(list(Session.objects.all()))

    for i in range(1, len(list(Periodic_bill.objects.all()))+1):
        bill = list(Periodic_bill.objects.filter(periodic_bill_id=i))[0]
        total = 0
        for session in list(Session.objects.filter(periodic_bill=bill)):
            total += session.charge_program.price
        bill.total = total
        bill.discount = bill.owner.bonus_points / 10
        bill.save()

    return {
        'SessionsInUploadedFile': SessionsInUploadedFile,
        'SessionsImported': SessionsImported,
        'TotalSessionsInDatabase': TotalSessionsInDatabase
        }