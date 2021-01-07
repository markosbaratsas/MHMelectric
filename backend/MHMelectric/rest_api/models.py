from django.db import models
from django.contrib.auth.models import User

class Car_Owner(models.Model):
    owner_id = models.AutoField(primary_key=True) # this is varchar originally...
    first_name = models.CharField(max_length=63, default='')
    last_name = models.CharField(max_length=63, default='')
    birthdate = models.DateTimeField(auto_now_add=True) # auto_add now = true and we will change it later...
    country = models.CharField(max_length=127, default='')
    city = models.CharField(max_length=127, default='')
    street = models.CharField(max_length=127, default='')
    street_number = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    postal_code = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    bonus_points = models.DecimalField(max_digits=7, decimal_places=0, default=0)
    
    # django provides us with an authentication system which we will use
    # so we don't have username-password here, since it exists on the User model
    # We bind this Car_Owner with a specific User instance using a foreign key
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, default=None, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    car_id_given = models.CharField(max_length=127, default='')
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
    average_consumption = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    owner = models.ForeignKey(Car_Owner, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f'{self.car_id}'


# class Car_Owner_Car(models.Model):
#     Car_Owner_Car_id = models.AutoField(primary_key=True)
#     owner = models.ForeignKey(Car_Owner, on_delete=models.DO_NOTHING)
#     car = models.ForeignKey(Car, on_delete=models.DO_NOTHING)

#     def __str__(self):
#         return str(self.car) + " belongs to " + str(self.owner)


class dc_charger_port(models.Model):
    dc_charger_port_id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING, null=True)
    port = models.CharField(max_length=15, default='')

    def __str__(self):
        return f'DC port {self.port} of car {self.car}'


class ac_charger_port(models.Model):
    ac_charger_port_id = models.AutoField(primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING, null=True)
    port = models.CharField(max_length=15, default='')

    def __str__(self):
        return f'AC port {self.port} of car {self.car}'

class Operator(models.Model):
    operator_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=127, default='')
    website_url = models.CharField(max_length=127, default='')
    comments = models.CharField(max_length=1023, default='')
    primary_phone = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    secondary_phone = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    address_info = models.CharField(max_length=127, default='')
    email = models.EmailField(max_length=63, default='')

    def __str__(self):
        return f'{self.operator_id}'

class Operator(models.Model):
    operator_id = models.AutoField(primary_key=True)
    operator_id_given = models.CharField(max_length=127, default='')
    title = models.CharField(max_length=127, default='')
    website_url = models.CharField(max_length=127, default='')
    comments = models.CharField(max_length=1023, default='')
    primary_phone = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    secondary_phone = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    address_info = models.CharField(max_length=127, default='')
    email = models.EmailField(max_length=63, default='')

    def __str__(self):
        return f'{self.operator_id}'


class Charging_point(models.Model):
    charging_point_id = models.AutoField(primary_key=True)
    charging_point_id_given = models.CharField(max_length=127, default='')
    country = models.CharField(max_length=127, default='')
    city = models.CharField(max_length=127, default='')
    street = models.CharField(max_length=127, default='')
    street_number = models.CharField(max_length=127, default='')
    postal_code = models.DecimalField(max_digits=5, decimal_places=0, default=0)
    phone_number = models.DecimalField(max_digits=34, decimal_places=0, default=0)
    email = models.EmailField(max_length=63, default='')

    operator = models.ForeignKey(Operator, on_delete=models.DO_NOTHING, null=True, default=None)

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
        return f'Charging point {self.charging_point} has charge program {self.charge_program}'


# class Charging_point_Operator(models.Model):
#     charging_point_operator_id = models.AutoField(primary_key=True)
#     operator = models.ForeignKey(Charge_program, on_delete=models.DO_NOTHING)
#     charging_point = models.ForeignKey(Charging_point, on_delete=models.DO_NOTHING)

#     def __str__(self):
#         return f'Operator {self.operator} in charging point {self.charging_point}'


class Connection_type(models.Model):
    connection_type_id = models.AutoField(primary_key=True)
    connection_type = models.CharField(max_length=31, default='')
    general_type = models.CharField(max_length=31, default='')
    voltage = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    amps = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    
    def __str__(self):
        return f'{self.connection_type}'


class Charging_point_Connection_type(models.Model):
    charging_point_connection_type_id = models.AutoField(primary_key=True)
    connection_type = models.ForeignKey(Charge_program, on_delete=models.DO_NOTHING)
    charging_point = models.ForeignKey(Charging_point, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'Connection type {self.connection_type} in charging point {self.charging_point}'


class Periodic_bill(models.Model):
    periodic_bill_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Car_Owner, on_delete=models.DO_NOTHING)
    paid = models.BooleanField(default=False)
    published_on = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.periodic_bill_id}'


class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    session_id_given = models.CharField(max_length=255, default='')
    car = models.ForeignKey(Car, on_delete=models.DO_NOTHING, null=True)
    car_owner = models.ForeignKey(Car_Owner, on_delete=models.DO_NOTHING, null=True)
    charging_point = models.ForeignKey(Charging_point, on_delete=models.DO_NOTHING, null=True)
    periodic_bill = models.ForeignKey(Periodic_bill, on_delete=models.DO_NOTHING, default=None, null=True)
    connection_time = models.DateTimeField(auto_now_add=True)
    disconnection_time = models.DateTimeField(auto_now_add=True) # auto_now_add=True and it will change later
    done_charging_time = models.DateTimeField(auto_now_add=True) # auto_now_add=True and it will change later
    kWh_delivered = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    timezone = models.CharField(max_length=31, default='')
    user_Wh_per_mile = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    user_kWh_requested = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    user_miles_requested = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    user_minutes_available = models.DecimalField(max_digits=4, decimal_places=0, default=0)
    user_modified_at = models.DateTimeField(auto_now_add=True)
    user_payment_method = models.CharField(max_length=63, default='')
    user_payment_required = models.BooleanField(default=True)
    user_requested_departure = models.DateTimeField(auto_now_add=True)

    charge_program = models.ForeignKey(Charge_program, on_delete=models.DO_NOTHING, null=True, default=None)

    def __str__(self):
        return f'{self.session_id}'

class UploadedCSV(models.Model):
    csv_file_id = models.AutoField(primary_key=True)
    csv_file = models.FileField(null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    uploaded_from = models.ForeignKey(User, on_delete=models.DO_NOTHING)
