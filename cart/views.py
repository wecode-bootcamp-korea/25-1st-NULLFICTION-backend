import json
from json.decoder           import JSONDecodeError

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import MultipleObjectsReturned
from django.db              import transaction

from cart.models            import Cart, Option
from products.models        import Product
from users.utils            import login_decorator



class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            user_id     = request.user.id
            product_id  = data['product_id']
            option_id   = data['option_id']
            quantity    = int(data['quantity'])
            
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message':'PRODUCT_NOT_EXIST'}, status=400)
            
            if not Option.objects.filter(id=option_id).exists():
                return JsonResponse({'message':'OPTION_NOT_EXIST'}, status=400)
            if quantity <= 0:
                return JsonResponse({'message':'QUANTITY_ERROR'}, status=400)
            
            cart = Cart.objects.filter(user=user_id, product=product_id, option=option_id).first()

            if Cart.objects.filter(user=user_id, product=product_id, option=option_id).exists():
                cart.quantity += quantity
                cart.save()
            
            else:
                Cart.objects.create(
                    user_id    = user_id,
                    product_id = product_id,
                    option_id  = option_id,
                    quantity   = quantity,
                    )
                
            return JsonResponse({'message': 'CREATE'}, status=201)

        except Cart.DoesNotExist:
            return JsonResponse({'message':'INVALID_CART'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_EEROR'}, status=400)
    
    @login_decorator
    def get(self, request):
        user_id = request.user.id

        if not Cart.objects.filter(user=user_id).exists():
            return JsonResponse({'message':'USER_CART_NOT_EXIST'}, status=400)

        carts  = Cart.objects.filter(user=user_id)
        result = []
        for cart in carts:
            result.append({
                'cart_id'  : cart.id,
                'name'     : cart.product.name,
                'option'   : cart.option.name,
                'image'    : cart.product.productimage_set.get(is_thumbnail=True).image_url,
                'quantity' : cart.quantity,
            })
            
        return JsonResponse({'result': result}, status=200)
    
    @transaction.atomic
    @login_decorator
    def patch(self, request):
        try:
            data     = json.loads(request.body)
            user_id  = request.user.id
            cart_id  = request.GET.get('id')
            quantity = data['quantity']

            if not Cart.objects.filter(id=cart_id, user=user_id).exists():
                return JsonResponse({'message':'INVALID_CART_ID'}, status=404)
            if quantity <= 0:
                return JsonResponse({'message':'QUANTITY_ERROR'}, status=400)

            cart = Cart.objects.get(id=cart_id, user=user_id)
            cart.quantity = data['quantity']
            cart.save()
        
            return JsonResponse({'quantity': cart.quantity}, status=200)

        except MultipleObjectsReturned:
            return JsonResponse({'message':'Multiple_Objects_Returned'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


    @login_decorator
    def delete(self, request):
        try:
            user_id = request.user.id
            cart_id = request.GET.get('id')
            if not Cart.objects.filter(id=cart_id, user=user_id).exists():
                return JsonResponse({'message':'INVALID_CART_ID'}, status=404)

            Cart.objects.get(id=cart_id, user=user_id).delete()
            
            return JsonResponse({'message': 'DELETE'}, status=200)
    
        except MultipleObjectsReturned:
            return JsonResponse({'message':'Multiple_Objects_Returned'}, status=400)