from rest_framework import serializers

from rest_api.models import Car

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['car_id_given', 'brand', 'car_type', 'car_model', 
                'release_year', 'variant', 'usable_battery_size']