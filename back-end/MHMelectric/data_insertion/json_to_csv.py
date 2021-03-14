# to run the script execute:  python3 manage.py shell < data_insertion/json_to_csv.py

import json
import csv
from MHMelectric.settings import BASE_DIR


with open(str(str(BASE_DIR) + "/data_insertion/file_paths.json")) as paths:
    path_to_file = json.loads(paths.read())["json_to_csv"]

# path_to_file = "/mnt/c/Users/marak/Downloads/OneDrive_1_05-01-2021/acn_data/caltech_acndata_sessions_12month.json"

fw = open("/mnt/c/Users/marak/Downloads/OneDrive_1_05-01-2021/acn_data/caltech_acndata_sessions_12month.csv", "w+")
writer = csv.writer(fw)
writer.writerow(["_id",
      "clusterID",
      "connectionTime",
      "disconnectTime",
      "doneChargingTime",
      "kWhDelivered",
      "sessionID",
      "siteID",
      "spaceID",
      "stationID",
      "timezone",
      "userID",
          "userInputs.WhPerMile",
          "userInputs.kWhRequested",
          "userInputs.milesRequested",
          "userInputs.minutesAvailable",
          "userInputs.modifiedAt",
          "userInputs.paymentRequired",
          "userInputs.requestedDeparture",
          "userInputs.userID"])
with open(path_to_file) as json_file:
    data = json.load(json_file)
    for i in list(data["_items"])[:100]:
        if(i["userInputs"]!=None):
            writer.writerow([i["_id"],
                i["clusterID"],
                i["connectionTime"],
                i["disconnectTime"],
                i["doneChargingTime"],
                i["kWhDelivered"],
                i["sessionID"],
                i["siteID"],
                i["spaceID"],
                i["stationID"],
                i["timezone"],
                i["userID"],
                    i["userInputs"][0]["WhPerMile"],
                    i["userInputs"][0]["kWhRequested"],
                    i["userInputs"][0]["milesRequested"],
                    i["userInputs"][0]["minutesAvailable"],
                    i["userInputs"][0]["modifiedAt"],
                    i["userInputs"][0]["paymentRequired"],
                    i["userInputs"][0]["requestedDeparture"],
                    i["userInputs"][0]["userID"]])
        else:
            writer.writerow([i["_id"],
                i["clusterID"],
                i["connectionTime"],
                i["disconnectTime"],
                i["doneChargingTime"],
                i["kWhDelivered"],
                i["sessionID"],
                i["siteID"],
                i["spaceID"],
                i["stationID"],
                i["timezone"],
                i["userID"],
                    'null',
                    'null',
                    'null',
                    'null',
                    'null',
                    'null',
                    'null',
                    'null'])
        print(i["_id"])

fw.close()