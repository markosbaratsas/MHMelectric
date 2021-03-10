import datetime
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.authtoken.models import Token
from urllib.parse import urlencode
from pytz import timezone

from rest_api.views import sessions_per_point, sessions_per_station, sessions_per_ev, sessions_per_provider, check_db_connection
from rest_api.models import Session, Charging_point, Station, Car, Provider


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.sessions_per_point_url = reverse('sessions_per_point', args=['1', '20200101', '20200104'])
        self.sessions_per_station_url = reverse('sessions_per_station', args=['1', '20200101', '20200104'])
        self.sessions_per_ev_url = reverse('sessions_per_ev', args=['1', '20200101', '20200104'])
        self.sessions_per_provider_url = reverse('sessions_per_provider', args=['1', '20200101', '20200104'])
        self.check_db_connection_url = reverse('check_db_connection')

        # creatin of objects that are needed for most of the tests below
        station = Station.objects.create(station_id_given=1)
        self.station = station
        charging_point = Charging_point.objects.create(charging_point_id_given=1, station=self.station)
        self.charging_point = charging_point
        car = Car.objects.create(car_id_given=1)
        self.car = car
        provider = Provider.objects.create(provider_id_given=1)
        self.provider = provider

        self.session01 = Session.objects.create(
            car=car, 
            charging_point=charging_point,
            station=station,
            provider=provider,
            connection_time=datetime.datetime(2020, 1, 2, 18, 16, 50).replace(tzinfo=timezone('UTC')),
            disconnection_time=datetime.datetime(2020, 1, 2, 18, 50, 50).replace(tzinfo=timezone('UTC')),
            done_charging_time=datetime.datetime(2020, 1, 2, 18, 50, 50).replace(tzinfo=timezone('UTC')),
            user_modified_at=datetime.datetime(2020, 1, 2, 18, 40, 50).replace(tzinfo=timezone('UTC')),
            user_requested_departure=datetime.datetime(2020, 1, 2, 18, 52, 50).replace(tzinfo=timezone('UTC')),
        )
        self.session02 = Session.objects.create(
            car=car, 
            charging_point=charging_point,
            station=station,
            provider=provider,
            connection_time=datetime.datetime(2020, 1, 3, 18, 16, 50).replace(tzinfo=timezone('UTC')),
            disconnection_time=datetime.datetime(2020, 1, 3, 18, 50, 50).replace(tzinfo=timezone('UTC')),
            done_charging_time=datetime.datetime(2020, 1, 3, 18, 50, 50).replace(tzinfo=timezone('UTC')),
            user_modified_at=datetime.datetime(2020, 1, 3, 18, 40, 50).replace(tzinfo=timezone('UTC')),
            user_requested_departure=datetime.datetime(2020, 1, 3, 18, 52, 50).replace(tzinfo=timezone('UTC')),
        )
        self.session03 = Session.objects.create(
            car=car, 
            charging_point=charging_point,
            station=station,
            provider=provider,
            connection_time=datetime.datetime(2020, 2, 3, 18, 16, 50).replace(tzinfo=timezone('UTC')),
            disconnection_time=datetime.datetime(2020, 2, 3, 18, 50, 50).replace(tzinfo=timezone('UTC')),
            done_charging_time=datetime.datetime(2020, 2, 3, 18, 50, 50).replace(tzinfo=timezone('UTC')),
            user_modified_at=datetime.datetime(2020, 2, 3, 18, 40, 50).replace(tzinfo=timezone('UTC')),
            user_requested_departure=datetime.datetime(2020, 2, 3, 18, 52, 50).replace(tzinfo=timezone('UTC')),
        )

    def test_sessions_per_point(self):
        user, _ = User.objects.get_or_create(username='some-username')
        token, _ = Token.objects.get_or_create(user=user)
        response = self.client.get(self.sessions_per_point_url, HTTP_X_OBSERVATORY_AUTH=token.key)

        # should only get 2 sessions and not the 3rd one because it is not on the date range
        self.assertEquals(len(response.data["ChargingSessionsList"]), 2)

    def test_sessions_per_station(self):
        user, _ = User.objects.get_or_create(username='some-username')
        token, _ = Token.objects.get_or_create(user=user)
        response = self.client.get(self.sessions_per_station_url, HTTP_X_OBSERVATORY_AUTH=token.key)

        # should only get 2 sessions and not the 3rd one because it is not on the date range
        self.assertEquals(response.data["SessionsSummaryList"][0]["PointSessions"], 2)

    def test_sessions_per_ev(self):
        user, _ = User.objects.get_or_create(username='some-username')
        token, _ = Token.objects.get_or_create(user=user)
        response = self.client.get(self.sessions_per_ev_url, HTTP_X_OBSERVATORY_AUTH=token.key)

        # should only get 2 sessions and not the 3rd one because it is not on the date range
        self.assertEquals(len(response.data["ChargingSessionsList"]), 2)

    def test_sessions_per_provider(self):
        user, _ = User.objects.get_or_create(username='some-username')
        token, _ = Token.objects.get_or_create(user=user)
        response = self.client.get(self.sessions_per_provider_url, HTTP_X_OBSERVATORY_AUTH=token.key)

        # should only get 2 sessions and not the 3rd one because it is not on the date range
        self.assertEquals(len(response.data["Sessions"]), 2)

    def test_check_db_connection(self):
        response = self.client.get(self.check_db_connection_url)

        # should only get 2 sessions and not the 3rd one because it is not on the date range
        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(response.data, {'status': 'OK'})
