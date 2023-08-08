from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from areas.models import Area


class User(AbstractUser):
    """ 自定义 """
    mobile = models.CharField(max_length=11, unique=True, verbose_name='phone number')
    email_activate = models.BooleanField(default=False, verbose_name='email is_activate')
    default_address = models.ForeignKey("Address", related_name="users", on_delete=models.SET_NULL, null=True,
                                        blank=True, verbose_name="default_address")

    class Meta:
        db_table = 'tb_user'
        verbose_name = 'User'

    def __str__(self):
        return self.username


class Address(models.Model):
    title = models.CharField(max_length=30, verbose_name="title")
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    receiver = models.CharField(max_length=20, verbose_name='receiver')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_address',
                                 verbose_name='province_name')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_address',
                             verbose_name='city_name')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_address',
                                 verbose_name='district_name')
    place = models.CharField(max_length=120, verbose_name='specification address')

    mobile = models.CharField(max_length=11, verbose_name='mobile_number')
    telephone = models.CharField(max_length=30, null=True, blank=True, default="", verbose_name="tel")
    email = models.CharField(max_length=30, null=True, blank=True, default="", verbose_name="email")
    is_delete = models.BooleanField(default=False, verbose_name="is delete")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="address", verbose_name="user_address")

    class Meta:
        db_table = "tb_address"
        verbose_name = "address_for_receiver"
        ordering = ["-update_at"]
