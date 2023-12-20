from django.urls import path
from . import views


urlpatterns = [
#     Cart
        path('', views.cart ,name='cart'),
        path('add_cart/<int:variant_id>/', views.increment_cartItem ,name='increment_cartItem'),
        path('add_to_cart/<int:variant_id>', views.add_to_cart ,name='add_to_cart'),
        path('decrement/<int:variant_id>/<int:cart_item_id>/', views.decrement_cartItem ,name='decrement_cartItem'),
        path('delete_cart/<int:variant_id>/<int:cart_item_id>/',views.delete_cart, name='delete_cart'),
# Checkout
        path('checkout/', views.checkout ,name='checkout'),

        path('wishlist/',views.wishlist,name='wishlist'),
        path('add_to_wishlist/<int:product_id>/',views.add_to_wishlist,name='add_to_wishlist'),
        path('delete_from_wishlist/<int:product_id>/',views.delete_from_wishlist,name='delete_from_wishlist')


]
