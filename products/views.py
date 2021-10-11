from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Sum, Q
from django.core.exceptions import ObjectDoesNotExist

from products.models        import Product

class ProductView(View):
    def get(self, request):
        try:
            main_category = request.GET.get('main-category')
            best_seller   = request.GET.get('best-seller')
            sub_category  = request.GET.get('sub-category')
            scent         = request.GET.get('scent')
            keyword       = request.GET.get('keyword')
            
            if main_category:
                products = Product.objects.filter(Q(sub_category__main_category__id=main_category))
            
            if best_seller:
                quantity = int(best_seller)
                products = Product.objects.annotate(quantity_sum=Sum('orderitem__quantity')).order_by('-quantity_sum')[:quantity]
            
            if sub_category:
                products = Product.objects.filter(Q(sub_category__id=sub_category))
 
            if scent:
                products = Product.objects.filter(Q(scent__id=scent))

            if keyword:
                products = Product.objects.filter(Q(name__icontains=keyword)|Q(collection__name__icontains=keyword))

            if not (main_category or best_seller or sub_category or scent or keyword):
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