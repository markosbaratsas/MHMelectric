from django.contrib import admin

from rest_api.models import *

admin.site.register(Car_Owner)
admin.site.register(Car)
admin.site.register(dc_charger_port)
admin.site.register(ac_charger_port)
admin.site.register(Operator)
admin.site.register(Charging_point)
admin.site.register(Charge_program)
admin.site.register(Charge_program_Charging_point)
admin.site.register(Connection_type)
admin.site.register(Charging_point_Connection_type)
admin.site.register(Periodic_bill)
admin.site.register(Session)
admin.site.register(UploadedCSV)
