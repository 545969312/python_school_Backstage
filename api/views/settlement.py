from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

from api.utils.response import BaseResponse
from api.utils.user_auth import UserAuthentication
from api import models

from django.conf import settings
from api.utils.raise_error import CourseNotExistsException
import datetime
import json
import ast

from django_redis import get_redis_connection

CONN = get_redis_connection("default")


class Settlement(ViewSetMixin, APIView):
    authentication_classes = [UserAuthentication, ]

    def list(self, request, *args, **kwargs):

        ret = BaseResponse()

        try:
            # 1. 根据用户ID去结算中心获取该用户所有要结算课程
            # 2. 根据用户ID去结算中心获取该用户所有可用未绑定课程的优惠券
            pattern = settings.SETTLEMENT % (request.user.id, '*')
            g_pattern = 'global_coupon_%s*' % request.user.id
            user_settlement_list = CONN.keys(pattern)
            user_coupon_list = CONN.keys(g_pattern)

            # 3. 用户表中获取贝里余额
            usable_balance = models.TransactionRecord.objects.get(account_id=request.user.id).balance
            # 4. 以上数据构造成一个字典
            user_settlement_course_dic = {}
            course_detail_dict = {}
            coupon_dict = {}
            dic = {}
            for key in user_settlement_list:
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

                    user_settlement_course_dic['name'] = name
                    user_settlement_course_dic['price'] = price
                    user_settlement_course_dic['valid_period_display'] = valid_period_display

                    dic[id] = user_settlement_course_dic

                # 课程绑定优惠券
                for key, value in coupon_dict.items():
                    coupon_dict[key] = value
                    # print(value)
                    brief = value.get('brief')
                    valid_begin_date = value.get('valid_begin_date')
                    valid_end_date = value.get('valid_end_date')
                    coupon_type = value.get('coupon_type')
                    default_coupon_id = value.get('default_coupon_id')

                    user_settlement_course_dic['brief'] = brief
                    user_settlement_course_dic['brief'] = brief
                    user_settlement_course_dic['valid_begin_date'] = valid_begin_date
                    user_settlement_course_dic['valid_end_date'] = valid_end_date
                    user_settlement_course_dic['coupon_type'] = coupon_type
                    user_settlement_course_dic['default_coupon_id'] = default_coupon_id

                    dic[key] = user_settlement_course_dic
            dic['usable_balance'] = usable_balance
            ret.data = dic

        except Exception as e:
            print(e)
            ret.code = 0
            ret.error = '获取结算信息失败'
        return Response(ret.dict)

    def create(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            user_id = request.user.id
            course_id_list = request.data.get('course_id')

            # 添加之前先清空结算中新的数据
            pattern = settings.SETTLEMENT % (user_id, '*')
            settlement_list = CONN.keys(pattern)

            if settlement_list:
                CONN.delete(*settlement_list)


            # 便利加入结算中新的所有course_id
            course_detail_dict = {}
            coupon_dict = {}
            global_coupon_dict = {}
            coupon_bind_course_dic = {}
            today = datetime.date.today()
            for course_id in course_id_list:

                # 判断购物车中是否存在
                shop_car_key = settings.SHOP_CAR % (user_id, course_id)
                if not CONN.exists(shop_car_key):
                    raise CourseNotExistsException('购物车中不存在该课程')

                # 拿到课程详情
                course_detail = CONN.hgetall(shop_car_key)

                for key, value in course_detail.items():
                    if key == 'price_policy_dict':
                        value = json.loads(value.decode('utf-8'))
                    else:
                        value = value.decode('utf-8')
                    course_detail_dict[key.decode('utf-8')] = value

                # 根据课程id找到课程优惠券
                coupon_list = models.CouponRecord.objects.filter(
                    account_id=user_id,
                    status=0,
                    coupon__valid_begin_date__lte=today,
                    coupon__valid_end_date__gte=today,
                    coupon__object_id=course_id,
                    coupon__content_type__model='course'
                )
                print(coupon_list)
                # 找到用户所有未绑定的优惠券
                global_coupon_list = models.CouponRecord.objects.filter(
                    account_id=user_id,
                    status=0,
                    coupon__valid_begin_date__lte=today,
                    coupon__valid_end_date__gte=today,
                    coupon__content_type__isnull=True
                )
                print(global_coupon_list)
                for coupon_record in coupon_list:
                    temp = {
                        'brief': coupon_record.coupon.brief,
                        'coupon_type': coupon_record.coupon.coupon_type,
                        'money_equivalent_value': coupon_record.coupon.money_equivalent_value,
                        'off_percent': coupon_record.coupon.off_percent,
                        'minimum_consume': coupon_record.coupon.minimum_consume,
                        'valid_begin_date': coupon_record.coupon.valid_begin_date,
                        'valid_end_date': coupon_record.coupon.valid_end_date,
                        'object_id': coupon_record.coupon.object_id,
                        'default_coupon_id': coupon_record.id,
                    }

                    coupon_dict[coupon_record.id] = temp
                for coupon_record in global_coupon_list:

                    temp2 = {
                        'brief': coupon_record.coupon.brief,
                        'coupon_type': coupon_record.coupon.coupon_type,
                        'money_equivalent_value': coupon_record.coupon.money_equivalent_value,
                        'off_percent': coupon_record.coupon.off_percent,
                        'minimum_consume': coupon_record.coupon.minimum_consume,
                        'valid_begin_date': coupon_record.coupon.valid_begin_date,
                        'valid_end_date': coupon_record.coupon.valid_end_date,
                        'default_g_coupon_id': coupon_record.id,
                    }

                    global_coupon_dict[coupon_record.id] = temp2

                # 写入结算redis
                coupon_bind_course_dic['course_detail_dict'] = course_detail_dict
                coupon_bind_course_dic['coupon_dict'] = coupon_dict
                settlement_key = settings.SETTLEMENT % (user_id, course_id)
                global_key = 'global_coupon_%s' % user_id

                CONN.hmset(settlement_key, coupon_bind_course_dic)

                CONN.hmset(global_key, global_coupon_dict)

            ret.data = '加入结算中心成功'
        except Exception as e:
            print(e)
            ret.error = '结算失败'
            ret.code = 10005
        return Response(ret.dict)

    def update(self, request, *args, **kwargs):
        """
        修改用户选中的优惠券
        """
        """
        1. 获取用户提交：user_id course_id
        2. 去结算中心获取当前用户所拥有的绑定当前课程优惠，并进行校验
        3. course_id=0 --> 去结算中心获取当前用户所拥有的未绑定课程优惠，并进行校验
        """
        res = BaseResponse()
        try:
            course_id = request.data.get('course_id')
            coupon_id = request.data.get('coupon_id')
            user_id = request.user.id

            pattern = settings.SETTLEMENT % (request.user.id, '*')
            g_pattern = 'global_coupon_%s*' % request.user.id
            user_settlement_list = CONN.keys(pattern)
            g_coupon_list = CONN.keys(g_pattern)

            course_id_list = []
            coupon_id_list = []
            g_coupon_id_list = []

            for key in user_settlement_list:
                coupon_dict = CONN.hget(key, 'coupon_dict').decode('utf-8')
                coupon_dict = eval(coupon_dict)

                for key, value in coupon_dict.items():
                    coupon_id_list.append(key)
                    course_id_list.append(value.get('object_id'))

            for g_key in g_coupon_list:

                global_coupon_dict = CONN.hgetall(g_key)
                for key in global_coupon_dict:
                    g_coupon_id_list.append(int(key.decode('utf-8')))

            if course_id:

                if (course_id in course_id_list) and (coupon_id in coupon_id_list):

                    res.defaul_coupon_id = coupon_id
                else:
                    res.code = 10001
                    res.error = '该课程没有这个优惠券'
            else:
                if coupon_id not in g_coupon_id_list:
                    res.code = 10001
                    res.error = '无此优惠券'

                else:
                    res.g_defaul_coupon_id = coupon_id
        except Exception as e:
            res.code = 10009
            res.error = '修改失败'

        return Response(res.dict)
