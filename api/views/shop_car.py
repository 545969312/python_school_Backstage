from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from rest_framework.pagination import PageNumberPagination
from api.api_serializers import CourseSerializerC
from api.utils.response import BaseResponse
from api import models


class ShopCar(ViewSetMixin, APIView):

    def list(self, request, *args, **kwargs):

        ret = BaseResponse()
        try:
            # 从数据库获取数据
            queryset = models.Course.objects.all()

            # 分页
            # page = PageNumberPagination()
            # course_list = page.paginate_queryset(queryset, request, self)

            # 分页之后的结果执行序列化
            ser = CourseSerializerC(instance=queryset, many=True)

            ret.data = ser.data
        except Exception as e:
            ret.code = 0
            ret.error = '获取数据失败'

        return Response(ret.dict)

    def create(self, request, *args, **kwargs):
        shop_car = {
            'user': {
                'course_id': '',
                'course_name': '',
                'price_policy': {
                    'course_valid_period': '',
                    'course_price': ''
                },
            }
        }
        res = request.POST

        shop_car['user']['course_id'] = res.get('id')
        shop_car['user']['course_name'] = res.get('name')

        print(shop_car)
        return Response('ok')

    def retrieve(self, request, pk, *args, **kwargs):
        response = {'code': 1000, 'data': None, 'error': None}
        try:
            course = models.Course.objects.get(id=pk)
            ser = CourseSerializerC(instance=course)
            response['data'] = ser.data
        except Exception as e:
            response['code'] = 500
            response['error'] = '获取数据失败'

    def update(self,request, pk, *args, **kwargs):
        """
        修改
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def destroy(self, request, pk, *args, **kwargs):
        """
        删除
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """

