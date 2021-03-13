import argparse
import re
import datetime
import urllib3
import requests
import sys
import pathlib

def valid_username(s):
    r = re.compile('^(\\w)+$', re.ASCII)
    if r.match(s):
        return s
    else:
        msg = "Not a valid username: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)
    
def valid_date(s):
    try:
        datetime.datetime.strptime(s, '%Y%m%d').date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)
    return s

def valid_api_key(s):
    r = re.compile('^([a-zA-Z0-9]){4}-([a-zA-Z0-9]){4}-([a-zA-Z0-9]){4}$', re.ASCII)
    if r.match(s):
        return s
    else:
        msg = "Not a valid API key: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def valid_file(s):
    if s.endswith('.csv'):
        return s
    else:
        msg = "Not a valid record file: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def add_help(x):
    x.add_argument(
        '-h',
        '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='show this help message and exit'
    )   
    x.add_argument(
        '--test',
        action='store_true',
        help=argparse.SUPPRESS
    )

parser = argparse.ArgumentParser(prog = 'ev_group23', description = 'Provide operations regarding the system')

sub_parsers = parser.add_subparsers(metavar = 'Scope', help = 'Operation to execute')
 
parser_healthcheck = sub_parsers.add_parser('healthcheck', help = 'Check connectivity to database', add_help = False)
parser_healthcheck.set_defaults(scope='healthcheck')
parser_healthcheck.add_argument('healthcheck', action = 'store_true')
required = parser_healthcheck.add_argument_group('required arguments')
required.add_argument('--format', choices = ['json', 'csv'], required = True, 
                    help = 'Format of result', metavar = 'format', type = str)
required.add_argument('--apikey', type = valid_api_key, required = True, metavar = 'apikey', help = 'API key of user')
optional = parser_healthcheck.add_argument_group('optional arguments')
add_help(optional)

parser_resetsessions = sub_parsers.add_parser('resetsessions', help = 'Erase all sessions and set default admin account: username: admin, password: petrol4ever', add_help = False)
parser_resetsessions.set_defaults(scope='resetsessions')
parser_resetsessions.add_argument('resetsessions', action = 'store_true')
required = parser_resetsessions.add_argument_group('required arguments')
required.add_argument('--format', choices = ['json', 'csv'], required = True, 
                    help = 'Format of result', metavar = 'format', type = str)
required.add_argument('--apikey', type = valid_api_key, required = True, metavar = 'apikey', help = 'API key of user')
optional = parser_resetsessions.add_argument_group('optional arguments')
add_help(optional)

parser_login = sub_parsers.add_parser('login', help = 'Login of user', add_help = False)
parser_login.set_defaults(scope='login')
required = parser_login.add_argument_group('required arguments')
required.add_argument('--username', help = 'Username of user', metavar = 'username', type = str, required = True)
required.add_argument('--passw', help = 'Password of user', metavar = 'password', type = str, required = True )
required.add_argument('--format', choices = ['json', 'csv'], required = True, 
                    help = 'Format of result', metavar = 'format', type = str)
#required.add_argument('--apikey', type = valid_api_key, required = True, metavar = 'apikey', help = 'API key of user')
optional = parser_login.add_argument_group('optional arguments')
add_help(optional)

parser_logout = sub_parsers.add_parser('logout', help = 'Logout of user',  add_help = False)
parser_logout.set_defaults(scope='logout')
parser_logout.add_argument('logout', action = 'store_true')
required = parser_logout.add_argument_group('required arguments')
required.add_argument('--format', choices = ['json', 'csv'], required = True, 
                    help = 'Format of result', metavar = 'format', type = str)
required.add_argument('--apikey', type = valid_api_key, required = True, metavar = 'apikey', help = 'API key of user')
optional = parser_logout.add_argument_group('optional arguments')
add_help(optional)

parser_SessionsPerPoint = sub_parsers.add_parser('SessionsPerPoint', help = 'Show sessions of specific point', add_help = False)
parser_SessionsPerPoint.set_defaults(scope='perPoint')
required = parser_SessionsPerPoint.add_argument_group('required arguments')
required.add_argument('--point', help = 'PointID', metavar = 'point_id', type = str, required = True)
required.add_argument('--datefrom', help = 'Starting Date', metavar = 'date_from', type = valid_date, required = True)
required.add_argument('--dateto', help = 'Finishing Date', metavar = 'date_to', type = valid_date, required=True)
required.add_argument('--format', choices = ['json', 'csv'], required = True, 
                    help = 'Format of result', metavar = 'format', type = str)
