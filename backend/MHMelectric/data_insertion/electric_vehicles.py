# to run the script execute:  python3 manage.py shell < data_insertion/electric_vehicles.py
# or fix it accordingly based on the directory you are

import json
import sys
from rest_api.models import *
from MHMelectric.settings import BASE_DIR
from random import randrange


with open(str(str(BASE_DIR) + "/data_insertion/file_paths.json")) as paths:
    path_to_file = json.loads(paths.read())["electric_vehicles"]

# path_to_file = "/mnt/c/Users/markg/Downloads/OneDrive_1_05-01-2021/electric_vehicles_data.json"

with open(path_to_file) as json_file:
    data = json.load(json_file)
    for i in list(data["data"]):
        if(len(list(Car.objects.filter(car_id_given=i["id"])))==0):
            ownerID = randrange(1, len(list(Car_Owner.objects.all())))
            Car.objects.get_or_create(car_id_given=i["id"], 
                brand=i["brand"]  if i["brand"]!=None else '', 
                car_type=i["type"]  if i["type"]!=None else '', 
                car_model=i["model"]  if i["model"]!=None else '', 
                release_year=i["release_year"]  if i["release_year"]!=None else 0, 
                variant=i["variant"]  if i["variant"]!=None else '', 
                usable_battery_size=i["ac_charger"]["usable_phases"]  if i["ac_charger"]!=None and i["ac_charger"]["usable_phases"]!=None else 0, 
                ac_charger_max_power=i["ac_charger"]["max_power"]  if i["ac_charger"]!=None and i["ac_charger"]["max_power"]!=None else 0, 
                dc_charger_max_power=i["dc_charger"]["max_power"]  if i["dc_charger"]!=None and i["dc_charger"]["max_power"]!=None else 0, 
                energy_average_consumption=i["energy_consumption"]["average_consumption"]  if i["energy_consumption"]!=None and i["energy_consumption"]["average_consumption"]!=None else 0,
                owner=list(Car_Owner.objects.filter(owner_id=ownerID))[0])
            if i["dc_charger"]!=None and i["dc_charger"]["ports"]!=None:
                for j in i["dc_charger"]["ports"]:
                    dc_charger_port.objects.create(car=list(Car.objects.filter(car_id_given=i["id"]))[0], port=j)
            if i["ac_charger"]!=None and i["ac_charger"]["ports"]!=None:
                for j in i["ac_charger"]["ports"]:
                    ac_charger_port.objects.create(car=list(Car.objects.filter(car_id_given=i["id"]))[0], port=j)
                    