from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.products, name='products'),
    path('add_element', views.add_element, name='add_element'),
    path('add', views.add_product ,name='add'),
    path('edit_element/<int:id>/', views.edit_element, name='edit_element'),
    path('update/<str:id>', views.update ,name='update'),
    path('list/<int:id>/', views.list, name='list'),
    path('unlist/<int:id>/', views.unlist, name='unlist'),
    path('search/',views.search,name='search'),
    # varient
    path('varient/<int:id>/', views.varient ,name='varient'),
    path('varient/<int:id>/', views.varient ,name='add_varient'),
    path('edit_varient/<int:varient_id>/', views.edit_varient ,name='edit_varient'),
    path('update_varient/<int:id>/', views.update_varient ,name='update_varient'),
    path('delete_varient/<int:varient_id>/', views.delete_varient ,name='delete_varient'),




# category
    path('category', views.category, name='category'),
    path('category/add/', views.category_add,name='category_add'),
    path('category/edit/', views.category_edit ,name='category_edit'),
    path('category/update/<str:id>', views.category_update ,name='category_update'),
    path('category/delete/<int:id>/', views.category_delete, name='category_delete'),
    path('category/undelete/<int:id>/', views.category_undelete, name='category_undelete'),  
    path('category/search/', views.category_search, name='category_search'),

# brand
    path('brand', views.brand, name='brand'),
    path('brand/add/', views.brand_add,name='brand_add'),
    path('brand/edit/', views.brand_edit ,name='brand_edit'),
    path('brand/update/<str:id>', views.brand_update ,name='brand_update'),
    path('brand/delete/<int:id>/', views.brand_delete, name='brand_delete'),
    path('brand/undelete/<int:id>/', views.brand_undelete, name='brand_undelete'),  
    path('brand/search/',views.brand_search,name='brand_search'),


# order
    path('order/', views.order, name='order'),
    path('order/<int:item_id>/',views.order, name='order'),

# coupons
    path('coupon/', views.coupon, name='coupon'),
    path('delete_coupon/<int:coupon_id>/',views.delete_coupon, name='delete_coupon'),    
    path('edit_coupon/<int:coupon_id>/',views.edit_coupon, name='edit_coupon'),

# offers
    path('offers/', views.offers, name='offers'),
    path('delete_offer/<int:offer_id>/',views.delete_offer, name='delete_offer'),    
    path('edit_offer/<int:offer_id>/',views.edit_offer, name='edit_offer'),      



]