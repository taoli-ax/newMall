import json
import re

from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.db import DatabaseError
from django.http import HttpRequest, HttpResponseForbidden, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django_redis import get_redis_connection
from redis import Redis

from .models import User, Address
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request: HttpRequest):
        print(request.POST)
        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        mobile = request.POST.get('phone')
        allow = request.POST.get('allow')
        msg_code = request.POST.get('msg_code')
        pic_code = request.POST.get('pic_code')

        if not all([user_name, pwd, cpwd, mobile, msg_code, allow]):
            return HttpResponseForbidden('hehe')

        if not re.match(r'^[0-9a-zA-Z-_]{5,20}$', user_name):
            return HttpResponseForbidden('length 5 - 20')

        if not re.match(r'^[0-9a-zA-Z-_]{8,20}$', pwd):
            return HttpResponseForbidden('length 8 - 20')

        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseForbidden('phone number not right')

        if not pwd == cpwd:
            return HttpResponseForbidden('password not equal')

        if allow != 'on':
            return HttpResponseForbidden('agree protocol')

        conn: Redis = get_redis_connection('sms_code')
        sms: bytes = conn.get(mobile)
        print('短信验证码redis:', sms)

        if not sms or sms.decode() != msg_code:
            return render(request, 'register.html', context={'error_msg': '验证码错误'})

        try:
            user = User.objects.create_user(username=user_name, password=pwd, mobile=mobile)
        except DatabaseError as e:
            return render(request, 'register.html', context={'error_msg': 'server error'})
        login(request, user)

        # return HttpResponse('register success')
        resp = redirect('/index')
        resp.set_cookie('username', user_name, max_age=3600 * 24 * 7)
        return resp


class UsernameCountView(View):
    def get(self, request, username):
        try:
            count = User.objects.filter(username=username).count()
        except DatabaseError:
            ret = {
                'code': 500,
                'errmsg': 'DB errors',
                'count': 0
            }

        ret = {
            'code': 200,
            'msg': 'success',
            'count': count
        }

        return JsonResponse(ret)


class MobileCountView(View):
    def get(self, request, mobile):
        try:
            count = User.objects.filter(mobile=mobile).count()
        except DatabaseError:
            ret = {
                'code': 500,
                'errmsg': 'DB errors',
                'count': 0
            }

        ret = {
            'code': 200,
            'msg': 'success',
            'count': count
        }

        return JsonResponse(ret)


class LoginView(View):
    def post(self, request: HttpRequest, ):
        # 提取数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        remembered = request.POST.get('remembered')
        # 验证数据 略
        if not any([username, password]):
            return HttpResponseForbidden('password or username is required.')
        # 认证数据
        user = authenticate(username=username, password=password)

        if not user:
            return render(request, 'login.html', {'loginerror': 'invalid password or username.'})
        # 状态保持
        login(request, user)
        if not remembered:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)
        # 返回
        next_url = request.GET.get('next', reverse('contents:index'))  # 如果有next路径参数，则跳转到next所指向的url,否则返回index的url
        resp = redirect(next_url)
        resp.set_cookie('username', username, max_age=3600 * 24 * 7)
        return resp

    def get(self, request):
        return render(request, 'login.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        response = redirect(reverse('contents:index'))
        response.delete_cookie('username')
        return response


class LoginRequiredViewMixin(object):
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(LoginRequiredViewMixin, cls).as_view(*args, **kwargs)
        return login_required(view)


class UserCenterView(LoginRequiredViewMixin, View):
    """
    先调用LoginRequiredViewMixin的as_view
    此时super()就是View
    """

    # 功能上没问题，但每次都要重复写这段代码
    # def as_view(cls, **kwargs):
    #     view = super().as_view(**kwargs)
    #     return login_required(view)

    def get(self, request: HttpRequest):
        # print(request.user.email_activate)
        context = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_activate,
        }
        return render(request, 'user_center_info.html', context=context)


