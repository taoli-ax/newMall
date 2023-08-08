from django.contrib import admin
from django.urls import path, re_path
from .views import (
    RegisterView,
    UsernameCountView,
    MobileCountView,
    LoginView,
    LogoutView,
    UserCenterView,
    EmailView,
    AddressView,
    DefaultAddressView,
AddressTitleView,
PasswordView,

)

app_name = 'users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    re_path(r'usernames/(?P<username>[a-zA-Z0-9-_]{5,20})/count/', UsernameCountView.as_view(), name='username_count'),
    re_path(r'mobiles/(?P<mobile>1[3-9]\d{9})/count/', MobileCountView.as_view(), name='mobile_count'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('info/', UserCenterView.as_view(), name='info'),
    path('emails/', EmailView.as_view(), name='email'),
    re_path('^addresses/$', AddressView.as_view(), name='address'),
    re_path(r'^addresses/create/$', AddressView.as_view(), name='create'),
    re_path(r'^addresses/(?P<address_id>\d+)/$', AddressView.as_view(), name='address_update_delete'),
    re_path(r'^addresses/(?P<address_id>\d+)/default/$', DefaultAddressView.as_view(), name='default_address'),
    re_path(r'^addresses/(?P<address_id>\d+)/title/$', AddressTitleView.as_view(), name='address_title'),
    re_path(r'^password/$', PasswordView.as_view(), name='password'),
]
