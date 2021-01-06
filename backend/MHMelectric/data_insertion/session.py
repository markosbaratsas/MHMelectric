# to run the script execute:  python3 manage.py shell < data_insertion/charging_points.py
# or fix it accordingly based on the directory you are

import json
import sys
from rest_api.models import *

path_to_file = "/mnt/c/Users/marak/Downloads/OneDrive_1_1-5-2021/acn_data/caltech_acndata_sessions_12month.json"

s = set()
with open(path_to_file) as json_file:
    data = json.load(json_file)
    # for i in list(data["_items"]):
    for i in list(data["_items"])[:100]:
        Session.objects.create(session_id_given=i["_id"], 
            car=None,
            car_owner=None,
            # charging_point==list(Charging_point.objects.filter(charging_point_id=i["stationID"]))[0]
            periodic_bil=None,
            connection_time=i["connectionTime"], 
            disconnection_time=i["disconnectTime"], 
            done_charging_time=i["doneChargingTime"], 
            kWh_delivered=i["kWhDelivered"], 
            timezone=i["timezone"], 
            user_Wh_per_mile=i["userInputs"][0]["WhPerMile"]  if i["userInputs"]!=None and i["userInputs"][0]["WhPerMile"]!=None else 0, 
            user_kWh_requested=i["userInputs"][0]["kWhRequested"]  if i["userInputs"]!=None and i["userInputs"][0]["kWhRequested"]!=None else 0,
            user_miles_requested=i["userInputs"][0]["milesRequested"]  if i["userInputs"]!=None and i["userInputs"][0]["milesRequested"]!=None else 0,
            user_minutes_available=i["userInputs"][0]["minutesAvailable"]  if i["userInputs"]!=None and i["userInputs"][0]["minutesAvailable"]!=None else 0,
            user_modified_at=i["userInputs"][0]["modifiedAt"]  if i["userInputs"]!=None and i["userInputs"][0]["modifiedAt"]!=None else 0,
            user_payment_required=i["userInputs"][0]["paymentRequired"]  if i["userInputs"]!=None and i["userInputs"][0]["paymentRequired"]!=None else True,
            user_requested_departure=i["userInputs"][0]["requestedDeparture"]  if i["userInputs"]!=None and i["userInputs"][0]["requestedDeparture"]!=None else True)
        s.add(i["userID"])
        # print(i["userID"])
    print(s)