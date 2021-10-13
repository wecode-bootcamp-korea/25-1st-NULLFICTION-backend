import json

from django.http           import JsonResponse
from django.views          import View

from cart.models           import Cart, Option
from products.models       import Product
from users.utils           import login_decorator 


class CartsView(View):
    @loginView_decorator
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

            Cart.objects.create(
                user       = request.user,
                product    = product,
                option     = option, 
                quantity   = quantity,
                )
            
            return JsonResponse({'message': 'SUCCESS'}, status=201)
   
        except KeyError:
            return JsonResponse({'message': 'KEY_EEROR'}, status=400)

    @login_decorator
    def get(self, request):
        user       = request.user
        user_carts = Cart.objects.filter(user=user)
        result     = []

        for cart in user_carts:
            result.append({
                'product_name' : cart.product.name,
                'product_option' : cart.option,
                'product_quantity' : cart.
                
            })
