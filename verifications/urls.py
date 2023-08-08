from django.contrib import admin
from django.urls import path, re_path
from .views import ImageCodeView,SmsCodeView

urlpatterns = [
    re_path(r'image_codes/(?P<uuid>[\w-]+)/', ImageCodeView.as_view(), name='image_code'),
    re_path(r'sms_codes/(?P<mobile>1[3-9]\d{9})/',SmsCodeView.as_view(),name='sms_code'),
]
