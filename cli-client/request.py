import requests
import json
from pathlib import Path
import os
import sys

from requests import api

global url_to_send 
global data_to_send

def sessionsPerPoint(pointID, yyyymmdd_from, yyyymmdd_to, api_key,format):
    global url_to_send 
    url_to_send = f'http://localhost:8765/evcharge/api/SessionsPerPoint/{pointID}/{yyyymmdd_from}/{yyyymmdd_to}?format={format}'
    x = requests.get(f'http://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']    
        x = requests.get(url_to_send, headers={'X-OBSERVATORY-AUTH':f'{token}'})
        json_text = json.loads(x.text)
        print(json.dumps(json_text, indent=4))
    except:
        print(x.text)

def sessionsPerStation(stationID, yyyymmdd_from, yyyymmdd_to, api_key,format):
    global url_to_send 
    url_to_send= f'http://localhost:8765/evcharge/api/SessionsPerStation/{stationID}/{yyyymmdd_from}/{yyyymmdd_to}?format={format}'
    x = requests.get(f'http://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(url_to_send, headers={'X-OBSERVATORY-AUTH':f'{token}'})
        json_text = json.loads(x.text)
        print(json.dumps(json_text, indent=4))
    except:
        print(x.text)

def sessionsPerProvider(providerID, yyyymmdd_from, yyyymmdd_to, api_key,format):
    global url_to_send 
    url_to_send = f'http://localhost:8765/evcharge/api/SessionsPerProvider/{providerID}/{yyyymmdd_from}/{yyyymmdd_to}?format={format}'
    x = requests.get(f'http://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']     
        x = requests.get(url_to_send, headers={'X-OBSERVATORY-AUTH':f'{token}'})
        json_text = json.loads(x.text)
        print(json.dumps(json_text, indent=4))
    except:
        print(x.text)

def sessionsPerEV(vehicleID, yyyymmdd_from, yyyymmdd_to, api_key,format):
    global url_to_send 
    url_to_send = f'http://localhost:8765/evcharge/api/SessionsPerEV/{vehicleID}/{yyyymmdd_from}/{yyyymmdd_to}?format={format}'
    x = requests.get(f'http://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}})
    try:
        token = json.loads(x.text)['token']  
        x = requests.get(url_to_send, headers={'X-OBSERVATORY-AUTH':f'{token}'})
        json_text = json.loads(x.text)
        print(json.dumps(json_text, indent=4))
    except:
        print(x.text)
    

def login(username, password):
    global url_to_send 
    global data_to_send
    data_to_send = {'username': {username}, 'password': {password}}
    url_to_send = f'http://localhost:8765/evcharge/api/cli_login'
    x = requests.post(url_to_send, data = data_to_send) 
    try:
        print('Your API-key is: ', json.loads(x.text)['api_key'])
        file = open(str(Path.home()) + "/softeng20bAPI.token", 'w+')
        file.write(json.loads(x.text)['api_key'])
        file.close()
    except:
        print(json.loads(x.text)['non_field_errors'][0])    

def logout(api_key):
    global url_to_send 
    url_to_send = f'http://localhost:8765/evcharge/api/cli_logout'
    x = requests.post(url_to_send, data = {'api_key': {api_key}}) 
    path = str(Path.home()) + "/softeng20bAPI.token"
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file  softeng20bAPI.token does not exist")
    print(x.status_code)

def resetsessions(api_key, format):
    global url_to_send 
    url_to_send = f'http://localhost:8765/evcharge/api/admin/resetsessions?format={format}'
    x = requests.get(f'http://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.post(url_to_send,  headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(x.json()['status'])
    except:
        print(x.text)

def healthcheck(api_key, format):
    global url_to_send 
    url_to_send = f'http://localhost:8765/evcharge/api/admin/healthcheck/?format={format}'
    x = requests.get(f'http://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(url_to_send,  headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(x.json()['status'])
    except:
        print(x.text)

def admin_healthcheck(api_key, format):
    global url_to_send 
    url_to_send = f'http://localhost:8765/evcharge/api/admin/healthcheck/?format={format}'
    x = requests.get(f'http://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(url_to_send,  headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(x.json()['status'])
    except:
        print(x.text)

def admin_resetsessions(api_key, format):
    global url_to_send 
    url_to_send = f'http://localhost:8765/evcharge/api/admin/resetsessions?format={format}'
    x = requests.get(f'http://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.post(url_to_send,  headers={'X-OBSERVATORY-AUTH':f'{token}'})
        print(x.json()['status'])
    except:
        print(x.text)

def admin_users(username, api_key, format):
    global url_to_send 
    url_to_send = f'http://localhost:8765/evcharge/api/admin/users/{username}?format={format}'
    x = requests.get(f'http://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.get(url_to_send,  headers={'X-OBSERVATORY-AUTH':f'{token}'})
        json_text = json.loads(x.text)
        print(json.dumps(json_text, indent=4))
    except:
        print(x.text)

def admin_usermod(username, password, api_key, format):
    global url_to_send 
    url_to_send = f'http://localhost:8765/evcharge/api/admin/usermod/{username}/{password}?format={format}'
    x = requests.get(f'http://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.post(url_to_send,  headers={'X-OBSERVATORY-AUTH':f'{token}'})
        json_text = json.loads(x.text)
        print(json.dumps(json_text, indent=4))
    except:
        print(x.text)

def admin_sessionsupd(source, api_key, format):
    global url_to_send 
    url_to_send = f'http://localhost:8765/evcharge/api/admin/system/sessionsupd?format={format}'
    try:
        file_to_send = open(source,'rb')
    except:
        print("Cannot find or open file.")
        sys.exit()
    x = requests.get(f'http://localhost:8765/evcharge/api/get_token_from_api_key', data = {'api_key': {api_key}}) #
    try:
        token = json.loads(x.text)['token']
        x = requests.post(url_to_send, files={'file':file_to_send}, headers={'X-OBSERVATORY-AUTH':f'{token}'})
        file_to_send.close()
        json_text = json.loads(x.text)
        print(json.dumps(json_text, indent=4))
    except:
        print(x.text)