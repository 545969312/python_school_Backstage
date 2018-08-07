from django.conf.urls import url
from api.views import course, course_detail, query_all

urlpatterns = [
    url(r'course/$', course.Course.as_view()),
    url(r'course_detail/$', course_detail.CourseDetail.as_view()),
    url(r'query_all/(?P<condition>\w+)/', query_all.QueryAll.as_view()),
]

