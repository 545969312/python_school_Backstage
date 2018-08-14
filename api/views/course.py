from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from api.api_serializers import CourseSerializer
from api import models


class Course(APIView):
    """
        课程列表API
    """

    def get(self, request, *args, **kwargs):  # 获取课程数据

        res = {'status': 1}
        if request.version == 'v1':
            res['version'] = 'v1'
        else:
            res['version'] = '其他版本'
        course = models.Course.objects.all()
        course_obj = CourseSerializer(course, many=True)  # 序列化文章
        res['data'] = course_obj.data


        return Response(res)
