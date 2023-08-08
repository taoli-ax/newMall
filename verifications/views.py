import random
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views import View
from woniu.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from redis import Redis
from woniu.libs.yuntongxun.sms import CCP

from celery_tasks.sms.tasks import send_sms_code


class ImageCodeView(View):
    def get(self, request: HttpRequest, uuid):
        print('ImageCodeView: ', uuid)
        code, code_text, code_image = captcha.generate_captcha()
        # 获取redis数据库,存入uuid:code_text
        connection: Redis = get_redis_connection('image_code')
        print('code:', code)
        connection.setex(uuid, 60 * 5, code_text)
        # 返回 code_image
        print('code:', code)
        print('code_text:', code_text)
        return HttpResponse(code_image, content_type='image/jpg')


class SmsCodeView(View):
    def get(self, request: HttpRequest, mobile):
        conn_sms: Redis = get_redis_connection('sms_code')
        sms_flag = conn_sms.get('send_flag_%s' % mobile)
        if sms_flag:
            return JsonResponse({'code': 401, 'errmsg': 'please wait until 5 min later'})
        image_code: str = request.GET.get('image_code')
        uuid = request.GET.get('uuid')

        if not all([image_code, uuid]):
            return JsonResponse({'code': 404, 'errmsg': '缺少必要的参数'})
        # 提取图片验证码
        connection: Redis = get_redis_connection('image_code')
        image_code_redis: bytes = connection.get(uuid)

        if not image_code_redis:
            return JsonResponse({'code': 400, 'errmsg': '图形验证码已失效'})

        # 删除验证码，无论如何，取出来用过就要删，防止客户端猜测
        connection.delete(uuid)

        if image_code.lower() != image_code_redis.decode().lower():
            return JsonResponse({'code': 400, 'errmsg': '验证码错误'})
        # 使用pipline提高redis性能
        pipline = conn_sms.pipeline()
        # 生成随机数当做短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        # 发送前 保存到redis
        pipline.setex(mobile, 60 * 1, sms_code)
        pipline.setex('send_flag_%s' % mobile, 60 * 1, 1)
        pipline.execute()

        # 发送短信验证码，升级为celery 任务
        # result = CCP().send_template_sms('15221342767', [sms_code, 50], 1)
        # print('sms send result:', result)
        send_sms_code.delay(mobile, sms_code)
        # if result != 0:
        #     return JsonResponse({'code': 4001, 'errmsg': 'sms result :%s'%result})

        return JsonResponse({'code': 0, 'msg': '短信验证码发送成功'})
