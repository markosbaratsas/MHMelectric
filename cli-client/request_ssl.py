import requests
import json
from pathlib import Path
import pathlib
import os
import sys

from requests import api

path = str(pathlib.Path(__file__).parent.absolute())+'/cert.pem'


def sessionsPerPoint(pointID, yyyymmdd_from, yyyymmdd_to, api_key,format):
    x = requests.get(f'https://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}},verify = path) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(f'https://localhost:8765/evcharge/api/SessionsPerPoint/{pointID}/{yyyymmdd_from}/{yyyymmdd_to}?format={format}', headers={'X-OBSERVATORY-AUTH':f'{token}'},verify = path)
        json_text = json.loads(x.text)
        print(json.dumps(json_text, indent=4))
    except:
        print(x.text)

def sessionsPerStation(stationID, yyyymmdd_from, yyyymmdd_to, api_key,format):
    x = requests.get(f'https://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}},verify = path) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(f'https://localhost:8765/evcharge/api/SessionsPerStation/{stationID}/{yyyymmdd_from}/{yyyymmdd_to}?format={format}', headers={'X-OBSERVATORY-AUTH':f'{token}'},verify = path)
        json_text = json.loads(x.text)
        print(json.dumps(json_text, indent=4))
    except:
        print(x.text)

def sessionsPerProvider(providerID, yyyymmdd_from, yyyymmdd_to, api_key,format):
    x = requests.get(f'https://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}},verify = path) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(f'https://localhost:8765/evcharge/api/SessionsPerProvider/{providerID}/{yyyymmdd_from}/{yyyymmdd_to}?format={format}', headers={'X-OBSERVATORY-AUTH':f'{token}'},verify = path)
        json_text = json.loads(x.text)
        print(json.dumps(json_text, indent=4))
    except:
        print(x.text)

def sessionsPerEV(vehicleID, yyyymmdd_from, yyyymmdd_to, api_key,format):
    x = requests.get(f'https://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}},verify = path)
    try:
        token = json.loads(x.text)['token']
        x = requests.get(f'https://localhost:8765/evcharge/api/SessionsPerEV/{vehicleID}/{yyyymmdd_from}/{yyyymmdd_to}?format={format}', headers={'X-OBSERVATORY-AUTH':f'{token}'},verify = path)
        json_text = json.loads(x.text)
        print(json.dumps(json_text, indent=4))
    except:
        print(x.text)
    

def login(username, password):
    x = requests.post(f'https://localhost:8765/evcharge/api/cli_login', data = {'username': {username}, 'password': {password}}, verify = path) 
    try:
        print('Your API-key is: ', json.loads(x.text)['api_key'])
        file = open(str(Path.home()) + "/softeng20bAPI.token", 'w+')
        file.write(json.loads(x.text)['api_key'])
        file.close()
    except:
        print(json.loads(x.text)['non_field_errors'][0])    

def logout(api_key):
    x = requests.post(f'https://localhost:8765/evcharge/api/cli_logout', data = {'api_key': {api_key}},verify = path) 
    token_path = str(Path.home()) + "/softeng20bAPI.token"
    if os.path.exists(token_path):
        os.remove(token_path)
    else:
        print("The file  softeng20bAPI.token does not exist")
    print(x.status_code)

def resetsessions(api_key, format):
    x = requests.get(f'https://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}},verify = path) #
    try:
        token = json.loads(x.text)['token']
        x = requests.post(f'https://localhost:8765/evcharge/api/admin/resetsessions?format={format}',  headers={'X-OBSERVATORY-AUTH':f'{token}'},verify = path)
        print(x.json()['status'])
    except:
        print(x.text)

def healthcheck(api_key, format):
    x = requests.get(f'https://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}},verify = path) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(f'https://localhost:8765/evcharge/api/admin/healthcheck/?format={format}',  headers={'X-OBSERVATORY-AUTH':f'{token}'},verify = path)
        print(x.json()['status'])
    except:
        print(x.text)

def admin_healthcheck(api_key, format):
    x = requests.get(f'https://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}},verify = path) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(f'https://localhost:8765/evcharge/api/admin/healthcheck/?format={format}',  headers={'X-OBSERVATORY-AUTH':f'{token}'},verify = path)
        print(x.json()['status'])
    except:
        print(x.text)

def admin_resetsessions(api_key, format):
    x = requests.get(f'https://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}},verify = path) #
    try:
        token = json.loads(x.text)['token']
        x = requests.post(f'https://localhost:8765/evcharge/api/admin/resetsessions?format={format}',  headers={'X-OBSERVATORY-AUTH':f'{token}'},verify = path)
        print(x.json()['status'])
    except:
        print(x.text)

def admin_users(username, api_key, format):
    x = requests.get(f'https://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}},verify = path) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(f'https://localhost:8765/evcharge/api/admin/users/{username}?format={format}',  headers={'X-OBSERVATORY-AUTH':f'{token}'},verify = path)
        json_text = json.loads(x.text)
        print(json.dumps(json_text, indent=4))
    except:
        print(x.text)

def admin_usermod(username, password, api_key, format):
    x = requests.get(f'https://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}},verify = path) #
    try:
        token = json.loads(x.text)['token']
        x = requests.post(f'https://localhost:8765/evcharge/api/admin/usermod/{username}/{password}?format={format}',  headers={'X-OBSERVATORY-AUTH':f'{token}'},verify = path)
        json_text = json.loads(x.text)
        print(json.dumps(json_text, indent=4))
    except:
        print(x.text)

def admin_sessionsupd(source, api_key, format):
    try:
        file_to_send = open(source,'rb')
    except:
        print("Cannot find or open file.")
        sys.exit()
    x = requests.get(f'https://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}},verify = path) #
    try:
        token = json.loads(x.text)['token']
        x = requests.post(f'https://localhost:8765/evcharge/api/admin/system/sessionsupd?format={format}', files={'file':file_to_send}, headers={'X-OBSERVATORY-AUTH':f'{token}'},verify = path)
        file_to_send.close()
        json_text = json.loads(x.text)
        print(json.dumps(json_text, indent=4))
    except:
        file_to_send.close()
        print(x.text)