required.add_argument('--apikey', type = valid_api_key, required = True, metavar = 'apikey', help = 'API key of user')
optional = parser_SessionsPerPoint.add_argument_group('optional arguments')
add_help(optional)

parser_SessionsPerStation = sub_parsers.add_parser('SessionsPerStation', help = 'Show sessions of specific station', add_help = False)
parser_SessionsPerStation.set_defaults(scope='perStation')
required = parser_SessionsPerStation.add_argument_group('required arguments')
required.add_argument('--station', help = 'StationID', metavar = 'station_id', type = str, required = True)
required.add_argument('--datefrom', help = 'Starting Date', metavar = 'date_from', type =  valid_date, required = True)
required.add_argument('--dateto', help = 'Finishing Date', metavar = 'date_to', type = valid_date, required=True)
required.add_argument('--format', choices = ['json', 'csv'], required = True, 
                    help = 'Format of result', metavar = 'format', type = str)
required.add_argument('--apikey', type = valid_api_key, required = True, metavar = 'apikey', help = 'API key of user')
optional = parser_SessionsPerStation.add_argument_group('optional arguments')

add_help(optional)

parser_SessionsPerEV = sub_parsers.add_parser('SessionsPerEV', help = 'Show sessions of specific electric vehicle', add_help = False)
parser_SessionsPerEV.set_defaults(scope='perEV')
required = parser_SessionsPerEV.add_argument_group('required arguments')
required.add_argument('--ev', help = 'VehicleID', metavar = 'vehicle_id', type = str, required = True)
required.add_argument('--datefrom', help = 'Starting Date', metavar = 'date_from', type =  valid_date, required = True)
required.add_argument('--dateto', help = 'Finishing Date', metavar = 'date_to', type = valid_date, required=True)
required.add_argument('--format', choices = ['json', 'csv'], required = True, 
                    help = 'Format of result', metavar = 'format', type = str)
required.add_argument('--apikey', type = valid_api_key, required = True, metavar = 'apikey', help = 'API key of user')
optional = parser_SessionsPerEV.add_argument_group('optional arguments')
add_help(optional)

parser_SessionsPerProvider = sub_parsers.add_parser('SessionsPerProvider', help = 'Show sessions of specific provider', add_help = False)
parser_SessionsPerProvider.set_defaults(scope='perProvider')
required = parser_SessionsPerProvider.add_argument_group('required arguments')
required.add_argument('--provider', help = 'ProviderID', metavar = 'provider_id', type = str, required = True)
required.add_argument('--datefrom', help = 'Starting Date', metavar = 'date_from', type =  valid_date, required = True)
required.add_argument('--dateto', help = 'Finishing Date', metavar = 'date_to', type = valid_date, required=True)
required.add_argument('--format', choices = ['json', 'csv'], required = True, 
                    help = 'Format of result', metavar = 'format', type = str)
required.add_argument('--apikey', type = valid_api_key, required = True, metavar = 'apikey', help = 'API key of user')
optional = parser_SessionsPerProvider.add_argument_group('optional arguments')
add_help(optional)

parser_Admin = sub_parsers.add_parser('Admin', help = 'Operations executed by admin')
parser_Admin.set_defaults(scope='Admin')

admin_sub_parsers = parser_Admin.add_subparsers(metavar = 'Operation', help = '')

parser_usermod = admin_sub_parsers.add_parser('usermod', help = 'Create new user or change password', add_help = False)
parser_usermod.set_defaults(admin_scope='usermod')
required = parser_usermod.add_argument_group('required arguments')
required.add_argument('--username', help = 'Username', metavar = 'username', type = valid_username, required = True)
required.add_argument('--passw', help = 'Password', metavar = 'password', type = str, required = True)
required.add_argument('--format', choices = ['json', 'csv'], required = True, 
                    help = 'Format of result', metavar = 'format', type = str)
required.add_argument('--apikey', type = valid_api_key, required = True, metavar = 'apikey', help = 'API key of user')
optional = parser_usermod.add_argument_group('optional arguments')
add_help(optional)

parser_users = admin_sub_parsers.add_parser('users', help = 'Show user state',  add_help = False)
parser_users.set_defaults(admin_scope='users')
required = parser_users.add_argument_group('required arguments')
required.add_argument('username',help = 'Username', metavar = 'username', type = valid_username)
required.add_argument('--format', choices = ['json', 'csv'], required = True, 
                    help = 'Format of result', metavar = 'format', type = str)
