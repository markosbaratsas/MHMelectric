# to run the script execute:  python3 manage.py shell < data_insertion/charging_points.py
# or fix it accordingly based on the directory you are

import json
import sys

path_to_file = "/mnt/c/Users/markg/Downloads/OneDrive_1_05-01-2021/charging_points_europe_json/reference2.json"

with open(path_to_file) as json_file:
    data = json.load(json_file)

