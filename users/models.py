from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel):
    user_id  = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=200)
    name     = models.CharField(max_length=50)
    mobile   = models.CharField(max_length=20)
    email    = models.EmailField(max_length=100, unique=True)
    birthday = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'users'

class UserAddress(TimeStampModel):
    zipcode = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    user    = models.ForeignKey('User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'user_addresses'