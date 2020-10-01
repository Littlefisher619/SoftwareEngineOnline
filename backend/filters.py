import django_filters

from backend.models import *


class GroupFilter(django_filters.FilterSet):
    class Meta:
        model = Group
        fields = ("grouptype", "leader", "groupname", "id", )


class JudgementFilter(django_filters.FilterSet):
    class Meta:
        model = Judgement
        fields = ("homework", "judger", "group", "student",)


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ("stuname", "stuid", "id",)