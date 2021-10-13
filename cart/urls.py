from django.urls import path

from cart.views  import CartView, CartsView

urlpatterns = [
    path('', CartsView.as_view()),
    path('/<int:cart_id>', CartView.as_view())
]