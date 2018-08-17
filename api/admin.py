from django.contrib import admin
from api import models

# Register your models here.
admin.site.register(models.Course)
admin.site.register(models.Teacher)
admin.site.register(models.CourseCategory)
admin.site.register(models.CourseChapter)
admin.site.register(models.CourseOutline)
admin.site.register(models.CourseSection)
admin.site.register(models.CourseDetail)
admin.site.register(models.CourseSubCategory)
admin.site.register(models.DegreeCourse)
admin.site.register(models.Scholarship)
admin.site.register(models.OftenAskedQuestion)
admin.site.register(models.Homework)
admin.site.register(models.PricePolicy)

admin.site.register(models.Coupon)
admin.site.register(models.CouponRecord)
admin.site.register(models.Account)
admin.site.register(models.UserToken)

admin.site.register(models.Article)
admin.site.register(models.ArticleDetail)
admin.site.register(models.ArticleSource)
admin.site.register(models.Collection)
admin.site.register(models.Comment)

admin.site.register(models.EnrolledCourse)
admin.site.register(models.EnrolledDegreeCourse)
admin.site.register(models.ScoreRule)
admin.site.register(models.ScoreRecord)
admin.site.register(models.CourseSchedule)
admin.site.register(models.StudyRecord)
admin.site.register(models.DegreeRegistrationForm)
admin.site.register(models.Order)
admin.site.register(models.OrderDetail)
admin.site.register(models.TransactionRecord)
admin.site.register(models.HomeworkRecord)
admin.site.register(models.StuFollowUpRecord)


