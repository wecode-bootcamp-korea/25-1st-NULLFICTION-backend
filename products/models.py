from django.db   import models

from core.models import TimeStampModel


class Product(TimeStampModel):
    name               = models.CharField(max_length=100)
    size_g             = models.CharField(max_length=50)
    size_ml            = models.CharField(max_length=50)
    size_oz            = models.CharField(max_length=50)
    price              = models.IntegerField()
    description        = models.TextField()
    detail_description = models.TextField()
    ingredient         = models.TextField()
    sub_category       = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    collection         = models.ForeignKey('Collection', on_delete=models.CASCADE)
    is_deleted         = models.BooleanField(default=False)

    class Meta:
        db_table = 'products'

class MainCategory(TimeStampModel):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'main_categories'

class SubCategory(TimeStampModel):
    name          = models.CharField(max_length=50)
    main_category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

class Collection(TimeStampModel):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'collections'

class Scent(TimeStampModel):
    name        = models.CharField(max_length=50)
    description = models.TextField()
    product     = models.ManyToManyField('Product', through='ProductScent')

    class Meta:
        db_table = 'scents'

class ProductScent(TimeStampModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    scent   = models.ForeignKey('Scent', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_scents'

class ProductImage(TimeStampModel):
    image_url    = models.URLField()
    is_thumbnail = models.BooleanField(default=False)
    product      = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_images'