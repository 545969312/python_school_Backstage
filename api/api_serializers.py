from rest_framework import serializers
from rest_framework.validators import ValidationError
from api import models


class CourseSerializer(serializers.ModelSerializer):
    sub_category = serializers.CharField(source='sub_category.name')
    level = serializers.CharField(source='get_level_display')
    course_type = serializers.CharField(source='get_course_type_display')
    price_policy = serializers.SerializerMethodField()
    asked_question = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = '__all__'

    def get_price_policy(self, row):
        price_list = row.price_policy.all()
        return [{'price_policy_id': item.object_id, 'price': item.price, 'valid_period': item.valid_period} for item in
                price_list]

    def get_asked_question(self, row):
        asked_question_list = row.asked_question.all()
        return [{'answer': item.answer, 'question': item.question} for item in asked_question_list]


class CourseDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CourseDetail
        fields = '__all__'


class DegreeCourseSerializerA(serializers.ModelSerializer):

    teachers = serializers.SerializerMethodField() #  manytomany 时要定义方法

    class Meta:
        model = models.DegreeCourse
        fields = '__all__'

    def get_teachers(self, row):
        teachers_list = row.teachers.all()
        return [{'name': item.name} for item in teachers_list]


class DegreeCourseSerializerB(serializers.ModelSerializer):
    degreecourse_price_policy = serializers.SerializerMethodField()

    class Meta:
        model = models.DegreeCourse
        fields = ['name', 'degreecourse_price_policy']

    def get_degreecourse_price_policy(self, row):
        price_list = row.degreecourse_price_policy.all()
        return [{'price': item.price} for item in price_list]


class CourseSerializerC(serializers.ModelSerializer):

    sub_category = serializers.CharField(source='sub_category.name')
    level = serializers.CharField(source='get_level_display')
    course_type = serializers.CharField(source='get_course_type_display')
    price_policy = serializers.SerializerMethodField()
    asked_question = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = '__all__'

    def get_price_policy(self, row):
        price_list = row.price_policy.all()
        return [{'price_policy_id': item.object_id, 'price': item.price, 'valid_period': item.valid_period} for item in price_list]

    def get_asked_question(self, row):
        asked_question_list = row.asked_question.all()
        return [{'answer': item.answer, 'question': item.question} for item in asked_question_list]


class CourseSerializerD(serializers.ModelSerializer):

    class Meta:
        model = models.Course
        fields = '__all__'


class CourseSerializerE(serializers.ModelSerializer):
    level_name = serializers.CharField(source='get_level_display')
    hours = serializers.CharField(source='coursedetail.hours')
    course_slogan = serializers.CharField(source='coursedetail.course_slogan')
    recommend_courses = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['id', 'name', 'level_name', 'hours', 'course_slogan', 'recommend_courses']

    def get_recommend_courses(self,row):
        recommend_list = row.coursedetail.recommend_courses.all()
        return [ {'id': item.id, 'name': item.name} for item in recommend_list]


class CourseSerializerF(serializers.ModelSerializer):

    asked_question = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['name', 'asked_question']

    def get_asked_question(self, row):
        asked_list = row.asked_question.all()
        return [{'question': item.question, 'answer': item.answer} for item in asked_list]


class CourseSerializerG(serializers.ModelSerializer):

    course_outline = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['name', 'course_outline']

    def get_course_outline(self, row):
        course_outline_list = row.coursedetail.courseoutline_set.all()
        return [{'title': item.title, 'content': item.content} for item in course_outline_list]


class CourseSerializerH(serializers.ModelSerializer):

    course_chapter = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['name', 'course_chapter']

    def get_course_chapter(self, row):
        course_chapter_list = row.coursechapters.all()
        return [{'name': item.name, 'chapter': item.chapter} for item in course_chapter_list]













