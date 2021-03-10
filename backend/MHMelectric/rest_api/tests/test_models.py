from django.test import TestCase
from rest_api.models import Station, Charging_point, Charge_program, Provider


class TestModels(TestCase):

    def setUp(self):
        self.station = Station.objects.create(
            station_id_given='test', 
            country='Greece', 
            city='Athens', 
            street='Katechaki', 
            street_number='52', 
            postal_code='11525', 
            phone_number='691235678', 
            email='eimai@i.maria'
        )

    def test_station(self):
        station = self.station

        self.assertDictEqual(station.get_some_info(), {
            'country': station.country,
            'city': station.city,
            'street': station.street,
            'street_number': station.street_number,
            'postal_code': int(station.postal_code),
            'phone_number': int(station.phone_number),
            'email': station.email
        })

    def test_charging_point(self):
        station = self.station
        charging_point = Charging_point.objects.create(
            charging_point_id_given='test',
            station=station
        )

        self.assertDictEqual(charging_point.get_some_info(), {
            'station_info': station.get_some_info()
        })

    def test_charge_program(self):
        charge_program = Charge_program.objects.create(
            price=7,
            duration=20,
            description='Some description'
        )

        self.assertDictEqual(charge_program.get_some_info(), {
            'price': charge_program.price,
            'duration': charge_program.duration,
            'description': charge_program.description
        })

    def test_provider(self):
        provider = Provider.objects.create(
            provider_id_given='test',
            title='some title',
            website_url='www.some-website.gr',
            comments='Comments',
            primary_phone=6912345678,
            secondary_phone=6912345678,
            address_info='Katechaki 52, Athens',
            email='eimai@i.maria'
        )

        self.assertDictEqual(provider.get_some_info(), {
            'title': provider.title,
            'website_url': provider.website_url,
            'comments': provider.comments,
            'primary_phone': int(provider.primary_phone),
            'secondary_phone': int(provider.secondary_phone),
            'address_info': provider.address_info,
            'email': provider.email
        })