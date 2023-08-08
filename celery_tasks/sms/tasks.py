import logging

from woniu.libs.yuntongxun.sms import CCP

from celery_tasks.app import app


@app.task()
def send_sms_code(mobile, sms_code):
    result = CCP().send_template_sms(mobile, [sms_code, 50], 1)
    logging.getLogger('django').info('sms_code:'+sms_code)
    return result

