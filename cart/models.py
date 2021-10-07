from django.db       import models

from users.models    import User
from products.models import Product

class Cart(models.Model):
    quantity   = models.IntegerField()
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    option     = models.ForeignKey('Option', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'carts'

class Option(models.Model):
    name       = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'options'