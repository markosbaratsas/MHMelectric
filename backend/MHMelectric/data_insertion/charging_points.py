# to run the script execute:  python3 manage.py shell < data_insertion/charging_points.py
# or fix it accordingly based on the directory you are


# first run python3 manage.py shell < data_insertion/helper_parse_charging_point.py


import json
import sys
from decimal import Decimal
from rest_api.models import *

path_to_file = "/mnt/c/Users/marak/Downloads/OneDrive_1_1-5-2021/charging_points_europe_json/ready_data.json"

with open(path_to_file) as json_file:
    data = json.load(json_file)
    data = data["data"]
    for i in list(data):
        if(i["OperatorInfo"]!=None and i["OperatorInfo"]["ID"]!=None):
            Operator.objects.create(operator_id_given=i["OperatorInfo"]["ID"],
                title=i["OperatorInfo"]["Title"]  if i["OperatorInfo"]!=None and i["OperatorInfo"]["Title"]!=None else '',
                website_url=i["OperatorInfo"]["WebsiteURL"]  if i["OperatorInfo"]!=None and i["OperatorInfo"]["WebsiteURL"]!=None else '',
                comments=i["OperatorInfo"]["Comments"]  if i["OperatorInfo"]!=None and i["OperatorInfo"]["Comments"]!=None else '',
                primary_phone=''.join(i["OperatorInfo"]["PhonePrimaryContact"].split("-"))  if i["OperatorInfo"]!=None and i["OperatorInfo"]["PhonePrimaryContact"]!=None and i["OperatorInfo"]["PhonePrimaryContact"]!='' and i["OperatorInfo"]["PhonePrimaryContact"]!='866) 816-7584' else 0,
                secondary_phone=''.join(i["OperatorInfo"]["PhoneSecondaryContact"].split("-"))  if i["OperatorInfo"]!=None and i["OperatorInfo"]["PhoneSecondaryContact"]!=None and i["OperatorInfo"]["PhoneSecondaryContact"]!='' else 0,
                address_info=i["OperatorInfo"]["AddressInfo"]  if i["OperatorInfo"]!=None and i["OperatorInfo"]["AddressInfo"]!=None else '',
                email=i["OperatorInfo"]["ContactEmail"]  if i["OperatorInfo"]!=None and i["OperatorInfo"]["ContactEmail"]!=None else '')

        Charging_point.objects.create(charging_point_id_given=i["ID"],
            country=i["AddressInfo"]["Country"]["Title"]  if i["AddressInfo"]!=None and i["AddressInfo"]["Country"]!=None and i["AddressInfo"]["Country"]["Title"]!=None else '',
            city=i["AddressInfo"]["Town"]  if i["AddressInfo"]!=None and i["AddressInfo"]["Town"]!=None else '',
            street=' '.join(i["AddressInfo"]["AddressLine1"].split(" ")[1:])  if i["AddressInfo"]!=None and i["AddressInfo"]["AddressLine1"]!=None else '',
            street_number=list(i["AddressInfo"]["AddressLine1"].split(" "))[0]  if i["AddressInfo"]!=None and i["AddressInfo"]["AddressLine1"]!=None else '',
            postal_code=i["AddressInfo"]["Postcode"]  if i["AddressInfo"]!=None and i["AddressInfo"]["Postcode"]!=None else 0,
            phone_number=''.join((''.join(i["AddressInfo"]["ContactTelephone1"].split("-"))).split(' '))  if i["AddressInfo"]!=None and i["AddressInfo"]["ContactTelephone1"]!=None and i["AddressInfo"]["ContactTelephone1"]!='' and i["AddressInfo"]["ContactTelephone1"]!='415-392-3434  877-798-3752' else 0,
            email=i["AddressInfo"]["ContactEmail"]  if i["AddressInfo"]!=None and i["AddressInfo"]["ContactEmail"]!=None else '',
            operator=list(Operator.objects.filter(operator_id_given=i["OperatorID"]))[0] if len(list(Operator.objects.filter(operator_id_given=i["OperatorID"])))!=0 else None)
