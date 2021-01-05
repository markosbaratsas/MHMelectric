from django.db import models
from django.contrib.auth.models import User

class Car_Owner(models.Model):
    owner_id = models.AutoField(primary_key=True) # this is varchar originally...
    first_name = models.CharField(max_length=63, default='')
    last_name = models.CharField(max_length=63, default='')
    birthdate = models.DateTimeField(auto_now_add=True) # auto_add now = true and we will change it later...
    country = models.CharField(max_length=127, default='')
    city = models.CharField(max_length=127, default='')
    street = models.CharField(max_length=31, default='')
    street_number = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    postal_code = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    bonus_points = models.DecimalField(max_digits=7, decimal_places=0, default=0)
    
    # django provides us with an authentication system which we will use
    # so we don't have username-password here, since it exists on the User model
    # We bind this Car_Owner with a specific User instance using a foreign key
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.first_name) + str(self.last_name)
        # return f'{self.user.username}'



class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=63, default='')
    car_type = models.CharField(max_length=15, default='')
    car_model = models.CharField(max_length=31, default='')
    release_year = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    variant = models.CharField(max_length=15, default='')
    usable_battery_size = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    ac_charger_usable_phases = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    ac_charger_max_power = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    dc_charger_max_power = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    energy_average_consumption = models.DecimalField(max_digits=4, decimal_places=1, default=0)

    def __str__(self):
        return f'{self.car_id}'



class Car_Owner_Car(models.Model):
    Car_Owner_Car_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Car_Owner, on_delete=models.DO_NOTHING)
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.car) + " belongs to " + str(self.owner)



class dc_charger_ports(models.Model):
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    port = models.CharField(max_length=15, default='', primary_key=True)

    def __str__(self):
        return "DC port " + str(self.port) + " of car " + str(self.car)



class ac_charger_ports(models.Model):
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    port = models.CharField(max_length=15, default='', primary_key=True)

    def __str__(self):
        return "AC port " + str(self.port) + " of car " + str(self.car)



class Charging_point(models.Model):
    charging_point_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=127, default='')
    city = models.CharField(max_length=127, default='')
    street = models.CharField(max_length=31, default='')
    street_number = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    postal_code = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    phone_number = models.CharField(max_length=31, default='') # why varchar?
    email = models.CharField(max_length=31, default='')

    def __str__(self):
        return f'{self.charging_point_id}'



class Charge_program(models.Model):
    charge_program_id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    duration = models.DecimalField(max_digits=6, decimal_places=0, default=0)
    description = models.CharField(max_length=1023, default='')

    def __str__(self):
        return f'{self.charge_program_id}'



class Charge_program_Charging_point(models.Model):
    charge_program_charging_point_id = models.AutoField(primary_key=True)
    charge_program = models.ForeignKey(Charge_program, on_delete=models.DO_NOTHING)
    charging_point = models.ForeignKey(Charging_point, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Charging point " + str(self.charging_point) + " has charge program " + str(self.charge_program)



class Provider(models.Model):
    provider_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=127, default='')
    website_url = models.CharField(max_length=127, default='')
    comments = models.CharField(max_length=1023, default='')
    primary_phone = models.CharField(max_length=31, default='') # why varchar?
    secondary_phone = models.CharField(max_length=31, default='') # why varchar?
    address_info = models.CharField(max_length=127, default='')
    email = models.CharField(max_length=63, default='')

    def __str__(self):
        return f'{self.provider_id}'



class Charging_point_Provider(models.Model):
    charging_point_provider_id = models.AutoField(primary_key=True)
    provider = models.ForeignKey(Charge_program, on_delete=models.DO_NOTHING)
    charging_point = models.ForeignKey(Charging_point, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Provider " + str(self.provider) + " in charging point " + str(self.charging_point)



class Connection_type(models.Model):
    connection_type_id = models.AutoField(primary_key=True)
    connection_type = models.CharField(max_length=31, default='')
    
    def __str__(self):
        return self.connection_type



class Charging_point_Connection_type(models.Model):
    charging_point_connection_type_id = models.AutoField(primary_key=True)
    connection_type = models.ForeignKey(Charge_program, on_delete=models.DO_NOTHING)
    charging_point = models.ForeignKey(Charging_point, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Connection type " + str(self.connection_type) + " in charging point " + str(self.charging_point)



class Periodic_bill(models.Model):
    periodic_bill_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Car_Owner, on_delete=models.DO_NOTHING)
    paid = models.BooleanField(default=False)
    published_on = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=16, decimal_places=12, default=0)
    discount = models.DecimalField(max_digits=16, decimal_places=12, default=0)

    def __str__(self):
        return f'{self.periodic_bill_id}'



class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)
    car_owner = models.ForeignKey(Car_Owner, on_delete=models.DO_NOTHING)
    charging_point = models.ForeignKey(Charging_point, on_delete=models.DO_NOTHING)
    periodic_bil = models.ForeignKey(Periodic_bill, on_delete=models.DO_NOTHING)
    connection_time = models.DateTimeField(auto_now_add=True)
    disconnection_time = models.DateTimeField(auto_now_add=True)
    done_charging_time = models.DateTimeField(auto_now_add=True)
    kWh_delivered = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    timezone = models.CharField(max_length=31, default='')
    user_Wh_per_mile = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    user_Wh_requested = models.DecimalField(max_digits=5, decimal_places=3, default=0)
    user_miles_requested = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    user_minutes_available = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    user_modified_at = models.DateTimeField(auto_now_add=True)
    user_payment_required = models.BooleanField(default=True)
    user_requested_departure = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.session_id}'