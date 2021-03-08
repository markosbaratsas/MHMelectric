import os
from rest_framework import serializers

from rest_api.models import Car_Owner, Car, Periodic_bill, Session, UploadedCSV

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
