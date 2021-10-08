import os
import django
import csv
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nullfiction.settings")
django.setup()

from products.models import *

CSV_PATH_PRODUCTS = './products.csv'

with open(CSV_PATH_PRODUCTS) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None )
    for row in data_reader:
        name = row[1]
        size_g = row[2]
        size_ml = row[3]
        size_oz = row[4]
        price = row[5]
        sub = row[6]
        col = row[7]
        desc = row[8]
        ddesc = row[9]
        ingre = row[10]
        de = row[11]

        Product.objects.create(name=name, size_g=size_g, size_ml=size_ml, size_oz=size_oz, price=price, sub_category_id=sub, collection_id=col, description=desc, detail_description=ddesc, ingredient=ingre, is_deleted=de)
