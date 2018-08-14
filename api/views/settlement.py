from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

from api.utils.response import BaseResponse
from api.utils.user_auth import UserAuthentication
from api import models

from django.conf import settings
import json

from django_redis import get_redis_connection
CONN = get_redis_connection("default")


class Settlement(ViewSetMixin, APIView):
    authentication_classes = [UserAuthentication, ]

    def list(self, request, *args, **kwargs):

        ret = BaseResponse()

        try:
            # 拿到用户所有购物信息
            pattern = settings.SETTLEMENT % (request.user.id, '*')
            user_settlement_list = CONN.keys(pattern)
            print(user_settlement_list)
            user_settlement_course_list = []
            for key in user_settlement_list:
                temp = {
                    'id': CONN.hget(key, 'id').decode('utf-8'),
                    'name': CONN.hget(key, 'name').decode('utf-8'),
                    'img': CONN.hget(key, 'img').decode('utf-8'),
                    'default_price_id': CONN.hget(key, 'default_price_id').decode('utf-8'),
                    'price_policy_dict': CONN.hget(key, 'price_policy_dict').decode('utf-8')
                }

                user_settlement_course_list.append(temp)
            ret.data = user_settlement_course_list

        except Exception as e:
            ret.code = 0
            ret.error = '获取购物车信息失败'
        return Response(ret.dict)

    def create(self, request, *args, **kwargs):
        ret = BaseResponse()
        user_id = request.user.id
        res = request.data

        settlement_key = settings.SETTLEMENT % (user_id, '*')
        CONN.delete(settlement_key)

        for course_id in res:

            course_obj = models.Course.objects.filter(id=course_id).first()
            if not course_obj:
                ret.error = '没有该课程'
                ret.code = 0
                return Response(ret.dict)

            shop_car_key = settings.SHOP_CAR % (user_id, course_id)
            settlement_key = settings.SETTLEMENT % (user_id, course_id)

            shop_id = CONN.hget(shop_car_key, 'id').decode('utf-8')
            shop_name = CONN.hget(shop_car_key, 'name').decode('utf-8')
            shop_img = CONN.hget(shop_car_key, 'img').decode('utf-8')
            shop_default_price_id = CONN.hget(shop_car_key, 'default_price_id').decode('utf-8')
            shop_price_policy_dict = CONN.hget(shop_car_key, 'price_policy_dict').decode('utf-8')

            user_obj = models.Account.objects.filter(id=user_id).first()
            coupon_obj = user_obj.couponrecord__coupon.all()


            CONN.hset(settlement_key, 'id', shop_id)
            CONN.hset(settlement_key, 'name', shop_name)
            CONN.hset(settlement_key, 'img', shop_img)
            CONN.hset(settlement_key, 'default_price_id', shop_default_price_id)
            CONN.hset(settlement_key, 'price_policy_dict', shop_price_policy_dict)
        return Response(ret)

    def update(self, request, *args, **kwargs):
        """
        修改用户选中的价格策略
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        """
        1. 获取课程ID、要修改的价格策略ID
        2. 校验合法性（去redis中）
        """
        res = BaseResponse()
        try:
            ret = request.data
            course_id = ret.get('id')
            price_policy_id = ret.get('price_policy_id')

            key = settings.LUFFY_SHOPPING_CAR % (request.user.id, course_id,)

            if not CONN.exists(key):
                res.code = 10007
                res.error = '课程不存在'
                return Response(res.dict)

            price_policy_dict = json.loads(CONN.hget(key, 'price_policy_dict').decode('utf-8'))
            if price_policy_id not in price_policy_dict:
                res.code = 10008
                res.error = '价格策略不存在'
                return Response(res.dict)

            CONN.hset(key, 'default_price_id', price_policy_id)
            CONN.expire(key, 20 * 60)
            res.data = '修改成功'
        except Exception as e:
            res.code = 10009
            res.error = '修改失败'

        return Response(res.dict)