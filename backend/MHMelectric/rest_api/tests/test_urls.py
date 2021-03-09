from django.test import SimpleTestCase
from django.urls import reverse, resolve

from rest_api.views import sessions_per_point, sessions_per_station, sessions_per_ev, sessions_per_provider, SessionsUpload, check_db_connection, resetsessions

class TestRestApiUrls(SimpleTestCase):

    def test_sessions_per_point(self):
        url = reverse('sessions_per_point', args=['some-pointID', 'some-date_from', 'some-date_to'])
        self.assertEquals(resolve(url).func, sessions_per_point)

    def test_sessions_per_station(self):
        url = reverse('sessions_per_station', args=['some-stationID', 'some-date_from', 'some-date_to'])
        self.assertEquals(resolve(url).func, sessions_per_station)

    def test_sessions_per_ev(self):
        url = reverse('sessions_per_ev', args=['some-vehicleID', 'some-date_from', 'some-date_to'])
        self.assertEquals(resolve(url).func, sessions_per_ev)

    def test_sessions_per_provider(self):
        url = reverse('sessions_per_provider', args=['some-providerID', 'some-date_from', 'some-date_to'])
        self.assertEquals(resolve(url).func, sessions_per_provider)

    def test_sessions_upload(self):
        url = reverse('sessions_upload')
        self.assertEquals(resolve(url).func.view_class, SessionsUpload)

    def test_check_db_connection(self):
        url = reverse('check_db_connection')
        self.assertEquals(resolve(url).func, check_db_connection)

    def test_resetsessions(self):
        url = reverse('resetsessions')
        self.assertEquals(resolve(url).func, resetsessions)
