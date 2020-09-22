from django.contrib.auth.models import AbstractUser
from django.db import models
import json


# Create your models here.


class User(AbstractUser):
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-createat']

    username = models.CharField(u'用户名', max_length=255, unique=True)
    email = models.EmailField(u'邮箱', max_length=255, blank=True)
    stuid = models.CharField(u'学号', max_length=10, blank=False)
    stuname = models.CharField(u'姓名', max_length=255, blank=True)

    GROUP_MEMBER = 0
    GROUP_LEADER = 1
    TEST_GROUP = 2
    TEACHER = 3

    ROLE_CHOICES = (
        (GROUP_MEMBER, '组员'),
        (GROUP_LEADER, '组长'),
        (TEST_GROUP, '测试组'),
        (TEACHER, '教师'),
    )

    role = models.PositiveSmallIntegerField(verbose_name="角色", choices=ROLE_CHOICES, default=GROUP_MEMBER)
    createat = models.DateTimeField(u'注册时间', auto_now_add='注册时间')

    def __str__(self):
        return self.username


class HomeWork(models.Model):
    class Meta:
        verbose_name = '作业'
        verbose_name_plural = verbose_name
        ordering = ['-createat']

    SIGNGLE = 0
    DOUBLE = 1
    GROUP = 2

    TYPE_CHOICES = (
        (SIGNGLE, '单人作业'),
        (DOUBLE, '结对作业'),
        (GROUP, '组队作业'),
    )

    id = models.BigAutoField(primary_key=True, editable=False)
    title = models.CharField(u'标题', blank=True, max_length=255)
    scorerules = models.TextField(u'得分规则', blank=True)
    author = models.ForeignKey(User, related_name='homework_author_user', verbose_name='发布者', on_delete=models.CASCADE)
    createat = models.DateTimeField(u'创建时间', auto_now_add=True)
    homeworktype = models.PositiveSmallIntegerField(verbose_name="作业类型", choices=TYPE_CHOICES, default=SIGNGLE)

    def __str__(self):
        return "HomeWork(%d) - %s" % (self.id, self.title)


class Group(models.Model):
    class Meta:
        verbose_name = '组队'
        verbose_name_plural = verbose_name
        ordering = ['-createat']

    DOUBLE = 1
    GROUP = 2
    TYPE_CHOICES = (
        (DOUBLE, '结对作业的组'),
        (GROUP, '团队项目的组'),
    )

    id = models.BigAutoField(primary_key=True, editable=False)

    leader = models.ForeignKey(User, related_name='group_leader_user', verbose_name='队长', on_delete=models.CASCADE)
    grouptype = models.PositiveSmallIntegerField(verbose_name="组队类型", choices=TYPE_CHOICES, default=DOUBLE)
    groupname = models.CharField(u'队伍名', max_length=255, blank=True)
    members = models.TextField(u'组员列表', blank=True)
    createat = models.DateTimeField(u'创建时间', auto_now_add=True)
    token = models.CharField(u'Token', max_length=255, blank=True)

    def __str__(self):
        return "Group(%d, %s) - %s" % (self.id, self.leader.username, self.groupname)

    @classmethod
    def filter_group_by_from_user(cls, user):
        double_group = None
        big_group = None

        try:
            double_group = Group.objects.get(leader=user, grouptype=Group.DOUBLE)
        except Group.DoesNotExist:
            for group in Group.objects.filter(grouptype=Group.DOUBLE):

                if user.pk in json.loads(group.members):
                    double_group = group
                    break

        try:
            big_group = Group.objects.get(leader=user, grouptype=Group.GROUP)
        except Group.DoesNotExist:
            for group in Group.objects.filter(grouptype=Group.GROUP):
                if user.pk in json.loads(group.members):
                    big_group = group
                    break

        return double_group, big_group


class Judgement(models.Model):
    class Meta:
        verbose_name = '评分'
        verbose_name_plural = verbose_name
        ordering = ['-createat']

    id = models.BigAutoField(primary_key=True, editable=False)
    homework = models.ForeignKey(HomeWork, related_name='judgement_homework', verbose_name='对应作业',
                                 on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group, related_name='judgement_group', verbose_name='对应组', on_delete=models.CASCADE,
                              blank=True, null=True)
    student = models.ForeignKey(User, related_name='judgement_user', verbose_name='对应学生', on_delete=models.CASCADE,
                                blank=True, null=True)
    scoredatail = models.TextField(u'评分详情', blank=True)
    judger = models.ForeignKey(User, related_name='judger_user', verbose_name='评分人', on_delete=models.CASCADE)
    createat = models.DateTimeField(u'创建时间', auto_now=True)

    def __str__(self):
        return "Group(%d, %s) - %s" % (self.id, self.judger.username, self.homework)


class Rate(models.Model):
    class Meta:
        verbose_name = '组内评分'
        verbose_name_plural = verbose_name
        ordering = ['-createat']

    id = models.BigAutoField(primary_key=True, editable=False)
    group = models.ForeignKey(Group, related_name='rate_group', verbose_name='对应组', on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, related_name='rate_owner_user', verbose_name='对应学生', on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(verbose_name='评分', null=True)
    rater = models.ForeignKey(User, related_name='rater_user', verbose_name='评分人', on_delete=models.CASCADE)
    createat = models.DateTimeField(u'创建时间', auto_now=True)
