from django.db   import models

from core.models import TimeStampModel

class User(TimeStampModel):
    username  = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=200)
    name     = models.CharField(max_length=50)
    mobile   = models.CharField(max_length=20)
    email    = models.EmailField(max_length=100, unique=True)
    birthday = models.DateField(null=True, blank=True)
    zipcode = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'users'