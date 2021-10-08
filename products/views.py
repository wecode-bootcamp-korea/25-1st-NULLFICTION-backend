import json

from django.http  import JsonResponse
from django.views import View

from products.models import Product, ProductImage

class ProductView(View):
    def get(self, request):
        try:
            result   = []
            products = Product.objects.all()

            for product in products:
                image = product.productimage_set.get(is_thumbnail=True)
                product_info = {
                    'id'          : product.id,
                    'name'        : product.name,
                    'collection'  : product.collection.name,
                    'size_g'      : product.size_g,
                    'size_ml'     : product.size_ml,
                    'size_oz'     : product.size_oz,
                    'price'       : product.price,
                    'description' : product.description,
                    'image'       : image.image_url
                }
                result.append(product_info)

            return JsonResponse({'result': result}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'})


class Sample(View) :
    def get(self,request) :
        lists = [1,2,4,6]        
        return JsonResponse({"result": list(Product.objects.filter(id__in=lists).values_list())})