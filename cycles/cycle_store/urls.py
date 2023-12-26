from django.urls import path,include
from . import views

urlpatterns =[
    path('', views.home ,name='home'),
    path('login/', views.user_login ,name='user_login'),
    path('signup/otp_verification/', views.otp_verification, name='otp_verification'),
    path('signup/', views.signup,name='signup'),
    path('contact/', views.contact ,name='contact'),                 
    path('shop/', include('shop.urls'), name='shop'),
    path('logout/', views.custom_logout ,name='logout'),
    path('forgotpassword/', views.forgotPassword ,name='forgotPassword'),
    path('forgotpassword/pas_otp_verification', views.pass_otp_verification ,name='pass_otp_verification'),
    path('set_newpassword/', views.set_newpassword ,name='set_newpassword'),



]