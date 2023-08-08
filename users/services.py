from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from django.shortcuts import render

from users.models import User


class MobileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        instance = User.objects.get(mobile=username)
        if not instance:
            return render(request, 'login.html', {'loginerror': 'password or username invalid .'})
        if instance.check_password(password):
            return instance
