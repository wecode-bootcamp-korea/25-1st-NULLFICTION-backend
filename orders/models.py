from django.db       import models

from core.models     import TimeStampModel
from users.models    import User
from products.models import Product

class Order(TimeStampModel):
    number       = models.CharField(max_length=100)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class OrderStatus(TimeStampModel):
    status = models.CharField(max_length=100)

    class Meta:
        db_table = 'order_status'

class OrderItem(TimeStampModel):
    quantity          = models.IntegerField(default=0)
    product           = models.ForeignKey(Product, on_delete=models.CASCADE)
    order             = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_item_status = models.ForeignKey('OrderItemStatus',on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_items'

class OrderItemStatus(TimeStampModel):
    status = models.CharField(max_length=100)

    class Meta:
        db_table = 'order_item_status'

class Shipping(TimeStampModel):
    tracking_number = models.CharField(max_length=100)
    date            = models.DateField()
    message         = models.CharField(max_length=100)
    detail          = models.CharField(max_length=200)
    order           = models.ForeignKey('Order', on_delete=models.CASCADE)
    order_item      = models.ManyToManyField('OrderItem', through='ShippingItem')

    class Meta:
        db_table = 'shipping'

class ShippingItem(TimeStampModel):
    shipping   = models.ForeignKey('Shipping', on_delete=models.CASCADE)
    order_item = models.ForeignKey('OrderItem', on_delete=models.CASCADE)

    class Meta:
        db_table = 'shipping_order_items'