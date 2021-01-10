import requests
import json


def sessionsPerEV(vehicleID, yyyymmdd_from, yyyymmdd_to, api_key):
    # print(vehicleID, yyyymmdd_from, yyyymmdd_to)
    x = requests.get(f'http://127.0.0.1:8765/evcharge/api/get_token_from_api_key/{api_key}') # we need to create this
    print(x.text)
    token = json.loads(x.text)['token']
    x = requests.get(f'http://127.0.0.1:8765/evcharge/api/SessionsPerEV/{vehicleID}/{yyyymmdd_from}/{yyyymmdd_to}', headers={'X-OBSERVATORY-AUTH':f'{token}'})
    print(json.loads(x.text)['PeriodFrom'])