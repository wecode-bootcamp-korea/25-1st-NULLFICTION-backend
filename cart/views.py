import json

from django.http           import JsonResponse
from django.views          import View

from cart.models           import Cart, Option
from products.models       import Product, ProductImage, ProductScent
from users.utils           import login_decorator



class CartsView(View):
    @login_decorator
    def post(self, request):
        try:
            data     = json.loads(request.body)
            user     = request.user,
            product  = Product.objects.get(id = data['product_id'])
            option   = Option.objects.get(id = data['option_id'])
            quantity = int(data['quantity'])
            cart     = Cart.objects.filter(user=user, product=product, option=option).first()
            
            if Cart.objects.filter(user=user, product=product, option=option).exists():
                cart.quantity += quantity
                cart.save()
            
            else:
                Cart.objects.create(
                    user       = user,
                    product    = product,
                    option     = option,
                    quantity   = quantity,
                    )
                
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_EEROR'}, status=400)
    
    @login_decorator
    def get(self, request):
        user  = request.user
        carts = Cart.objects.filter(user=user)
        
        result     = []
        for cart in carts:
            result.append({
                'cart_id'  : cart.id,
                'name'     : cart.product.name,
                'option'   : cart.option.name,
                'image'    : cart.product.productimage_set.filter(is_thumbnail=True).image_url,
                'quantity' : cart.quantity,
            })
        
        return JsonResponse({'result': result}, status=200)

class CartView(View):   
    @login_decorator
    def patch(self, request, cart_id):
        data     = json.loads(request.body)
        cart     = Cart.objects.get(id=cart_id)
        
        cart.quantity = data['quantity']
        cart.save()
    
        return JsonResponse({'message': 'SUCCESS'})

    @login_decorator
    def delete(self, request, cart_id):
        cart = Cart.objects.get(id=cart_id)
        cart.delete()

        return JsonResponse({'message': 'DELETE'})