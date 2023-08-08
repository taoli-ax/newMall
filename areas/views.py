import json
import re

from django.http import HttpRequest, JsonResponse, HttpResponseForbidden
from django.shortcuts import render
import memcache
# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page

from areas.models import Area
from users.models import Address


class AreaView(View):
    @method_decorator(cache_page(timeout=60 * 60 * 2, cache='memcached'))
    def get(self, request: HttpRequest):
        # 提取 area_id
        print('areas coming....')
        area_id = request.GET.get('area_id')
        # 判断 area_id是否存在
        # 没有 ，取省，有，取市/区
        if not area_id:
            province_list = []
            try:
                province = Area.objects.filter(parent__isnull=True)
                for p in province:
                    province_list.append({'id': p.id, 'name': p.name})
            except Exception as e:
                print('something happen:', e)
            return JsonResponse({'code': '0', 'msg': 'OK', 'province_list': province_list})
        else:
            try:
                area = Area.objects.get(id=area_id)
                subs = area.subs.all()
                subs_obj = [{'id': sub.id, 'name': sub.name} for sub in subs]
                response_obj = {'id': area.id, 'name': area.name, 'subs': subs_obj}
            except Exception as e:
                print('something happen:', e)
            return JsonResponse({'code': '0', 'msg': 'OK', 'sub_data': response_obj})