class EmailView(View):
    def put(self, request: HttpRequest):
        if not request.user.is_authenticated:
            return JsonResponse({'code': 401, 'errmsg': 'login required.'})
        data = json.loads(request.body)
        email = data.get('email')
        if not email:
            return JsonResponse({'code': 403, 'errmsg': 'email required'})

        if not re.match(r"^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
            return HttpResponseForbidden('email format invalid.')
        # 修改User表的email字段并保存
        request.user.email = email
        request.user.save()
        return JsonResponse({'code': 201, 'msg': 'success'})


class AddressView(View):
    def get(self, request: HttpRequest):
        print("AddressView:", request.user.default_address_id)
        address_list = Address.objects.filter(user=request.user, is_delete=False)
        address_obj = [{"id": address.id,
                        "title": address.title,
                        "receiver": address.receiver,
                        "province_id": address.province_id,
                        "province": address.province.name,
                        "city_id": address.city_id,
                        "city": address.city.name,
                        "district_id": address.district_id,
                        "district": address.district.name,
                        "mobile": address.mobile,
                        "place": address.place,
                        "tel": address.telephone,
                        "email": address.email}
                       for address in address_list]

        context = {"addresses": address_obj, "user": request.user}

        return render(request, 'user_center_site.html', context=context)

    def post(self, request: HttpRequest):
        # post中数据用在body中,get数据在request.GET中
        print("hello world")

        data_request = json.loads(request.body.decode())
        mobile = data_request.get("mobile")
        place = data_request.get("place")
        province_id = data_request.get("province_id")
        city_id = data_request.get("city_id")
        district_id = data_request.get("district_id")
        receiver = data_request.get("receiver")
        title = data_request.get("title")
        tel = data_request.get("tel")
        email = data_request.get("email")

        if not all([mobile, place, province_id, city_id, district_id, receiver]):
            return JsonResponse({"code": 4101, "errmsg": "缺少必要参数"})

        if not re.match("^1[345789]\d{9}$", mobile):
            return JsonResponse({"code": 4007, "errmsg": 'mobile format invalid.'})
        # if not re.match(r"^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
        #     return JsonResponse({"code": 5001, "errmsg": 'email format invalid.'})
        title = receiver if not title else title
        address = Address.objects.create(
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            mobile=mobile,
            place=place,
            telephone=tel,
            email=email,
            title=title,
            user=request.user
        )
        address.save()
        data = {"code": 0, "msg": "OK", "address": {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province_id": address.province_id,
            "province": address.province.name,
            "city_id": address.city_id,
            "city": address.city.name,
            "district_id": address.district_id,
            "district": address.district.name,
            "mobile": address.mobile,
            "place": address.place,
            "tel": address.telephone,
            "email": address.email,
        }}
        return JsonResponse(data)

    def put(self, request: HttpRequest, address_id):
        print("update data????")
        data_request = json.loads(request.body.decode())
        mobile = data_request.get("mobile")
        place = data_request.get("place")
        province_id = data_request.get("province_id")
        city_id = data_request.get("city_id")
        district_id = data_request.get("district_id")
        receiver = data_request.get("receiver")
        tel = data_request.get("tel")
        email = data_request.get("email")

        if not all([mobile, place, province_id, city_id, district_id, receiver]):
            return JsonResponse({"code": 4101, "errmsg": "缺少必要参数"})

        if not re.match("^1[345789]\d{9}$", mobile):
            return JsonResponse({"code": 4007, "errmsg": 'mobile format invalid.'})
        try:
            Address.objects.filter(id=address_id).update(
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                mobile=mobile,
                place=place,
                telephone=tel,
                email=email
            )
        except Exception as e:
            print("update while %s" % e)

        address = Address.objects.get(id=address_id)
        data = {"code": 0, "msg": "OK", "address": {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province_id": address.province_id,
            "province": address.province.name,
            "city_id": address.city_id,
            "city": address.city.name,
            "district_id": address.district_id,
            "district": address.district.name,
            "mobile": address.mobile,
            "place": address.place,
            "tel": address.telephone,
            "email": address.email,
        }}

        return JsonResponse(data)

    def delete(self, request: HttpRequest, address_id):
        Address.objects.filter(user=request.user, id=address_id).delete()

        return JsonResponse({"code": 0, "msg": "OK"})


class DefaultAddressView(View):
    def put(self, request: HttpRequest, address_id):
        print("address_id", address_id)
        print("hello", request.user.default_address_id)
        request.user.default_address_id = address_id
        request.user.save()
        return JsonResponse({"code": 0, "msg": "OK"})


class AddressTitleView(View):
    def put(self, request: HttpRequest, address_id):
        data = json.loads(request.body.decode())
        Address.objects.filter(id=address_id).update(title=data.get('title'))
        return JsonResponse({"code": 0, "msg": "OK"})


class PasswordView(View):
    def get(self, request: HttpRequest):
        print("走了get")
        return render(request, 'user_center_pass.html', {"error": False})

    def post(self, request: HttpRequest):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            logout(request)
            response = redirect(reverse('users:login'))
            response.delete_cookie("username")
            return response
        else:
            return render(request, 'user_center_pass.html', {
                'error': form.errors
            })
