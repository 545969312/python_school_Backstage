# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-06 09:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('course_img', models.CharField(max_length=255)),
                ('course_type', models.SmallIntegerField(choices=[(0, '付费'), (1, 'VIP专享'), (2, '学位课程')])),
                ('brief', models.TextField(max_length=2048, verbose_name='课程概述')),
                ('level', models.SmallIntegerField(choices=[(0, '初级'), (1, '中级'), (2, '高级')], default=1)),
                ('pub_date', models.DateField(blank=True, null=True, verbose_name='发布日期')),
                ('period', models.PositiveIntegerField(default=7, verbose_name='建议学习周期(days)')),
                ('order', models.IntegerField(help_text='从上一个课程数字往后排', verbose_name='课程顺序')),
                ('attachment_path', models.CharField(blank=True, max_length=128, null=True, verbose_name='课件路径')),
                ('status', models.SmallIntegerField(choices=[(0, '上线'), (1, '下线'), (2, '预上线')], default=0)),
                ('template_id', models.SmallIntegerField(default=1, verbose_name='前端模板id')),
            ],
            options={
                'verbose_name_plural': '06.专题课或学位课模块',
            },
        ),
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
            options={
                'verbose_name_plural': '01.课程大类',
            },
        ),
        migrations.CreateModel(
            name='CourseChapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.SmallIntegerField(default=1, verbose_name='第几章')),
                ('name', models.CharField(max_length=128)),
                ('summary', models.TextField(blank=True, null=True, verbose_name='章节介绍')),
                ('pub_date', models.DateField(auto_now_add=True, verbose_name='发布日期')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coursechapters', to='api.Course')),
            ],
            options={
                'verbose_name_plural': '10. 课程章节',
            },
        ),
        migrations.CreateModel(
            name='CourseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.IntegerField(verbose_name='课时')),
                ('course_slogan', models.CharField(blank=True, max_length=125, null=True)),
                ('video_brief_link', models.CharField(blank=True, max_length=255, null=True, verbose_name='课程介绍')),
                ('why_study', models.TextField(verbose_name='为什么学习这门课程')),
                ('what_to_study_brief', models.TextField(verbose_name='我将学到哪些内容')),
                ('career_improvement', models.TextField(verbose_name='此项目如何有助于我的职业生涯')),
                ('prerequisite', models.TextField(max_length=1024, verbose_name='课程先修要求')),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Course')),
                ('recommend_courses', models.ManyToManyField(blank=True, related_name='recommend_by', to='api.Course')),
            ],
            options={
                'verbose_name_plural': '07.课程或学位模块详细',
            },
        ),
        migrations.CreateModel(
            name='CourseOutline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('order', models.PositiveSmallIntegerField(default=1)),
                ('content', models.TextField(max_length=2048, verbose_name='内容')),
                ('course_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.CourseDetail')),
            ],
            options={
                'verbose_name_plural': '09. 课程大纲',
            },
        ),
        migrations.CreateModel(
            name='CourseSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('order', models.PositiveSmallIntegerField(help_text='建议每个课时之间空1至2个值，以备后续插入课时', verbose_name='课时排序')),
                ('section_type', models.SmallIntegerField(choices=[(0, '文档'), (1, '练习'), (2, '视频')], default=2)),
                ('section_link', models.CharField(blank=True, help_text='若是video，填vid,若是文档，填link', max_length=255, null=True)),
                ('video_time', models.CharField(blank=True, max_length=32, null=True, verbose_name='视频时长')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('free_trail', models.BooleanField(default=False, verbose_name='是否可试看')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coursesections', to='api.CourseChapter')),
            ],
            options={
                'verbose_name_plural': '11. 课时',
            },
        ),
        migrations.CreateModel(
            name='CourseSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.CourseCategory')),
            ],
            options={
                'verbose_name_plural': '02.课程子类',
            },
        ),
        migrations.CreateModel(
            name='DegreeCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('course_img', models.CharField(max_length=255, verbose_name='缩略图')),
                ('brief', models.TextField(verbose_name='学位课程简介')),
                ('total_scholarship', models.PositiveIntegerField(default=40000, verbose_name='总奖学金(贝里)')),
                ('mentor_compensation_bonus', models.PositiveIntegerField(default=15000, verbose_name='本课程的导师辅导费用(贝里)')),
                ('period', models.PositiveIntegerField(default=150, verbose_name='建议学习周期(days)')),
                ('prerequisite', models.TextField(max_length=1024, verbose_name='课程先修要求')),
            ],
            options={
                'verbose_name_plural': '03.学位课',
            },
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='作业题目')),
                ('order', models.PositiveSmallIntegerField(help_text='同一课程的每个作业之前的order值间隔1-2个数', verbose_name='作业顺序')),
                ('homework_type', models.SmallIntegerField(choices=[(0, '作业'), (1, '模块通关考核')], default=0)),
                ('requirement', models.TextField(max_length=1024, verbose_name='作业需求')),
                ('threshold', models.TextField(max_length=1024, verbose_name='踩分点')),
                ('recommend_period', models.PositiveSmallIntegerField(default=7, verbose_name='推荐完成周期(天)')),
                ('scholarship_value', models.PositiveSmallIntegerField(verbose_name='为该作业分配的奖学金(贝里)')),
                ('note', models.TextField(blank=True, null=True)),
                ('enabled', models.BooleanField(default=True, help_text='本作业如果后期不需要了，不想让学员看到，可以设置为False')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.CourseChapter')),
            ],
            options={
                'verbose_name_plural': '12. 章节作业',
            },
        ),
        migrations.CreateModel(
            name='OftenAskedQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('question', models.CharField(max_length=255)),
                ('answer', models.TextField(max_length=1024)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': '08. 常见问题',
            },
        ),
        migrations.CreateModel(
            name='PricePolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('valid_period', models.SmallIntegerField(choices=[(1, '1天'), (3, '3天'), (7, '1周'), (14, '2周'), (30, '1个月'), (60, '2个月'), (90, '3个月'), (180, '6个月'), (210, '12个月'), (540, '18个月'), (720, '24个月')])),
                ('price', models.FloatField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': '15. 价格策略',
            },
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_percent', models.PositiveSmallIntegerField(help_text='只填百分值，如80,代表80%', verbose_name='奖励档位(时间百分比)')),
                ('value', models.PositiveIntegerField(verbose_name='奖学金数额')),
                ('degree_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.DegreeCourse')),
            ],
            options={
                'verbose_name_plural': '05.学位课奖学金',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('role', models.SmallIntegerField(choices=[(0, '讲师'), (1, '导师')], default=0)),
                ('title', models.CharField(max_length=64, verbose_name='职位、职称')),
                ('signature', models.CharField(blank=True, help_text='导师签名', max_length=255, null=True)),
                ('image', models.CharField(max_length=128)),
                ('brief', models.TextField(max_length=1024)),
            ],
            options={
                'verbose_name_plural': '04.导师或讲师',
            },
        ),
        migrations.AddField(
            model_name='degreecourse',
            name='teachers',
            field=models.ManyToManyField(to='api.Teacher', verbose_name='课程讲师'),
        ),
        migrations.AddField(
            model_name='coursedetail',
            name='teachers',
            field=models.ManyToManyField(to='api.Teacher', verbose_name='课程讲师'),
        ),
        migrations.AddField(
            model_name='course',
            name='degree_course',
            field=models.ForeignKey(blank=True, help_text='若是学位课程，此处关联学位表', null=True, on_delete=django.db.models.deletion.CASCADE, to='api.DegreeCourse'),
        ),
        migrations.AddField(
            model_name='course',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.CourseSubCategory'),
        ),
        migrations.AlterUniqueTogether(
            name='pricepolicy',
            unique_together=set([('content_type', 'object_id', 'valid_period')]),
        ),
        migrations.AlterUniqueTogether(
            name='oftenaskedquestion',
            unique_together=set([('content_type', 'object_id', 'question')]),
        ),
        migrations.AlterUniqueTogether(
            name='homework',
            unique_together=set([('chapter', 'title')]),
        ),
        migrations.AlterUniqueTogether(
            name='coursesection',
            unique_together=set([('chapter', 'section_link')]),
        ),
        migrations.AlterUniqueTogether(
            name='courseoutline',
            unique_together=set([('course_detail', 'title')]),
        ),
        migrations.AlterUniqueTogether(
            name='coursechapter',
            unique_together=set([('course', 'chapter')]),
        ),
    ]
