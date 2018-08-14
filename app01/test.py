from django.shortcuts import render, HttpResponse
from api import models


def index(request):
    # -- a.查看所有学位课并打印学位课名称以及授课老师

    # obj = models.DegreeCourse.objects.all()
    # for item in obj:
    #     print(item.name, item.teachers.first().name)

    # -- b.查看所有学位课并打印学位课名称以及学位课的奖学金

    # obj = models.DegreeCourse.objects.all()
    # for item in obj:
    #     for p in item.degreecourse_price_policy.all():
    #         print(item.name, p.price)

    # -- c.展示所有的专题课

    # obj = models.Course.objects.filter(degree_course__isnull=True)
    # for i in obj:
    #     print(i)

    # -- d.查看id = 1
    # 的学位课对应的所有模块名称

    # obj = models.Course.objects.filter(degree_course__isnull=False, id=1)
    # for item in obj:
    #     print(item.name)

    # -- e.获取id = 1的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses

    # obj = models.Course.objects.filter(id=1)
    # for item in obj:
    #
    #     print(
    #         item.name,
    #         item.get_level_display(),
    #         item.coursedetail.why_study,
    #         item.coursedetail.what_to_study_brief,
    #         item.coursedetail.recommend_courses.first().name,
    #     )

    # -- f.获取id = 1
    # 的专题课，并打印该课程相关的所有常见问题

    # obj = models.Course.objects.filter(id=1)
    # for item in obj:
    #     for i in item.asked_question.all():
    #         print(i.question)

    # -- g.获取id = 1
    # 的专题课，并打印该课程相关的课程大纲

    # obj = models.Course.objects.filter(id=1)
    # for item in obj:
    #     print(item.coursedetail.courseoutline_set.first().title)

    # -- h.获取id = 1
    # 的专题课，并打印该课程相关的所有章节

    # obj = models.Course.objects.filter(id=1)
    # for item in obj:
    #     print(item.coursechapters.first().name)

    # -- i.获取id = 1
    # 的专题课，并打印该课程相关的所有课时
    # 第1章·Python
    # 介绍、基础语法、流程控制
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）

    # obj = models.Course.objects.filter(id=1)
    # for item in obj:
    #     print(
    #         item.coursechapters.first().name,
    #         item.coursechapters.first().chapter,
    #         item.coursechapters.first().summary,
    #           )

    # -- 第1章·Python
    # 介绍、基础语法、流程控制
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # 01 - 课程介绍（一）
    # i.获取id = 1
    # 的专题课，并打印该课程相关的所有的价格策略

    # obj = models.Course.objects.filter(id=1)
    # for item in obj:
    #     for p in item.price_policy.all():
    #         print(p.price, p.valid_period)

    obj = models.Account.objects.filter(id=1)
    print(obj.couponrecord.number)



    return HttpResponse('ok')