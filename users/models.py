from django.db import models

class User(models.Model):
    user_id    = models.CharField(max_length=20, unique=True)
    password   = models.CharField(max_length=200)
    name       = models.CharField(max_length=50)
    mobile     = models.CharField(max_length=20)
    email      = models.EmailField(max_length=100, unique=True)
    birthday   = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'

class UserAddress(models.Model):
    zipcode    = models.CharField(max_length=20)
    address    = models.CharField(max_length=100)
    user       = models.ForeignKey('User', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_addresses'