import django_filters

from backend.models import *


class GroupFilter(django_filters.FilterSet):
    class Meta:
        model = Group
        fields = ("grouptype", "leader__stuname", "groupname", "id", "leader")


class JudgementFilter(django_filters.FilterSet):
    class Meta:
        model = Judgement
        fields = ("homework", "judger", "group", "student", "student__stuname", "student__stuid", "group__leader__stuname")


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ("stuname", "stuid", "id",)