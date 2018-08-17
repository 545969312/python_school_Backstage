from django.shortcuts import HttpResponse
from api import models

from django_redis import get_redis_connection
CONN = get_redis_connection("default")

def index(request, *args, **kwargs):
    # 获取用户ID = 1的所有优惠券

    # obj = models.Account.objects.filter(id=1).first()
    # m = obj.couponrecord_set.all()
    # for i in m:
    #     print(i.number)

    # 获取专题课ID = 1且用户ID = 10的所有优惠券

    # obj = models.Course.objects.filter(id=1).first()
    # coupon_obj = obj.coupon.all()
    # for coupon in coupon_obj:
    #     for record_obj in coupon.couponrecord_set.all():
    #         if record_obj.account.id == 10:
    #             print(record_obj.number)

    # 获取用户ID = 10的所有未绑定课程的优惠券
    # obj = models.Account.objects.filter(id=10).first()
    # coupon_obj = obj.couponrecord_set.all()
    # for coupon_ in coupon_obj:
    #     pass

    # 获取用户ID = 1的所有可用优惠券
    # obj = models.Account.objects.filter(id=1).first()
    # coupon_obj = obj.couponrecord_set.all()
    # for cou in coupon_obj:
    #     if cou.status == 0:
    #         print(cou.coupon.brief)

    # user_obj = models.Account.objects.filter(id=1).first()
    # coupon_obj = user_obj.values_list('couponrecord__coupon__brief')
    # print(coupon_obj)
    key = 'settlement_1_%s' % '*'
    list = CONN.keys(key)
    print(CONN.hgetall(*list))


    return HttpResponse('ok')