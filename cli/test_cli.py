#run tests with python3 -m pytest test_cli.py
from cli_side import main
import pytest
import request


def test_login(capsys):
    main(['login','--username','some_name','--passw','some_passw','--format','json','--test'])
    assert request.url_to_send == "http://localhost:8765/evcharge/api/cli_login"
    

def test_logout():
    main(['logout','--apikey','1234-1234-1234','--format','csv','--test'])
    assert request.url_to_send == "http://localhost:8765/evcharge/api/cli_logout"

def test_sessions_per_point():
    main(['SessionsPerPoint','--point','1','--datefrom','20201212','--dateto','20211212','--format','json','--apikey','1234-1234-1234','--test'])
    assert request.url_to_send == "http://localhost:8765/evcharge/api/SessionsPerPoint/1/20201212/20211212?format=json"

def test_sessions_per_ev():
    main(['SessionsPerEV','--ev','1','--datefrom','20201212','--dateto','20211212','--format','json','--apikey','1234-1234-1234','--test'])
    assert request.url_to_send == "http://localhost:8765/evcharge/api/SessionsPerEV/1/20201212/20211212?format=json"

def test_sessions_per_provider():
    main(['SessionsPerProvider','--provider','1','--datefrom','20201212','--dateto','20211212','--format','json','--apikey','1234-1234-1234','--test'])
    assert request.url_to_send == "http://localhost:8765/evcharge/api/SessionsPerProvider/1/20201212/20211212?format=json"

def test_sessions_per_station():
    main(['SessionsPerStation','--station','1','--datefrom','20201212','--dateto','20211212','--format','json','--apikey','1234-1234-1234','--test'])
    assert request.url_to_send == "http://localhost:8765/evcharge/api/SessionsPerStation/1/20201212/20211212?format=json"

def test_reset_sessions():
    main(['resetsessions','--format','json','--apikey','1234-1234-1234','--test'])
    assert request.url_to_send == "http://localhost:8765/evcharge/api/admin/resetsessions?format=json"

def test_healthcheck():
    main(['healthcheck','--format','json','--apikey','1234-1234-1234','--test'])
    assert request.url_to_send == "http://localhost:8765/evcharge/api/admin/healthcheck/?format=json"

def test_admin_healthcheck():
    main(['Admin','healthcheck','--format','json','--apikey','1234-1234-1234','--test'])
    assert request.url_to_send == "http://localhost:8765/evcharge/api/admin/healthcheck/?format=json"

def test_admin_resetsessions():
    main(['Admin','resetsessions','--format','json','--apikey','1234-1234-1234','--test'])
    assert request.url_to_send == "http://localhost:8765/evcharge/api/admin/resetsessions?format=json"

def test_admin_users():
    main(['Admin','users','Mitsotakis','--format','csv','--apikey','1234-1234-1234','--test'])
    assert request.url_to_send == "http://localhost:8765/evcharge/api/admin/users/Mitsotakis?format=csv"

def test_usermod():
    main(['Admin','usermod','--username','Mitsotakis','--passw','ThankGod','--format','csv','--apikey','1234-1234-1234','--test'])
    assert request.url_to_send == "http://localhost:8765/evcharge/api/admin/usermod/Mitsotakis/ThankGod?format=csv"

def test_sessions_upd_fail():
    with pytest.raises(SystemExit) as e:
        main(['Admin','sessionsupd','--source','nope.csv','--format','csv','--apikey','1234-1234-1234','--test'])
    assert e.type == SystemExit
    assert request.url_to_send == "http://localhost:8765/evcharge/api/admin/system/sessionsupd?format=csv"

def test_sessions_upd_success():
    main(['Admin','sessionsupd','--source','skata.csv','--format','csv','--apikey','1234-1234-1234','--test'])
    assert request.url_to_send == "http://localhost:8765/evcharge/api/admin/system/sessionsupd?format=csv"

def test_bad_arguments():
    with pytest.raises(SystemExit) as e:
        main(['Admin','sessionsupd','--source','--format','csv','--apikey','1234-1234-1234','--test'])
    assert e.type == SystemExit

def test_help(): 
    with pytest.raises(SystemExit) as e:
        main(['Admin','--help','--test'])      
    assert e.type == SystemExit