required.add_argument('--apikey', type = valid_api_key, required = True, metavar = 'apikey', help = 'API key of user')
optional = parser_users.add_argument_group('optional arguments')
add_help(optional)

parser_sessionsupd = admin_sub_parsers.add_parser('sessionsupd', help = 'Upload new sessions records from CSV file', add_help = False)
parser_sessionsupd.set_defaults(admin_scope='sessionsupd')
required = parser_sessionsupd.add_argument_group('required arguments')
required.add_argument('--source', help = 'Record file', metavar = 'CSV file', type = valid_file, required = True)
required.add_argument('--format', choices = ['json', 'csv'], required = True, 
                    help = 'Format of result', metavar = 'format', type = str)
required.add_argument('--apikey', type = valid_api_key, required = True, metavar = 'apikey', help = 'API key of user')
optional = parser_sessionsupd.add_argument_group('optional arguments')
add_help(optional)

parser_admin_healthcheck = admin_sub_parsers.add_parser('healthcheck', help = 'Check connectivity to database',  add_help = False)
parser_admin_healthcheck.set_defaults(admin_scope='healthcheck')
parser_admin_healthcheck.add_argument('healthcheck', action = 'store_true')
required = parser_admin_healthcheck.add_argument_group('required arguments')
required.add_argument('--format', choices = ['json', 'csv'], required = True, 
                    help = 'Format of result', metavar = 'format', type = str)
required.add_argument('--apikey', type = valid_api_key, required = True, metavar = 'apikey', help = 'API key of user')
optional = parser_admin_healthcheck.add_argument_group('optional arguments')
add_help(optional)

parser_admin_resetsessions = admin_sub_parsers.add_parser('resetsessions', help = 'Erase all sessions and set default admin account: username: admin, password: petrol4ever', add_help = False)
parser_admin_resetsessions.set_defaults(admin_scope='resetsessions')
parser_admin_resetsessions.add_argument('resetsessions', action = 'store_true')
required = parser_admin_resetsessions.add_argument_group('required arguments')
required.add_argument('--format', choices = ['json', 'csv'], required = True, 
                    help = 'Format of result', metavar = 'format', type = str)
required.add_argument('--apikey', type = valid_api_key, required = True, metavar = 'apikey', help = 'API key of user')
optional = parser_admin_resetsessions.add_argument_group('optional arguments')
add_help(optional)


def main(args=None):
    urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)
    if not args:
        args = sys.argv[1:]
    args = parser.parse_args(args)
    path = str(pathlib.Path(__file__).parent.absolute())
    if args.test:
        import request as req
    else:
        try:
            requests.get(f'http://localhost:8765/evcharge/api/')
            import request as req
        except:
            try:
                requests.get(f'https://localhost:8765/evcharge/api/',verify = path+'/cert.pem')
                import request_ssl as req
            except:    
                print("There is no connection to server")
                sys.exit()
    try:
        if args.scope == 'login':
            req.login(args.username, args.passw)
        elif args.scope == 'logout':
            req.logout(args.apikey)
        elif args.scope == 'resetsessions':
            req.resetsessions(args.apikey, args.format)
        elif args.scope == 'healthcheck':
            req.healthcheck(args.apikey, args.format)
        elif args.scope == 'perPoint':
            req.sessionsPerPoint(args.point, args.datefrom, args.dateto, args.apikey, args.format)
        elif args.scope == 'perStation':
            req.sessionsPerStation(args.station, args.datefrom, args.dateto, args.apikey, args.format)
        elif args.scope == 'perEV':
            req.sessionsPerEV(args.ev, args.datefrom, args.dateto, args.apikey, args.format)
        elif args.scope == 'perProvider':
            req.sessionsPerProvider(args.provider, args.datefrom, args.dateto, args.apikey, args.format)
        else:
            if args.admin_scope == 'usermod':
                req.admin_usermod(args.username, args.passw, args.apikey, args.format)
            elif args.admin_scope == 'users':
                req.admin_users(args.username, args.apikey, args.format)
            elif args.admin_scope == 'sessionsupd':
                req.admin_sessionsupd(args.source, args.apikey, args.format)
            elif args.admin_scope == 'healthcheck':
                req.healthcheck(args.apikey,args.format)
            else:
                req.resetsessions(args.apikey,args.format)
    except Exception as e:
        print(e)
        print("i hope you are testing")

if __name__ == '__main__':
    main()