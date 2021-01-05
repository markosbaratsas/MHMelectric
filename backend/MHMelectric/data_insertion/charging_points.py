# to run the script execute:  python3 manage.py shell < data_insertion/charging_points.py
# or fix it accordingly based on the directory you are


# first run helper_parse_charging_point.py


import json
import sys
from rest_api.models import *

path_to_file = "/mnt/c/Users/markg/Downloads/OneDrive_1_05-01-2021/charging_points_europe_json/ready_data.json"

with open(path_to_file) as json_file:
    data = json.load(json_file)
    data = data["data"]

print(data[0])