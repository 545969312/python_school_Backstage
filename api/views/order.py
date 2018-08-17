from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

from api.utils.response import BaseResponse
from api.utils.user_auth import UserAuthentication
from api import models

from django.conf import settings
from django.db import transaction
from api.utils.raise_error import CourseNotExistsException
import datetime
import json
import ast

from django_redis import get_redis_connection

CONN = get_redis_connection("default")


class Order(ViewSetMixin, APIView):
    authentication_classes = [UserAuthentication, ]

    def list(self, request, *args, **kwargs):
        res = BaseResponse()
        res.data = '查看订单'
        return Response(res)

    def create(self, request, *args, **kwargs):
        res = BaseResponse()
        try:
            # 1.创建订单 接受用户发过来的数据
            # {'balance':1000, 'alipay':228 }
            user_id = request.user.id
            use_balance = request.data.get('balance')  # 用户使用的贝里
            alipay = request.data.get('alipay')  # 应该支付金额

            # 判断用户贝里余额
            if request.user.balance <= use_balance:
                res.code = 10001
                res.error = '贝里余额不足'
                return Response(res.dict)

            # 2.获取结算中心的每个课程信息并应用优惠券

            pattern = settings.SETTLEMENT % (user_id, '*')
            settlement_list = CONN.keys(pattern)
            g_pattern = 'global_coupon_%s*' % request.user.id
            g_coupon_list = CONN.keys(g_pattern)

            # 3. 用户表中获取贝里余额
            totle_price = 0  # 总价格
            discount = 0  # 折扣抵消价

            g_coupon_dict_c = {}
            default_g_coupon_id = None

            for key in settlement_list:
                course_detail_dict = CONN.hget(key, 'course_detail_dict').decode('utf-8')
                coupon_dict = CONN.hget(key, 'coupon_dict').decode('utf-8')

                course_detail_dict = ast.literal_eval(course_detail_dict)
                coupon_dict = eval(coupon_dict)

                # 课程详细详细信息
                for key, value in course_detail_dict.items():
                    name = course_detail_dict.get('name')
                    id = course_detail_dict.get('default_price_id')
                    price_policy_dict = course_detail_dict.get('price_policy_dict')
                    price_policy = json.loads(price_policy_dict).get(id)
                    price = price_policy.get('price')
                    valid_period_display = price_policy.get('valid_period_display')
                totle_price += price

                # 课程绑定优惠券
                for key, value in coupon_dict.items():
                    # print(value)
                    brief = value.get('brief')
                    valid_begin_date = value.get('valid_begin_date')
                    valid_end_date = value.get('valid_end_date')
                    coupon_type = value.get('coupon_type')
                    money_equivalent_value = value.get('money_equivalent_value')
                    off_percent = value.get('off_percent')
                    minimum_consume = value.get('minimum_consume')
                    default_coupon_id = value.get('default_g_coupon_id')

                if default_coupon_id == 0:
                    discount += 0
                else:
                    if coupon_type == 0:
                        discount += price if money_equivalent_value > price else money_equivalent_value
                    elif coupon_type == 1 and price > minimum_consume:
                        discount += price if money_equivalent_value > price else money_equivalent_value
                    elif coupon_type == 2 and off_percent:
                        discount += price*(100-off_percent)/100
            # 未绑定的优惠券
            for key in g_coupon_list:
                g_coupon_dict = CONN.hgetall(key)

                # 获取优惠券id
                for k,v in g_coupon_dict.items():
                    value = eval(v.decode('utf-8'))
                    if type(value) is int:
                        default_g_coupon_id = value
                # 查找对应优惠券
                for ke,va in g_coupon_dict.items():
                    val = eval(va.decode('utf-8'))
                    if type(val) is dict:
                        if val.get('default_g_coupon_id') == default_g_coupon_id:
                            g_money_equivalent_value = val.get('money_equivalent_value')
                            g_coupon_type = val.get('coupon_type')
                            g_brief = val.get('brief')
                            g_off_percent = val.get('off_percent')
                            g_minimum_consume = val.get('minimum_consume')

                if default_coupon_id == 0:
                    discount += 0
                else:
                    if g_coupon_type == 0:
                        discount += price if g_money_equivalent_value > price else g_money_equivalent_value
                    elif g_coupon_type == 1 and price > g_minimum_consume:
                        discount += price if g_money_equivalent_value > price else g_money_equivalent_value
                    elif g_coupon_type == 2 and g_off_percent:
                        discount += price*(100-g_off_percent)/100

            # 判断总价是否合理
            if not alipay == totle_price-discount-use_balance/10:
                res.error = '价格不正确'
                res.code = 10001

            with transaction:
                # 生成订单
                pass

        except Exception as e:
            print(e)
            res.code = 0
            res.error = '获取结算信息失败'

        return Response(res.dict)

    def update(self, request, *args, **kwargs):
        res = BaseResponse()
        res.data = '修改订单'
        return Response(res)

    def destroy(self, request, *args, **kwargs):
        res = BaseResponse()
        res.data = '删除订单'
        return Response(res)
