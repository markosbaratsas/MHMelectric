import os
from rest_framework import serializers

from rest_api.models import (Car_Owner, Car, Charging_point, Station, Periodic_bill,
Provider, Charge_program, Session, UploadedCSV)

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['car_id', 'brand', 'car_type', 'car_model', 
                'release_year', 'variant', 'usable_battery_size']

class CarSerializerFrontendAdd(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['brand', 'car_type', 'car_model',
                'release_year', 'variant', 'usable_battery_size']

    def save(self, car_owner=None):

        try:
            car = Car.objects.create(
                brand=self.validated_data['brand'] if 'brand' in self.validated_data else '',
                car_type=self.validated_data['car_type'] if 'car_type' in self.validated_data else '',
                car_model=self.validated_data['car_model'] if 'car_model' in self.validated_data else '',
                release_year=self.validated_data['release_year'] if 'release_year' in self.validated_data else '',
                variant=self.validated_data['variant'] if 'variant' in self.validated_data else '',
                usable_battery_size=self.validated_data['usable_battery_size'] if 'usable_battery_size' in self.validated_data else 0,
                owner=car_owner
            )

            car.car_id_given = car.car_id

            car.save()
        except:
            car = None

        return car


class UploadedCSVSerializer(serializers.Serializer):
    file = serializers.FileField()

    def save(self, user):
        csv_object = UploadedCSV.objects.create(csv_file=self.validated_data['file'], uploaded_from=user)
        return csv_object

    @staticmethod
    def check_extension(filename):
        _, file_extension = os.path.splitext(filename)
        if file_extension != '.csv':
            raise serializers.ValidationError({'File extension': 'Only CSV files are accepted'})
        return True


class Car_OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car_Owner
        fields = ['owner_id', 'first_name', 'last_name', 'birthdate', 'country',
                'city', 'street', 'street_number', 'postal_code', 'bonus_points']


class Periodic_billSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodic_bill
        fields = ['periodic_bill_id', 'paid', 'published_on', 'total', 'discount']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['session_id', 'session_id_given', 'car', 'car_owner', 'charging_point',
                'station', 'periodic_bill', 'connection_time', 'disconnection_time',
                'done_charging_time', 'kWh_delivered', 'timezone', 'protocol', 'user_Wh_per_mile',
                'user_kWh_requested', 'user_miles_requested', 'user_minutes_available',
                'user_modified_at', 'user_payment_method', 'user_payment_required',
                'user_requested_departure', 'charge_program', 'provider']

    def save(self, car_owner=None):

        periodic_bill = None

        if ('periodic_bill' not in self.validated_data or self.validated_data['periodic_bill'] != None) and car_owner != None:
            if len(Periodic_bill.objects.filter(owner=car_owner, paid=False)) == 0:
                periodic_bill = Periodic_bill.objects.create(owner=car_owner)
            else:
                periodic_bill = Periodic_bill.objects.filter(owner=car_owner, paid=False)

        try:
            session = Session.objects.create(
                car=self.validated_data['car'],
                car_owner=self.validated_data['car_owner'],
                charging_point=self.validated_data['charging_point'] if 'charging_point' in self.validated_data else None,
                station=self.validated_data['station'] if 'station' in self.validated_data else None,
                periodic_bill=self.validated_data['periodic_bill'] if 'periodic_bill' in self.validated_data else periodic_bill,
                charge_program=self.validated_data['charge_program'] if 'charge_program' in self.validated_data else None,
                provider=self.validated_data['provider'] if 'provider' in self.validated_data else None,
                connection_time=self.validated_data['connection_time'] if 'connection_time' in self.validated_data else None,
                disconnection_time=self.validated_data['disconnection_time'] if 'disconnection_time' in self.validated_data else None,
                done_charging_time=self.validated_data['done_charging_time'] if 'done_charging_time' in self.validated_data else None,
                kWh_delivered=self.validated_data['kWh_delivered'] if 'kWh_delivered' in self.validated_data else None,
                timezone=self.validated_data['timezone'] if 'timezone' in self.validated_data else None,
                protocol=self.validated_data['protocol'] if 'protocol' in self.validated_data else None,
                user_Wh_per_mile=self.validated_data['user_Wh_per_mile'] if 'user_Wh_per_mile' in self.validated_data else None,
                user_kWh_requested=self.validated_data['user_kWh_requested'] if 'user_kWh_requested' in self.validated_data else None,
                user_miles_requested=self.validated_data['user_miles_requested'] if 'user_miles_requested' in self.validated_data else None,
                user_minutes_available=self.validated_data['user_minutes_available'] if 'user_minutes_available' in self.validated_data else None,
                user_modified_at=self.validated_data['user_modified_at'] if 'user_modified_at' in self.validated_data else None,
                user_payment_method=self.validated_data['user_payment_method'] if 'user_payment_method' in self.validated_data else None,
                user_payment_required=self.validated_data['user_payment_required'] if 'user_payment_required' in self.validated_data else None,
                user_requested_departure=self.validated_data['user_requested_departure'] if 'user_requested_departure' in self.validated_data else None
            )
        except:
            session = None

        return session


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['station_id', 'country', 'city', 'street', 'street_number', 'postal_code', 'phone_number', 'email']


class Charging_pointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charging_point
        fields = ['charging_point_id', 'charging_point_id_given']


class Charge_programSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge_program
        fields = ['charge_program_id', 'price', 'duration', 'description']


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['provider_id', 'provider_id_given', 'title', 'website_url', 'comments', 'primary_phone', 'secondary_phone', 'address_info', 'email']



class Car_OwnerChangeCredentialsFrontend(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=63, default='test@gmail.com')

    class Meta:
        model = Car_Owner
        fields = ['first_name', 'last_name', 'birthdate',
                'country', 'city', 'street', 'street_number', 'postal_code', 'email']

    def save(self, car_owner=None, user=None):

        try:

            if 'first_name' in self.validated_data:
                car_owner.first_name = self.validated_data['first_name']
            if 'last_name' in self.validated_data:
                car_owner.last_name = self.validated_data['last_name']
            if 'birthdate' in self.validated_data:
                car_owner.birthdate = self.validated_data['birthdate']
            if 'country' in self.validated_data:
                car_owner.country = self.validated_data['country']
            if 'city' in self.validated_data:
                car_owner.city = self.validated_data['city']
            if 'street' in self.validated_data:
                car_owner.street = self.validated_data['street']
            if 'street_number' in self.validated_data:
                car_owner.street_number = self.validated_data['street_number']
            if 'postal_code' in self.validated_data:
                car_owner.postal_code = self.validated_data['postal_code']
            if user != None and 'email' in self.validated_data:
                print("HOLAAAA USER", user)
                print(self.validated_data['email'])
                user.email = self.validated_data['email']
                user.save()
                print(user.email)

            car_owner.save()

        except:
            car_owner = None

        return car_owner
