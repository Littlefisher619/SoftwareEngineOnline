from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-createat']

    username = models.CharField(u'用户名', max_length=255, unique=True)
    email = models.EmailField(u'邮箱', max_length=255, blank=True)
    stuid = models.TextField(u'学号', max_length=10, blank=False)
    stuname = models.TextField(u'姓名', max_length=255, blank=True)

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