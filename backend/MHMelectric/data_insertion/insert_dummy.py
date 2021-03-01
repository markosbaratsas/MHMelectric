# to run the script execute:  python3 manage.py shell < data_insertion/insert_dummy.py
# or fix it accordingly based on the directory you are


import json
import sys
from decimal import Decimal
import datetime
from rest_api.models import *
from pytz import timezone

path_to_file = "/mnt/c/Users/marak/Downloads/dummy_data.json"

with open(path_to_file) as json_file:
    data = json.load(json_file)
    for i in list(data["car_owners"]):
        user, created = User.objects.get_or_create(username=i["user"]["username"])
        user.set_password(i["user"]["password"])
        user.save()
        Car_Owner.objects.get_or_create(first_name=i["first_name"],
                                last_name=i["last_name"],
                                birthdate=datetime.datetime.strptime(i["birthdate"], "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone('UTC')),
                                country=i["country"],
                                city=i["city"],
                                street=i["street"],
                                street_number=Decimal(i["street_number"]),
                                postal_code=Decimal(i["postal_code"]),
                                bonus_points=Decimal(i["bonus_points"]),
                                user=user)

    for i in list(data["providers"]):
        Provider.objects.get_or_create(provider_id_given=i["provider_id_given"],
                                    title=i["title"],
                                    website_url=i["website_url"],
                                    comments=i["comments"],
                                    primary_phone=Decimal(i["primary_phone"]),
                                    address_info=i["address_info"],
                                    email=i["email"])

    for i in list(data["connection_types"]):
        Connection_type.objects.get_or_create(connection_type=i["connection_type"],
                                    general_type=i["general_type"],
                                    voltage=Decimal(i["voltage"]),
                                    amps=Decimal(i["amps"][0:2]))

    for i in list(data["charge_programs"]):
        Charge_program.objects.get_or_create(price=Decimal(i["price"]),
                                    duration=i["duration"],
                                    description=i["description"])
                                    