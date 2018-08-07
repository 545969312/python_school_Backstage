from rest_framework.views import APIView
from rest_framework.response import Response
from api.api_serializers import CourseDetailSerializer
from api import models


class CourseDetail(APIView):
    """
        课程详情API
    """

    def get(self, request):  # 获取课程详情
        res = {'status': 1}
        course_detail = models.CourseDetail.objects.all()
        course_detail_obj = CourseDetailSerializer(course_detail, many=True)  # 序列化文章
        res['data'] = course_detail_obj.data
        return Response(res)
