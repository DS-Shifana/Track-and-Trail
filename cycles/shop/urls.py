from django.urls import path,include
from . import views

urlpatterns =[
    
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('category_suggestions/', views.category_suggestions, name='category_suggestions'),



    
]