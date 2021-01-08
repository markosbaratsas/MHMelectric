import argparse
import re
import datetime

def valid_username(s):
    r = re.compile('^(\\w)+$', re.ASCII)
    if r.match(s):
        return s
    else:
        msg = "Not a valid username: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)
    
def valid_date(s):
    try:
        return datetime.datetime.strptime(s, '%Y%m%d').date()
    except ValueError:
        msg = "Not a valid date: '{0}''.".format(s)
        raise argparse.ArgumentTypeError(msg)

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

parser = argparse.ArgumentParser(prog = 'ev_group23', description = 'Provide operations regarding the system',add_help = False)

sub_parsers = parser.add_subparsers(metavar = 'Scope', help = 'Operation to execute', required = True)
 
parser_healthcheck = sub_parsers.add_parser('healthcheck', help = 'Check connectivity to database')
parser_healthcheck.add_argument('healthcheck', action = 'store_true')

parser_resetsessions = sub_parsers.add_parser('resetsessions', help = 'Erase all sessions and set default admin account: username: admin, password: petrol4ever')
parser_resetsessions.add_argument('resetsessions', action = 'store_true')

parser_login = sub_parsers.add_parser('login', help = 'Login of user', add_help = False)
required = parser_login.add_argument_group('required arguments')
required.add_argument('--username', help = 'Username of user', metavar = 'username', type = str, required = True)
required.add_argument('--passw', help = 'Password of user', metavar = 'password', type = str, required = True )
optional = parser_login.add_argument_group('optional arguments')
add_help(optional)

parser_logout = sub_parsers.add_parser('logout', help = 'Logout of user')
parser_logout.add_argument('logout', action = 'store_true')

parser_SessionsPerPoint = sub_parsers.add_parser('SessionsPerPoint', help = 'Show sessions of specific point', add_help = False)
required = parser_SessionsPerPoint.add_argument_group('required arguments')
required.add_argument('--point', help = 'PointID', metavar = 'point_id', type = str, required = True)
required.add_argument('--datefrom', help = 'Starting Date', metavar = 'date_from', type = valid_date, required = True)
optional = parser_SessionsPerPoint.add_argument_group('optional arguments')
optional.add_argument('--dateto', help = 'Finishing Date', metavar = 'date_to', type = valid_date, default = datetime.date.today())
add_help(optional)

parser_SessionsPerStation = sub_parsers.add_parser('SessionsPerStation', help = 'Show sessions of specific station', add_help = False)
required = parser_SessionsPerStation.add_argument_group('required arguments')
required.add_argument('--station', help = 'StationID', metavar = 'station_id', type = str, required = True)
required.add_argument('--datefrom', help = 'Starting Date', metavar = 'date_from', type =  valid_date, required = True)
optional = parser_SessionsPerStation.add_argument_group('optional arguments')
optional.add_argument('--dateto', help = 'Finishing Date', metavar = 'date_to', type = valid_date, default = datetime.date.today())
add_help(optional)

parser_SessionsPerEV = sub_parsers.add_parser('SessionsPerEV', help = 'Show sessions of specific electric vehicle', add_help = False)
required = parser_SessionsPerEV.add_argument_group('required arguments')
required.add_argument('--ev', help = 'VehicleID', metavar = 'vehicle_id', type = str, required = True)
required.add_argument('--datefrom', help = 'Starting Date', metavar = 'date_from', type =  valid_date, required = True)
optional = parser_SessionsPerEV.add_argument_group('optional arguments')
optional.add_argument('--dateto', help = 'Finishing Date', metavar = 'date_to', type = valid_date, default = datetime.date.today())
add_help(optional)

parser_SessionsPerProvider = sub_parsers.add_parser('SessionsPerProvider', help = 'Show sessions of specific provider', add_help = False)
required = parser_SessionsPerProvider.add_argument_group('required arguments')
required.add_argument('--provider', help = 'ProviderID', metavar = 'provider_id', type = str, required = True)
required.add_argument('--datefrom', help = 'Starting Date', metavar = 'date_from', type =  valid_date, required = True)
optional = parser_SessionsPerProvider.add_argument_group('optional arguments')
optional.add_argument('--dateto', help = 'Finishing Date', metavar = 'date_to', type = valid_date, default = datetime.date.today())
add_help(optional)

parser_Admin = sub_parsers.add_parser('Admin', help = 'Operations executed by admin')

admin_sub_parsers = parser_Admin.add_subparsers(metavar = 'Operation', help = '')

parser_usermod = admin_sub_parsers.add_parser('usermod', help = 'Create new user or change password', add_help = False)
required = parser_usermod.add_argument_group('required arguments')
required.add_argument('--username', help = 'Username', metavar = 'username', type = valid_username, required = True)
required.add_argument('--passw', help = 'Password', metavar = 'password', type = str, required = True)
optional = parser_usermod.add_argument_group('optional arguments')
add_help(optional)

parser_users = admin_sub_parsers.add_parser('users', help = 'Show user state')
parser_users.add_argument('username',help = 'Username', metavar = 'username', type = valid_username)

parser_sessionsupd = admin_sub_parsers.add_parser('sessionsupd', help = 'Upload new sessions records from CSV file', add_help = False)
required = parser_sessionsupd.add_argument_group('required arguments')
required.add_argument('--source', help = 'Record file', metavar = 'CSV file', type = valid_file, required = True)
optional = parser_sessionsupd.add_argument_group('optional arguments')
add_help(optional)

parser_admin_healthcheck = admin_sub_parsers.add_parser('healthcheck', help = 'Check connectivity to database')
parser_admin_healthcheck.add_argument('healthcheck', action = 'store_true')

parser_admin_resetsessions = admin_sub_parsers.add_parser('resetsessions', help = 'Erase all sessions and set default admin account: username: admin, password: petrol4ever')
parser_admin_resetsessions.add_argument('resetsessions', action = 'store_true')

required = parser.add_argument_group('required arguments')

optional = parser.add_argument_group('optional arguments')
 
optional.add_argument(
    '-h',
    '--help',
    action='help',
    default= argparse.SUPPRESS,
    help='show this help message and exit'
)

required.add_argument('--format', choices = ['json', 'csv'], required = True, 
                    help = 'Format of result', metavar = 'format', type = str)

required.add_argument('--apikey', type = valid_api_key, required = True, metavar = 'apikey', help = 'API key of user')


#it's important to write --format ff --apikey --kk SCOPE in that order
if __name__ == '__main__':
     args = parser.parse_args()
     print(args)