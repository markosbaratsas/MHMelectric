import requests
import json
from pathlib import Path
import os

from requests import api

def sessionsPerPoint(pointID, yyyymmdd_from, yyyymmdd_to, api_key):
    x = requests.get(f'http://127.0.0.1:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(f'http://127.0.0.1:8765/evcharge/api/SessionsPerPoint/{pointID}/{yyyymmdd_from}/{yyyymmdd_to}', headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(json.loads(x.text))
    except:
        print(json.loads(x.text))

def sessionsPerStation(stationID, yyyymmdd_from, yyyymmdd_to, api_key):
    x = requests.get(f'http://127.0.0.1:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(f'http://127.0.0.1:8765/evcharge/api/SessionsPerStation/{stationID}/{yyyymmdd_from}/{yyyymmdd_to}', headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(json.loads(x.text))
    except:
        print(json.loads(x.text))

def sessionsPerProvider(providerID, yyyymmdd_from, yyyymmdd_to, api_key):
    x = requests.get(f'http://127.0.0.1:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(f'http://127.0.0.1:8765/evcharge/api/SessionsPerProvider/{providerID}/{yyyymmdd_from}/{yyyymmdd_to}', headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(json.loads(x.text))
    except:
        print(json.loads(x.text))

def sessionsPerEV(vehicleID, yyyymmdd_from, yyyymmdd_to, api_key):
    x = requests.get(f'http://127.0.0.1:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}})
    try:
        token = json.loads(x.text)['token']
        x = requests.get(f'http://127.0.0.1:8765/evcharge/api/SessionsPerEV/{vehicleID}/{yyyymmdd_from}/{yyyymmdd_to}', headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(json.loads(x.text))
    except:
        print(json.loads(x.text))
    

def login(username, password):
    x = requests.post(f'http://127.0.0.1:8765/evcharge/api/cli_login', data = {'username': {username}, 'password': {password}}) 
    file = open(str(Path.home()) + "/softeng20bAPI.token", 'w+')
    file.write(json.loads(x.text)['api_key'])
    file.close()
    print('Your API-key is: ', json.loads(x.text)['api_key'])    

def logout(api_key):
    x = requests.post(f'http://127.0.0.1:8765/evcharge/api/cli_logout', data = {'api_key': {api_key}}) 
    path = str(Path.home()) + "/softeng20bAPI.token"
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file  softeng20bAPI.token does not exist")
    print(x.text)

def resetsessions(api_key):
    x = requests.get(f'http://127.0.0.1:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.post(f'http://127.0.0.1:8765/evcharge/api/resetsessions',  headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(json.loads(x.text))
    except:
        print(json.loads(x.text))

def healthcheck(api_key):
    x = requests.get(f'http://127.0.0.1:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(f'http://127.0.0.1:8765/evcharge/api/admin/healthcheck/',  headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(x.json()['status'])
    except:
        print(json.loads(x.text))

def admin_healthcheck(api_key):
    x = requests.get(f'http://127.0.0.1:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(f'http://127.0.0.1:8765/evcharge/api/admin/healthcheck/',  headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(json.loads(x.text))
    except:
        print(json.loads(x.text))

def admin_resetsessions(api_key):
    x = requests.get(f'http://127.0.0.1:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.post(f'http://127.0.0.1:8765/evcharge/api/admin/resetsessions',  headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(json.loads(x.text))
    except:
        print(json.loads(x.text))

def admin_users(username, api_key):
    x = requests.get(f'http://127.0.0.1:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(f'http://127.0.0.1:8765/evcharge/api/admin/users/{username}',  headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(json.loads(x.text))
    except:
        print(json.loads(x.text))

def admin_usermod(username, password, api_key):
    x = requests.get(f'http://127.0.0.1:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.post(f'http://127.0.0.1:8765/evcharge/api/admin/usermod/{username}/{password}',  headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(json.loads(x.text))
    except:
        print(json.loads(x.text))

def admin_sessionsupd(source, api_key):
    x = requests.get(f'http://127.0.0.1:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.post(f'http://127.0.0.1:8765/evcharge/api/admin/system/sessionsupd', files={'file':open(source,'rb')}, headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(json.loads(x.text))
    except:
        print(json.loads(x.text))