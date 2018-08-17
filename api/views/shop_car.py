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


class ShopCar(ViewSetMixin, APIView):

    authentication_classes = [UserAuthentication, ]

    def list(self, request, *args, **kwargs):

        ret = BaseResponse()

        try:
            # 拿到用户所有购物信息
            pattern = settings.SHOP_CAR % (request.user.id, '*')
            user_shop_list = CONN.keys(pattern)
            print(user_shop_list)
            user_shop_course_list = []
            for key in user_shop_list:

                temp = {
                    'id': CONN.hget(key, 'id').decode('utf-8'),
                    'name': CONN.hget(key, 'name').decode('utf-8'),
                    'img': CONN.hget(key, 'img').decode('utf-8'),
                    'default_price_id': CONN.hget(key, 'default_price_id').decode('utf-8'),
                    'price_policy_dict': json.loads(CONN.hget(key, 'price_policy_dict').decode('utf-8'))
                }

                user_shop_course_list.append(temp)

            ret.data = user_shop_course_list

        except Exception as e:
            ret.code = 0
            ret.error = '获取购物车信息失败'
        return Response(ret.dict)
        # 分页
        # page = PageNumberPagination()
        # course_list = page.paginate_queryset(queryset, request, self)

    def create(self, request, *args, **kwargs):
        ret = BaseResponse()

        res = request.data
        print(res)

        # 1.先验证购买的课程是否存在
        course_id = res.get('id')
        price_policy_id = res.get('price_policy_id')

        course_obj = models.Course.objects.filter(id=course_id).first()
        if not course_obj:
            ret.error = '没有该课程'
            ret.code = 0
            return Response(ret.dict)

        # 2.验证用户所选课程的价格策略合法性
        price_policy_queryset = course_obj.price_policy.all()
        price_policy_dict = {}
        for item in price_policy_queryset:
            temp = {
                'id': item.id,
                'price': item.price,
                'valid_period': item.valid_period,
                'valid_period_display': item.get_valid_period_display()
            }
            price_policy_dict[item.id] = temp
        if price_policy_id not in price_policy_dict:
            return Response({'code': 10002, 'error': '傻×，价格策略别瞎改'})

        # 3. 把商品和价格策略信息放入购物车 SHOPPING_CAR

        # 写进购物车之前先看看购物车里面的容量是否达到了上限
        pattern = settings.SHOP_CAR % (request.user.id, '*')
        keys = CONN.keys(pattern)
        if keys and len(keys) >= 1000:
            ret.code = 0
            ret.error = '购物车已满，请先去支付'
            return Response(ret.dict)

        # 然后添加课程到购物车
        key = settings.SHOP_CAR % (request.user.id, course_id)
        CONN.hset(key, 'id', course_id)
        CONN.hset(key, 'name', course_obj.name)
        CONN.hset(key, 'img', course_obj.course_img)
        CONN.hset(key, 'default_price_id', price_policy_id)
        CONN.hset(key, 'price_policy_dict', json.dumps(price_policy_dict))

        # CONN.expire(key, 20*60)

        return Response('添加到购物车成功')

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
            course_id = request.data.get('id')
            # 价格策略在字典中存在的id应该是str类型的
            price_policy_id = str(request.data.get('price_policy_id'))

            key = settings.SHOP_CAR % (request.user.id, course_id,)

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
            # CONN.expire(key, 20 * 60)
            res.data = '修改成功'
        except Exception as e:
            res.code = 10009
            res.error = '修改失败'

        return Response(res.dict)

    def destroy(self, request, *args, **kwargs):
        """
        删除购物车中的某个课程
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ret = BaseResponse()
        try:
            course_id = request.data.get('id')

            # key = "shopping_car_%s_%s" % (USER_ID,courseid)
            key = settings.SHOP_CAR % (request.user.id, course_id,)
            # shop_list = CONN.keys(pattern)
            CONN.delete(key)
            ret.data = '删除成功'
        except Exception as e:
            ret.code = 10006
            ret.error = '删除失败'
        return Response(ret.dict)

