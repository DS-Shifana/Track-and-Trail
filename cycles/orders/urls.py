from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payment/', views.payment ,name='payment'), 

    path('profile/', views.profile ,name='profile'),
    path('edit_profile/', views.edit_profile ,name='edit_profile'),
    path('change_password/', views.change_password ,name='change_password'),

    path('my_address/', views.my_address ,name='my_address'),
    path('add_address/', views.add_address ,name='add_address'),
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('update_address/<int:address_id>/', views.update_address, name='update_address'),
    path('remove_address/<int:address_id>/', views.remove_address, name='remove_address'),

    path('my_orders/', views.my_orders ,name='my_orders'),
    path('order_success/', views.order_success, name='order_success'),
    path('cancel_order/<int:order_item_id>', views.cancel_order ,name='cancel_order'),

    path('wallet/', views.wallet ,name='wallet'),
    path('orderby_wallet/', views.orderby_wallet ,name='orderby_wallet'),


    path('apply_coupon/<int:order_id>', views.apply_coupon, name='apply_coupon'),
    # path('remove_coupon/<int:order_id>', views.cancel_order ,name='cancel_order'),



  
    ]