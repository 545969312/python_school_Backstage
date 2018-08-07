from rest_framework.views import APIView
from rest_framework.response import Response
from api.api_serializers import DegreeCourseSerializerA
from api.api_serializers import DegreeCourseSerializerB
from api.api_serializers import CourseSerializerC
from api.api_serializers import CourseSerializerD
from api.api_serializers import CourseSerializerE
from api.api_serializers import CourseSerializerF
from api.api_serializers import CourseSerializerG
from api.api_serializers import CourseSerializerH
from api import models
from api.utils.response import BaseResponse


class QueryAll(APIView):

    def get(self, request, condition, *args, **kwargs):
        res = BaseResponse()
        try:
            if request.version == 'v1':
                res.version = 'v1'
            else:
                res.version = '其他版本'

            if condition == 'a':
                """
                a.查看所有学位课并打印学位课名称以及授课老师
                """
                degree_obj = models.DegreeCourse.objects.all()
                degree_ser = DegreeCourseSerializerA(degree_obj, many=True)
                res.data = degree_ser.data

            elif condition == 'b':
                """
                b.查看所有学位课并打印学位课名称以及学位课的奖学金
                """
                degree_obj = models.DegreeCourse.objects.all()
                degree_ser = DegreeCourseSerializerB(degree_obj, many=True)
                res.data = degree_ser.data

            elif condition == 'c':
                """
                c.展示所有的专题课
                """
                course_obj = models.Course.objects.filter(degree_course__isnull=True)
                degree_ser = CourseSerializerC(course_obj, many=True)
                res.data = degree_ser.data

            elif condition == 'd':
                """
                d.查看id = 1的学位课对应的所有模块名称
                """
                course_list = models.Course.objects.filter(degree_course_id=1)
                degree_ser = CourseSerializerD(course_list, many=True)
                res.data = degree_ser.data

            elif condition == 'e':
                """
                e.获取id = 1的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、
                所有recommend_courses
                """
                course_list = models.Course.objects.get(id=1)
                degree_ser = CourseSerializerE(course_list)
                res.data = degree_ser.data

            elif condition == 'f':
                """
                f.获取id = 1的专题课，并打印该课程相关的所有常见问题
                """
                course_list = models.Course.objects.get(id=1)
                degree_ser = CourseSerializerF(course_list)
                res.data = degree_ser.data

            elif condition == 'g':
                """
                g.获取id = 1的专题课，并打印该课程相关的课程大纲
                """
                course_list = models.Course.objects.get(id=1)
                degree_ser = CourseSerializerG(course_list)
                res.data = degree_ser.data

            elif condition == 'h':
                """
                h.获取id = 1的专题课，并打印该课程相关的所有章节
                """
                course_list = models.Course.objects.get(id=1)
                degree_ser = CourseSerializerH(course_list)
                res.data = degree_ser.data

        except Exception as e:
            res.error = '获取数据失败'
            res.code = 0
        return Response(res.dict)
