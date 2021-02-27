import os
from rest_framework import serializers

from rest_api.models import Car_Owner, Car, UploadedCSV

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
