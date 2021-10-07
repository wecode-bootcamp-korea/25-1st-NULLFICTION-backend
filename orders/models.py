from django.db       import models

from users.models    import User
from products.models import Product

class Order(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)
    updated_at   = models.DateTimeField(auto_now=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    order_status_description = models.CharField(max_length=100)
    updated_at               = models.DateTimeField(auto_now=True)
    created_at               = models.DateTimeField(auto_now_add=True)    

    class Meta:
        db_table = 'order_status'

class OrderItem(models.Model):
    quantity          = models.IntegerField()
    product           = models.ForeignKey(Product, on_delete=models.CASCADE)
    order             = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_item_status = models.ForeignKey('OrderItemStatus',on_delete=models.CASCADE)
    updated_at        = models.DateTimeField(auto_now=True)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_items'

class OrderItemStatus(models.Model):
    order_item_status_description = models.CharField(max_length=100)
    updated_at                    = models.DateTimeField(auto_now=True)
    created_at                    = models.DateTimeField(auto_now_add=True)    

    class Meta:
        db_table = 'order_item_status'

class Shipping(models.Model):
    tracking_number  = models.CharField(max_length=100)
    shipping_date    = models.DateField()
    shipping_message = models.CharField(max_length=100)
    shipping_detail  = models.CharField(max_length=200)
    order            = models.ForeignKey('Order', on_delete=models.CASCADE)
    order_item       = models.ManyToManyField('OrderItem', through='ShippingItem')
    updated_at       = models.DateTimeField(auto_now=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shipping'

class ShippingItem(models.Model):
    shipping   = models.ForeignKey('Shipping', on_delete=models.CASCADE)
    order_item = models.ForeignKey('OrderItem', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shipping_items'