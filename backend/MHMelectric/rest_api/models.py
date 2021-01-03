from django.db import models
from django.contrib.auth.models import User

class Car_Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'