import json

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Sum
from django.core.exceptions import ObjectDoesNotExist

from products.models        import (
    Product, 
    MainCategory, 
    SubCategory,
    Scent
)

class ProductView(View):
    def get(self, request):
        try:
            main_category = request.GET.get('main-category')
            best_seller   = request.GET.get('best-seller')
            sub_category  = request.GET.get('sub-category')
            scent         = request.GET.get('scent')

            if main_category:
                main_category  = MainCategory.objects.get(id=main_category)
                sub_categories = main_category.subcategory_set.all()
                for sub_category in sub_categories:
                    product_list = sub_category.product_set.all()
                    products     = [product for product in product_list]
            
            elif best_seller:
                quantity = int(best_seller)
                products = Product.objects.annotate(quantity_sum=Sum('orderitem__quantity')).order_by('-quantity_sum')[:quantity]
            
            elif sub_category:
                sub_category = SubCategory.objects.get(id=sub_category)
                product_list = sub_category.product_set.all()
                products     = [product for product in product_list]

            elif scent:
                scent    = Scent.objects.get(id=scent)
                products = [product for product in scent.product.all()]                

            else:   
                products = Product.objects.all()

            result = [{
                    'id'          : product.id,
                    'name'        : product.name,
                    'collection'  : product.collection.name,
                    'size_g'      : product.size_g,
                    'size_ml'     : product.size_ml,
                    'size_oz'     : product.size_oz,
                    'price'       : product.price,
                    'description' : product.description,
                    'image'       : product.productimage_set.get(is_thumbnail=True).image_url
                } for product in products]
            return JsonResponse({'result': result}, status=200)

        except ObjectDoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_NOT_FOUND'}, status=404)
        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class ProductDetailView(View):
    def get(self, request):
        try:
            product = Product.objects.get(id=request.GET.get('id'))
            images  = [product_image.image_url for product_image in product.productimage_set.order_by('-is_thumbnail').all()]
            scent   = [scent.description for scent in product.scent_set.all()]

            result = {
                    'id'                 : product.id,
                    'name'               : product.name,
                    'collection'         : product.collection.name,
                    'size_g'             : product.size_g,
                    'size_ml'            : product.size_ml,
                    'size_oz'            : product.size_oz,
                    'price'              : product.price,
                    'detail_description' : product.detail_description,
                    'scent_description'  : scent,
                    'ingredient'         : product.ingredient,
                    'image'              : images
                }
            return JsonResponse({'result': result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'message' : 'PRODUCT_NOT_FOUND'}, status=404)
        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)