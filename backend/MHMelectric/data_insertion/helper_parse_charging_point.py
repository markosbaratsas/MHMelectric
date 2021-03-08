# In order to insert the given data I copied first 150 lines of `poi.json` into `used_data.json`.
# Then I run the following script to get a json that can be loaded...

import json
from MHMelectric.settings import BASE_DIR

with open(str(str(BASE_DIR) + "/data_insertion/file_paths.json")) as paths:
    path_to_file = json.loads(paths.read())["helper_parse_charging_point"]
    charging_points_created_file = json.loads(paths.read())["charging_points"]

# path_to_file = "/mnt/c/Users/marak/Downloads/OneDrive_1_1-5-2021/charging_points_europe_json/used_data.json"


# this file will be created
fw = open(charging_points_created_file, "w+")

fw.write('{ "data": [')
with open(path_to_file) as f:
    data = f.read()
    hello = data.split("\n")
    for i in hello[:148]:
        if(i==hello[147]):
            fw.write(i + "\n")
        else:
            fw.write(i + ",\n")

fw.write("]}")
fw.close()