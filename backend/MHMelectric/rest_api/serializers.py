import os
from rest_framework import serializers

from rest_api.models import Car_Owner, Car, Charging_point, Station, Periodic_bill, Charge_program, Session, UploadedCSV

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['car_id_given', 'brand', 'car_type', 'car_model', 
                'release_year', 'variant', 'usable_battery_size']


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
        fields = ['first_name', 'last_name', 'birthdate', 'country',
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

    # def validate(self, data):
    #     # try:
    #     print("hello")
    #     if data['charging_point'] != None:
    #         print(data['charging_point'].charging_point_id_given)
    #         Charging_point.objects.get(charging_point_id=int(data['charging_point']))
    #     # except:
    #     #     raise serializers.ValidationError("Charging Point Id is not valid.")
    #     try:
    #         if data['station'] != None:
    #             Station.objects.get(charging_point_id=int(data['station']))
    #     except:
    #         raise serializers.ValidationError("Station Id is not valid.")
    #     try:
    #         if data['periodic_bill'] != None:
    #             Periodic_bill.objects.get(charging_point_id=int(data['periodic_bill']))
    #     except:
    #         raise serializers.ValidationError("Periodic Bill Id is not valid.")
    #     try:
    #         if data['charge_program'] != None:
    #             Charge_program.objects.get(charging_point_id=int(data['charge_program']))
    #     except:
    #         raise serializers.ValidationError("Charge Program Id is not valid.")
    #     try:
    #         if data['provider'] != None:
    #             Provider.objects.get(provider_id=int(data['provider']))
    #     except:
    #         raise serializers.ValidationError("Provider Id is not valid.")

    #     return data

    def save(self):

        session = Session.objects.create(
            car=self.validated_data['car'],
            car_owner=self.validated_data['car_owner'],
            charging_point=self.validated_data['charging_point'] if 'charging_point' in self.validated_data else None,
            station=self.validated_data['station'] if 'station' in self.validated_data else None,
            periodic_bill=self.validated_data['periodic_bill'] if 'periodic_bill' in self.validated_data else None,
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

        # except:
        #     session = None

        return session
