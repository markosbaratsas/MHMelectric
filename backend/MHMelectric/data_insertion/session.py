# to run the script execute:  python3 manage.py shell < data_insertion/session.py
# or fix it accordingly based on the directory you are
# make sure you first add some charging points to the database

import json
import sys
from random import randrange
import datetime
from rest_api.models import *
from pytz import timezone

path_to_file = "/mnt/c/Users/marak/Downloads/OneDrive_1_05-01-2021/acn_data/caltech_acndata_sessions_12month.json"

s = set()
with open(path_to_file) as json_file:
    data = json.load(json_file)
    # for i in list(data["_items"]):
    for i in list(data["_items"])[:100]:
        if(len(list(Session.objects.filter(session_id_given=i["_id"])))==0):
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
            Session.objects.get_or_create(session_id_given=i["_id"],
                car=car,
                car_owner=car.owner,
                charging_point=chargingPointID,
                station=list(Station.objects.filter(station_id=stationID))[0] if (len(list(Station.objects.filter(station_id=stationID)))) else None,
                periodic_bill=bill,
                connection_time=datetime.datetime.strptime(i["connectionTime"], "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')) if i["connectionTime"]!=None and i["connectionTime"]!='' else datetime.datetime.strptime("Sun, 01 Sep 2000 16:56:18 GMT", "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')),
                disconnection_time=datetime.datetime.strptime(i["disconnectTime"], "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')) if i["disconnectTime"]!=None and i["disconnectTime"]!='' else datetime.datetime.strptime("Sun, 01 Sep 2000 16:56:18 GMT", "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')),
                done_charging_time=datetime.datetime.strptime(i["doneChargingTime"], "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')) if i["doneChargingTime"]!=None and i["doneChargingTime"]!='' else datetime.datetime.strptime("Sun, 01 Sep 2000 16:56:18 GMT", "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')),
                kWh_delivered=i["kWhDelivered"],
                timezone=i["timezone"], 
                user_Wh_per_mile=i["userInputs"][0]["WhPerMile"]  if i["userInputs"]!=None and i["userInputs"][0]["WhPerMile"]!=None else 0, 
                user_kWh_requested=i["userInputs"][0]["kWhRequested"]  if i["userInputs"]!=None and i["userInputs"][0]["kWhRequested"]!=None else 0,
                user_miles_requested=i["userInputs"][0]["milesRequested"]  if i["userInputs"]!=None and i["userInputs"][0]["milesRequested"]!=None else 0,
                user_minutes_available=i["userInputs"][0]["minutesAvailable"]  if i["userInputs"]!=None and i["userInputs"][0]["minutesAvailable"]!=None else 0,
                user_modified_at=datetime.datetime.strptime(i["userInputs"][0]["modifiedAt"], "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')) if i["userInputs"]!=None and i["userInputs"][0]["modifiedAt"]!=None else datetime.datetime.strptime("Sun, 01 Sep 2000 16:56:18 GMT", "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')),
                user_payment_required=i["userInputs"][0]["paymentRequired"]  if i["userInputs"]!=None and i["userInputs"][0]["paymentRequired"]!=None else True,
                user_requested_departure=datetime.datetime.strptime(i["userInputs"][0]["requestedDeparture"], "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')) if i["userInputs"]!=None and i["userInputs"][0]["requestedDeparture"]!=None else datetime.datetime.strptime("Sun, 01 Sep 2000 16:56:18 GMT", "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')),
                charge_program=list(Charge_program.objects.filter(charge_program_id=charge_programID))[0],
                provider=list(Provider.objects.filter(provider_id=providerID))[0])
            s.add(i["userID"])
            # print(i["userID"])
for i in range(1, len(list(Periodic_bill.objects.all()))+1):
    bill = list(Periodic_bill.objects.filter(periodic_bill_id=i))[0]
    total = 0
    for session in list(Session.objects.filter(periodic_bill=bill)):
        total += session.charge_program.price
    bill.total = total
    bill.discount = bill.owner.bonus_points / 10
    bill.save()
    