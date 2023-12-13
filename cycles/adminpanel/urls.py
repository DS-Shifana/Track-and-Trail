from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.adminlogin, name='adminlogin'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<str:filter>/', views.dashboard, name='dashboard_filter'),
    
    
    path('customers/', views.customers, name='customers'),
    path('block_customer/<int:user_id>/', views.block_customer, name='block_customer'),
    path('unblock_customer/<int:id>/', views.unblock_customer, name='unblock_customer'),
    path('search/',views.search,name='search'),
    path('product/', include('product.urls'), name='product'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('report/', views.report, name='report'),


]