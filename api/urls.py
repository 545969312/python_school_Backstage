from django.conf.urls import url
from api.views import course, course_detail, query_all, shop_car, index, login, settlement

urlpatterns = [
    url(r'login/$', login.Login.as_view({'post': 'login'})),

    url(r'course/$', course.Course.as_view()),
    url(r'index/$', index.index),

    url(r'course_detail/$', course_detail.CourseDetail.as_view()),
    url(r'query_all/(?P<condition>\w+)/', query_all.QueryAll.as_view()),

    url(r'shop_car/$', shop_car.ShopCar.as_view({'get': 'list',
                                                 'post': 'create',
                                                 'put': 'update',
                                                 'delete': 'destroy'
                                                 })),

    url(r'settlement/$', settlement.Settlement.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),
]

